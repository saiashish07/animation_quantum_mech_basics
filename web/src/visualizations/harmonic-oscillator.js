/**
 * Harmonic Oscillator Visualization
 */

class HarmonicOscillatorVisualizer {
    constructor(core) {
        this.core = core;
        this.currentState = 0;
        this.data = null;
    }

    async load(mass, omega, numStates) {
        try {
            this.data = await api.solveHarmonicOscillator(mass, omega, numStates);
            return this.data;
        } catch (error) {
            console.error('Failed to load harmonic oscillator:', error);
            throw error;
        }
    }

    visualize(stateIndex = 0) {
        if (!this.data) return;

        const x = this.data.x;
        const potential = this.data.potential;
        const psi = this.data.wavefunctions[stateIndex];
        const energies = this.data.energies;

        this.currentState = stateIndex;

        this.core.plotWavefunction(
            x, psi, potential, energies.slice(0, 5),
            {
                showWavefunction: true,
                showProbability: true,
                showPotential: true,
                showEnergyLevels: true,
                scale: 0.6
            }
        );

        return {
            energy: this.data.energies[stateIndex],
            analyticalEnergy: this.data.analytical_energies[stateIndex],
            x: x,
            psi: psi,
            probability: this.data.probability_densities[stateIndex]
        };
    }

    getStatistics(stateIndex) {
        if (!this.data) return null;

        const x = this.data.x;
        const dx = this.data.grid_info.dx;
        const psi = this.data.wavefunctions[stateIndex];
        const prob = this.data.probability_densities[stateIndex];

        const expX = this.computeExpectationValue(x, prob, dx);
        const expX2 = this.computeExpectationValue(
            x.map(xi => xi * xi), prob, dx
        );
        const expP = this.computeExpectationMomentum(x, psi, dx);
        const expP2 = this.computeExpectationMomentumSquared(x, psi, dx);

        const deltaX = Math.sqrt(Math.max(0, expX2 - expX * expX));
        const deltaP = Math.sqrt(Math.max(0, expP2 - expP * expP));

        return {
            quantumNumber: stateIndex,
            energy: this.data.energies[stateIndex],
            analyticalEnergy: this.data.analytical_energies[stateIndex],
            expectationX: expX,
            expectationP: expP,
            uncertaintyX: deltaX,
            uncertaintyP: deltaP,
            uncertaintyProduct: deltaX * deltaP,
            mass: this.data.parameters.mass,
            omega: this.data.parameters.omega,
            levelSpacing: this.data.parameters.level_spacing
        };
    }

    computeExpectationValue(x, prob, dx) {
        let sum = 0;
        for (let i = 0; i < x.length; i++) {
            sum += x[i] * prob[i];
        }
        return sum * dx;
    }

    computeExpectationMomentum(x, psi, dx) {
        let sum = 0;
        for (let i = 1; i < psi.length - 1; i++) {
            const dPsi = (psi[i + 1] - psi[i - 1]) / (2 * dx);
            sum += -Math.imag(psi[i] * Math.conj(dPsi));
        }
        return sum * dx;
    }

    computeExpectationMomentumSquared(x, psi, dx) {
        // ⟨p²⟩ = -∫ ψ* d²ψ/dx² dx
        let sum = 0;
        for (let i = 1; i < psi.length - 1; i++) {
            const d2Psi = (psi[i + 1] - 2 * psi[i] + psi[i - 1]) / (dx * dx);
            sum += -Math.real(psi[i] * Math.conj(d2Psi));
        }
        return sum * dx;
    }

    compareWithAnalytical() {
        if (!this.data) return null;

        const errors = this.data.energies.map((E, i) => {
            const analytical = this.data.analytical_energies[i];
            return {
                n: i,
                numerical: E,
                analytical: analytical,
                error: Math.abs(E - analytical) / analytical,
                relativeError: ((E - analytical) / analytical * 100).toFixed(3) + '%'
            };
        });

        return errors;
    }
}
