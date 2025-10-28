/**
 * UI Controls and Event Handling
 */

class UIController {
    constructor() {
        this.controls = {};
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Navigation buttons
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchSimulation(e.target.dataset.simulation);
            });
        });

        // Range inputs with value display
        this.setupRangeInputs();

        // Visualization mode
        const vizMode = document.getElementById('visualization-mode');
        if (vizMode) {
            vizMode.addEventListener('change', () => {
                app.onVisualizationModeChange();
            });
        }

        // Checkboxes
        document.getElementById('show-potential')?.addEventListener('change', () => {
            app.updateVisualization();
        });
        document.getElementById('show-energy')?.addEventListener('change', () => {
            app.updateVisualization();
        });
    }

    setupRangeInputs() {
        const ranges = document.querySelectorAll('input[type="range"]');
        ranges.forEach(input => {
            input.addEventListener('input', (e) => {
                const displayId = e.target.id + '-val';
                const display = document.getElementById(displayId);
                if (display) {
                    display.textContent = parseFloat(e.target.value).toFixed(1);
                }
                app.onParameterChange();
            });
        });
    }

    switchSimulation(simType) {
        // Update active button
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-simulation="${simType}"]`).classList.add('active');

        // Update control panel
        this.updateControlPanel(simType);

        // Load new simulation
        app.loadSimulation(simType);
    }

    updateControlPanel(simType) {
        const groups = document.querySelectorAll('.control-group');
        groups.forEach(g => g.style.display = 'none');

        const titleMap = {
            'infinite-well': 'Infinite Square Well',
            'finite-well': 'Finite Square Well',
            'tunneling': 'Quantum Tunneling',
            'harmonic': 'Harmonic Oscillator'
        };

        document.getElementById('simulation-title').textContent = titleMap[simType];

        const controlMap = {
            'infinite-well': 'infinite-well-controls',
            'finite-well': 'finite-well-controls',
            'tunneling': 'tunneling-controls',
            'harmonic': 'harmonic-controls'
        };

        const controlId = controlMap[simType];
        if (controlId) {
            document.getElementById(controlId).style.display = 'block';
        }

        // Always show general controls (last group)
        const generalControls = document.querySelectorAll('.control-group');
        generalControls[generalControls.length - 1].style.display = 'block';
    }

    getParameter(id) {
        const element = document.getElementById(id);
        return element ? parseFloat(element.value) : null;
    }

    setParameter(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.value = value;
            const displayId = id + '-val';
            const display = document.getElementById(displayId);
            if (display) {
                display.textContent = parseFloat(value).toFixed(1);
            }
        }
    }

    updateStatistics(stats) {
        if (stats.energy !== undefined) {
            document.getElementById('stat-energy').textContent = 
                stats.energy.toFixed(3);
        }
        if (stats.e1 !== undefined) {
            document.getElementById('stat-e1').textContent = 
                stats.e1.toFixed(3);
        }
        if (stats.expectationX !== undefined) {
            document.getElementById('stat-x').textContent = 
                stats.expectationX.toFixed(3);
        }
        if (stats.expectationP !== undefined) {
            document.getElementById('stat-p').textContent = 
                stats.expectationP.toFixed(3);
        }
    }

    showLoading(show = true) {
        const loader = document.getElementById('loading');
        if (loader) {
            if (show) {
                loader.classList.remove('hidden');
            } else {
                loader.classList.add('hidden');
            }
        }
    }

    showMessage(message, type = 'info') {
        console.log(`[${type.toUpperCase()}] ${message}`);
        // Could be extended to show toast notifications
    }
}

/**
 * Global UI Controller
 */
const ui = new UIController();

/**
 * Control Panel Toggle
 */
function toggleControlPanel() {
    const panel = document.querySelector('.control-panel');
    panel.classList.toggle('hidden');
}

/**
 * Reset Simulation
 */
function resetSimulation() {
    if (app) {
        app.reset();
    }
}

/**
 * Start Tunneling Animation
 */
function startTunnelingAnimation() {
    if (app && app.currentVisualizer && app.currentVisualizer.startAnimation) {
        app.currentVisualizer.startAnimation();
    }
}
