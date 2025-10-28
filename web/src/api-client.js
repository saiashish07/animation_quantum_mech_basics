/**
 * API Client for Quantum Simulations
 * Handles communication with backend server
 */

class QuantumSimulationAPI {
    constructor(baseUrl = 'http://localhost:5000/api') {
        this.baseUrl = baseUrl;
        this.cache = new Map();
    }

    /**
     * Solve infinite square well
     */
    async solveInfiniteWell(width, numStates) {
        const cacheKey = `iw-${width}-${numStates}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        try {
            const response = await fetch(`${this.baseUrl}/infinite-well`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ width, num_states: numStates })
            });
            
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            this.cache.set(cacheKey, data);
            return data;
        } catch (error) {
            console.error('Error solving infinite well:', error);
            throw error;
        }
    }

    /**
     * Solve finite square well
     */
    async solveFiniteWell(width, height, numStates) {
        const cacheKey = `fw-${width}-${height}-${numStates}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        try {
            const response = await fetch(`${this.baseUrl}/finite-well`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    width, 
                    height,
                    num_states: numStates 
                })
            });
            
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            this.cache.set(cacheKey, data);
            return data;
        } catch (error) {
            console.error('Error solving finite well:', error);
            throw error;
        }
    }

    /**
     * Simulate tunneling
     */
    async simulateTunneling(barrierHeight, barrierWidth, particleEnergy, packetSigma, duration = 1000) {
        try {
            const response = await fetch(`${this.baseUrl}/tunneling`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    barrier_height: barrierHeight,
                    barrier_width: barrierWidth,
                    particle_energy: particleEnergy,
                    packet_sigma: packetSigma,
                    duration: duration
                })
            });
            
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error simulating tunneling:', error);
            throw error;
        }
    }

    /**
     * Solve harmonic oscillator
     */
    async solveHarmonicOscillator(mass, omega, numStates) {
        const cacheKey = `ho-${mass}-${omega}-${numStates}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        try {
            const response = await fetch(`${this.baseUrl}/harmonic-oscillator`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mass,
                    omega,
                    num_states: numStates
                })
            });
            
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            this.cache.set(cacheKey, data);
            return data;
        } catch (error) {
            console.error('Error solving harmonic oscillator:', error);
            throw error;
        }
    }

    /**
     * Get transmission coefficient
     */
    async getTransmissionCoefficient(barrierHeight, barrierWidth, particleEnergy) {
        try {
            const response = await fetch(`${this.baseUrl}/transmission-coefficient`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    barrier_height: barrierHeight,
                    barrier_width: barrierWidth,
                    particle_energy: particleEnergy
                })
            });
            
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error getting transmission coefficient:', error);
            throw error;
        }
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
    }
}

// Create global API instance
const api = new QuantumSimulationAPI();
