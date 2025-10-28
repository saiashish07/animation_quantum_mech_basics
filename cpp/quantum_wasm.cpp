/**
 * Fast Wavefunction Computation Module
 * C++ implementation compiled to WebAssembly
 */

#include <emscripten/emscripten.h>
#include <emscripten/bind.h>
#include <vector>
#include <cmath>
#include <complex>

using namespace std;
using Complex = complex<double>;

// Gaussian wave packet creation
extern "C" {
    EMSCRIPTEN_KEEPALIVE
    double* create_gaussian_packet(double* x, int n_points, 
                                    double x0, double sigma, 
                                    double k0, double amplitude) {
        auto* psi = new double[n_points * 2];  // Real and imaginary parts
        
        for (int i = 0; i < n_points; i++) {
            double xi = x[i];
            double gaussian = amplitude * exp(-pow(xi - x0, 2) / (2 * sigma * sigma));
            double phase = k0 * xi;
            
            psi[2*i] = gaussian * cos(phase);        // Real part
            psi[2*i+1] = gaussian * sin(phase);      // Imaginary part
        }
        
        return psi;
    }
    
    EMSCRIPTEN_KEEPALIVE
    void free_array(double* ptr) {
        delete[] ptr;
    }
}

// Probability density computation
extern "C" {
    EMSCRIPTEN_KEEPALIVE
    double* compute_probability_density(double* psi, int n_points) {
        auto* prob = new double[n_points];
        
        for (int i = 0; i < n_points; i++) {
            double real_part = psi[2*i];
            double imag_part = psi[2*i+1];
            prob[i] = real_part * real_part + imag_part * imag_part;
        }
        
        return prob;
    }
}

// Normalization
extern "C" {
    EMSCRIPTEN_KEEPALIVE
    void normalize_wavefunction(double* psi, int n_points, double dx) {
        double norm_sq = 0.0;
        
        // Compute norm
        for (int i = 0; i < n_points; i++) {
            double real_part = psi[2*i];
            double imag_part = psi[2*i+1];
            norm_sq += (real_part * real_part + imag_part * imag_part) * dx;
        }
        
        double norm = sqrt(norm_sq);
        
        // Normalize
        for (int i = 0; i < n_points; i++) {
            psi[2*i] /= norm;
            psi[2*i+1] /= norm;
        }
    }
}

// Expectation value computation
extern "C" {
    EMSCRIPTEN_KEEPALIVE
    double compute_expectation_value(double* x, double* prob, int n_points, double dx) {
        double exp_val = 0.0;
        
        for (int i = 0; i < n_points; i++) {
            exp_val += x[i] * prob[i];
        }
        
        return exp_val * dx;
    }
}

// WKB transmission coefficient
extern "C" {
    EMSCRIPTEN_KEEPALIVE
    double compute_transmission_coefficient_wkb(double E, double* V, 
                                                 double* x, int n_points) {
        double kappa = 0.0;
        double dx = (x[n_points-1] - x[0]) / (n_points - 1);
        
        for (int i = 0; i < n_points; i++) {
            if (V[i] > E) {
                kappa += sqrt(2.0 * (V[i] - E)) * dx;
            }
        }
        
        double T = exp(-2.0 * kappa);
        return T < 1.0 ? T : 1.0;
    }
}

// Fast convolution for numerical derivatives
extern "C" {
    EMSCRIPTEN_KEEPALIVE
    double* compute_derivative(double* psi, int n_points, double dx) {
        auto* dpsi = new double[n_points * 2];
        
        // Forward difference
        for (int i = 0; i < n_points - 1; i++) {
            dpsi[2*i] = (psi[2*(i+1)] - psi[2*i]) / dx;
            dpsi[2*i+1] = (psi[2*(i+1)+1] - psi[2*i+1]) / dx;
        }
        
        // Handle boundary
        dpsi[2*(n_points-1)] = dpsi[2*(n_points-2)];
        dpsi[2*(n_points-1)+1] = dpsi[2*(n_points-2)+1];
        
        return dpsi;
    }
}

// Second derivative (Laplacian)
extern "C" {
    EMSCRIPTEN_KEEPALIVE
    double* compute_second_derivative(double* psi, int n_points, double dx) {
        auto* d2psi = new double[n_points * 2];
        double dx_sq = dx * dx;
        
        for (int i = 1; i < n_points - 1; i++) {
            double real_part = (psi[2*(i+1)] - 2*psi[2*i] + psi[2*(i-1)]) / dx_sq;
            double imag_part = (psi[2*(i+1)+1] - 2*psi[2*i+1] + psi[2*(i-1)+1]) / dx_sq;
            
            d2psi[2*i] = real_part;
            d2psi[2*i+1] = imag_part;
        }
        
        // Handle boundaries
        d2psi[0] = d2psi[2];
        d2psi[1] = d2psi[3];
        d2psi[2*(n_points-1)] = d2psi[2*(n_points-2)];
        d2psi[2*(n_points-1)+1] = d2psi[2*(n_points-2)+1];
        
        return d2psi;
    }
}
