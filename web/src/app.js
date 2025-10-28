/**
 * Main Application Controller
 * Orchestrates the quantum simulation application
 */

class QuantumSimulationApp {
    constructor() {
        this.canvas = null;
        this.core = null;
        this.visualizers = {};
        this.currentSimulation = 'infinite-well';
        this.currentVisualizer = null;

        this.init();
    }

    async init() {
        try {
            // Get canvas
            this.canvas = document.getElementById('webgl-canvas');
            if (!this.canvas) {
                throw new Error('Canvas element not found');
            }

            // Initialize WebGL core
            this.core = new QuantumVisualizerCore(this.canvas);

            // Create visualizers
            this.visualizers = {
                'infinite-well': new InfiniteWellVisualizer(this.core),
                'finite-well': new FiniteWellVisualizer(this.core),
                'tunneling': new TunnelingVisualizer(this.core),
                'harmonic': new HarmonicOscillatorVisualizer(this.core)
            };

            // Load initial simulation
            await this.loadSimulation('infinite-well');

            ui.showLoading(false);
        } catch (error) {
            console.error('Failed to initialize app:', error);
            ui.showMessage('Failed to initialize application: ' + error.message, 'error');
        }
    }

    async loadSimulation(simType) {
        try {
            ui.showLoading(true);

            this.currentSimulation = simType;
            this.currentVisualizer = this.visualizers[simType];

            switch (simType) {
                case 'infinite-well':
                    await this.loadInfiniteWell();
                    break;
                case 'finite-well':
                    await this.loadFiniteWell();
                    break;
                case 'tunneling':
                    await this.loadTunneling();
                    break;
                case 'harmonic':
                    await this.loadHarmonic();
                    break;
            }

            ui.showLoading(false);
        } catch (error) {
            console.error('Failed to load simulation:', error);
            ui.showMessage('Failed to load simulation: ' + error.message, 'error');
            ui.showLoading(false);
        }
    }

    async loadInfiniteWell() {
        const width = ui.getParameter('well-width');
        const numStates = ui.getParameter('num-eigenstates');

        await this.currentVisualizer.load(width, numStates);
        this.updateInfiniteWellVisualization();
    }

    updateInfiniteWellVisualization() {
        const stateIndex = ui.getParameter('selected-state');
        const result = this.currentVisualizer.visualize(stateIndex);

        if (result) {
            const stats = this.currentVisualizer.getStatistics(stateIndex);
            ui.updateStatistics({
                energy: result.energy,
                e1: this.currentVisualizer.data.energies[0],
                expectationX: stats.expectationX,
                expectationP: stats.expectationP
            });
        }
    }

    async loadFiniteWell() {
        const width = ui.getParameter('finite-width');
        const height = ui.getParameter('well-height');
        const numStates = ui.getParameter('finite-num-states');

        await this.currentVisualizer.load(width, height, numStates);
        this.updateFiniteWellVisualization();
    }

    updateFiniteWellVisualization() {
        const stateIndex = ui.getParameter('finite-selected-state');
        const result = this.currentVisualizer.visualize(stateIndex);

        if (result) {
            const stats = this.currentVisualizer.getStatistics(stateIndex);
            ui.updateStatistics({
                energy: result.energy,
                e1: this.currentVisualizer.data.energies[0],
                expectationX: stats.expectationX,
                expectationP: stats.expectationP
            });

            console.log(`Bound States: ${result.boundStates}`, 
                        `Penetration: ${stats.penetration.toFixed(3)}`);
        }
    }

    async loadTunneling() {
        const barrierHeight = ui.getParameter('barrier-height');
        const barrierWidth = ui.getParameter('barrier-width');
        const particleEnergy = ui.getParameter('particle-energy');
        const packetSigma = ui.getParameter('packet-sigma');

        await this.currentVisualizer.load(barrierHeight, barrierWidth, particleEnergy, packetSigma);
        this.updateTunnelingVisualization();
    }

