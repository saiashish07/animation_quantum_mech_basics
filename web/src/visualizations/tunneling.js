/**
 * Quantum Tunneling Visualization
 */

class TunnelingVisualizer {
    constructor(core) {
        this.core = core;
        this.data = null;
        this.animationRunning = false;
        this.currentFrame = 0;
    }

    async load(barrierHeight, barrierWidth, particleEnergy, packetSigma) {
        try {
            this.data = await api.simulateTunneling(
                barrierHeight, barrierWidth, particleEnergy, packetSigma
            );
            return this.data;
        } catch (error) {
            console.error('Failed to load tunneling simulation:', error);
            throw error;
        }
    }

    visualize(frameIndex = 0) {
        if (!this.data) return;

        const x = this.data.x;
        const potential = this.data.potential;
        const energies = [this.data.barrier_parameters.particle_energy];

        let wavefunction, probability;

        if (frameIndex === 0) {
            wavefunction = this.data.initial_wavefunction;
            probability = this.data.initial_probability;
        } else if (frameIndex === 1) {
            wavefunction = this.data.final_wavefunction;
            probability = this.data.final_probability;
        } else {
            // Interpolate
            const samples = this.data.trajectory_samples;
            if (samples[frameIndex]) {
                wavefunction = samples[frameIndex].wavefunction;
                probability = samples[frameIndex].probability;
            } else {
                wavefunction = this.data.final_wavefunction;
                probability = this.data.final_probability;
            }
        }

        this.core.plotWavefunction(
            x, wavefunction, potential, energies,
            {
                showWavefunction: true,
                showProbability: true,
                showPotential: true,
                showEnergyLevels: true,
                scale: 0.8
            }
        );

        return {
            transmission: this.data.transmission_coefficient,
            reflection: this.data.reflection_coefficient,
            x: x,
            wavefunction: wavefunction,
            probability: probability,
            frame: frameIndex
        };
    }

    startAnimation() {
        if (this.animationRunning) return;

        this.animationRunning = true;
        this.currentFrame = 0;
        this.animateFrame();
    }

    stopAnimation() {
        this.animationRunning = false;
    }

    animateFrame() {
        if (!this.animationRunning || !this.data) return;

        this.visualize(this.currentFrame);
        this.currentFrame = (this.currentFrame + 1) % (this.data.trajectory_samples.length + 1);

        setTimeout(() => this.animateFrame(), 50);
    }

    getCoefficients() {
        if (!this.data) return null;

        return {
            transmission: this.data.transmission_coefficient,
            reflection: this.data.reflection_coefficient,
            barrierHeight: this.data.barrier_parameters.height,
            barrierWidth: this.data.barrier_parameters.width,
            particleEnergy: this.data.barrier_parameters.particle_energy
        };
    }

    getPhysicalInsights() {
        if (!this.data) return null;

        const T = this.data.transmission_coefficient;
        const E = this.data.barrier_parameters.particle_energy;
        const V = this.data.barrier_parameters.height;

        return {
            transmissionProbability: T,
            reflectionProbability: 1 - T,
            barrierThickness: this.data.barrier_parameters.width,
            relativeEnergy: (E / V).toFixed(3),
            classicallyForbidden: E < V,
            description: E < V 
                ? `Particle with E=${E.toFixed(1)} tunneling through V=${V.toFixed(1)}`
                : `Particle with E=${E.toFixed(1)} over potential V=${V.toFixed(1)}`
        };
    }
}
