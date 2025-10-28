/**
 * Infinite Square Well Visualization
 */

class InfiniteWellVisualizer {
    constructor(core) {
        this.core = core;
        this.currentState = 1;
        this.data = null;
    }

    async load(width, numStates) {
        try {
            this.data = await api.solveInfiniteWell(width, numStates);
            return this.data;
        } catch (error) {
            console.error('Failed to load infinite well:', error);
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

        // Expected value of x
        const expX = this.computeExpectationValue(x, prob, dx);

        // Expected value of p
        const expP = this.computeExpectationMomentum(x, psi, dx);

        return {
            energy: this.data.energies[stateIndex - 1],
            expectationX: expX,
            expectationP: expP,
            state: stateIndex,
            wellWidth: this.data.potential.length
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
        // ⟨p⟩ = -i ∫ ψ* dψ/dx dx
        // Approximate derivative using finite differences
        let sum = 0;
        for (let i = 1; i < psi.length - 1; i++) {
            const dPsi = (psi[i + 1] - psi[i - 1]) / (2 * dx);
            sum += -Math.imag(psi[i] * Math.conj(dPsi));
        }
        return sum * dx;
    }
}
