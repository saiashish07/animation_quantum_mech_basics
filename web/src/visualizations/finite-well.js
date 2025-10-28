/**
 * Finite Square Well Visualization
 */

class FiniteWellVisualizer {
    constructor(core) {
        this.core = core;
        this.currentState = 1;
        this.data = null;
    }

    async load(width, height, numStates) {
        try {
            this.data = await api.solveFiniteWell(width, height, numStates);
            return this.data;
        } catch (error) {
            console.error('Failed to load finite well:', error);
            throw error;
        }
    }

    visualize(stateIndex = 1) {
        if (!this.data) return;

        const x = this.data.x;
        const potential = this.data.potential;
        const psi = this.data.wavefunctions[stateIndex - 1];
        const energies = this.data.energies;

        this.currentState = stateIndex;

        this.core.plotWavefunction(
            x, psi, potential, energies.slice(0, 5),
            {
                showWavefunction: true,
                showProbability: false,
                showPotential: true,
                showEnergyLevels: true,
                scale: 1.0
            }
        );

        return {
            energy: this.data.energies[stateIndex - 1],
            boundStates: this.data.bound_states,
            x: x,
            psi: psi,
            probability: this.data.probability_densities[stateIndex - 1]
        };
    }

    getStatistics(stateIndex) {
        if (!this.data) return null;

        const x = this.data.x;
        const dx = this.data.grid_info.dx;
        const psi = this.data.wavefunctions[stateIndex - 1];
        const prob = this.data.probability_densities[stateIndex - 1];

        const expX = this.computeExpectationValue(x, prob, dx);
        const expP = this.computeExpectationMomentum(x, psi, dx);

        return {
            energy: this.data.energies[stateIndex - 1],
            expectationX: expX,
            expectationP: expP,
            state: stateIndex,
            boundStates: this.data.bound_states,
            penetration: this.computePenetration(psi, dx)
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
            // For real wavefunctions this is approximately zero
            sum += -Math.imag(psi[i] * Math.conj(dPsi));
        }
        return sum * dx;
    }

    computePenetration(psi, dx) {
        // Measure of wavefunction in classically forbidden region
        const prob = psi.map(p => Math.abs(p) ** 2);
        const midpoint = Math.floor(prob.length / 2);
        const rightHalf = prob.slice(midpoint);
        const penetration = rightHalf.slice(-20).reduce((a, b) => a + b, 0) * dx;
        return Math.max(0, Math.min(1, penetration));
    }
}