    updateTunnelingVisualization() {
        const result = this.currentVisualizer.visualize(0);

        if (result) {
            const coeffs = this.currentVisualizer.getCoefficients();
            document.getElementById('transmission-coeff').textContent = 
                (coeffs.transmission * 100).toFixed(2) + '%';
            document.getElementById('reflection-coeff').textContent = 
                (coeffs.reflection * 100).toFixed(2) + '%';

            const insights = this.currentVisualizer.getPhysicalInsights();
            console.log('Tunneling Insights:', insights);
        }
    }

    async loadHarmonic() {
        const mass = ui.getParameter('mass');
        const omega = ui.getParameter('omega');
        const numStates = ui.getParameter('harm-num-states');

        await this.currentVisualizer.load(mass, omega, numStates);
        this.updateHarmonicVisualization();
    }

    updateHarmonicVisualization() {
        const stateIndex = ui.getParameter('harm-selected-state');
        const result = this.currentVisualizer.visualize(stateIndex);

        if (result) {
            const stats = this.currentVisualizer.getStatistics(stateIndex);
            ui.updateStatistics({
                energy: result.energy,
                e1: this.currentVisualizer.data.energies[0],
                expectationX: stats.expectationX,
                expectationP: stats.expectationP
            });

            const comparison = this.currentVisualizer.compareWithAnalytical();
            console.log('Harmonic Oscillator Comparison:', comparison);
        }
    }

    onParameterChange() {
        switch (this.currentSimulation) {
            case 'infinite-well':
                this.loadInfiniteWell();
                break;
            case 'finite-well':
                this.loadFiniteWell();
                break;
            case 'tunneling':
                this.loadTunneling();
                break;
            case 'harmonic':
                this.loadHarmonic();
                break;
        }
    }

    onVisualizationModeChange() {
        const mode = document.getElementById('visualization-mode').value;
        const showPotential = document.getElementById('show-potential').checked;
        const showEnergy = document.getElementById('show-energy').checked;

        const x = this.currentVisualizer.data.x;
        const potential = this.currentVisualizer.data.potential;
        const energies = this.currentVisualizer.data.energies.slice(0, 5);

        let psi, prob;

        switch (this.currentSimulation) {
            case 'infinite-well':
                const iwState = ui.getParameter('selected-state');
                psi = this.currentVisualizer.data.wavefunctions[iwState - 1];
                prob = this.currentVisualizer.data.probability_densities[iwState - 1];
                break;
            case 'finite-well':
                const fwState = ui.getParameter('finite-selected-state');
                psi = this.currentVisualizer.data.wavefunctions[fwState - 1];
                prob = this.currentVisualizer.data.probability_densities[fwState - 1];
                break;
            case 'harmonic':
                const hoState = ui.getParameter('harm-selected-state');
                psi = this.currentVisualizer.data.wavefunctions[hoState];
                prob = this.currentVisualizer.data.probability_densities[hoState];
                break;
            case 'tunneling':
                psi = this.currentVisualizer.data.initial_wavefunction;
                prob = this.currentVisualizer.data.initial_probability;
                break;
        }

        this.core.plotWavefunction(
            x, psi, 
            showPotential ? potential : null,
            showEnergy ? energies : null,
            {
                showWavefunction: mode === 'wavefunction' || mode === 'both',
                showProbability: mode === 'probability' || mode === 'both',
                showPotential: showPotential,
                showEnergyLevels: showEnergy,
                scale: 1.0
            }
        );
    }

    updateVisualization() {
        this.onVisualizationModeChange();
    }

    reset() {
        this.loadSimulation(this.currentSimulation);
    }

    dispose() {
        if (this.core) {
            this.core.dispose();
        }
    }
}

// Global app instance
let app;

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', () => {
    app = new QuantumSimulationApp();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (app) {
        app.dispose();
    }
});
