/**
 * Dashboard Controller - Main application orchestrator
 * Coordinates API calls, WebSocket updates, and UI rendering
 */

class QuantumDashboard {
    constructor() {
        // Initialize services with correct base URLs
        this.api = new QuantumAPIService('http://localhost:5000');
        this.websocket = new QuantumWebSocketService('http://localhost:5000');
        this.stateManager = new QuantumStateManager();

        // Visualizers
        this.visualizers = {};

        // Performance tracking
        this.lastApiTime = 0;
        this.frameCount = 0;
        this.fps = 0;

        // Initialize
        this.initializeDOM();
        this.setupEventListeners();
        this.setupWebSocketHandlers();
        this.setupStateObservers();
        this.initializeVisualizers();
        this.checkServerHealth();
    }

    /**
     * Initialize DOM elements and canvases
     */
    initializeDOM() {
        // Energy Levels Canvas
        const energyCanvas = document.getElementById('energyLevelsCanvas');
        if (energyCanvas) {
            energyCanvas.width = energyCanvas.offsetWidth;
            energyCanvas.height = energyCanvas.offsetHeight;
            this.visualizers.energyLevels = new EnergyLevelsVisualizer(energyCanvas);
        }

        // Probability Density Canvas
        const probCanvas = document.getElementById('probabilityCanvas');
        if (probCanvas) {
            probCanvas.width = probCanvas.offsetWidth;
            probCanvas.height = probCanvas.offsetHeight;
            this.visualizers.probability = new ProbabilityDensityVisualizer(probCanvas);
        }

        // Wavefunction Canvas (for 3D rendering with Three.js)
        const waveCanvas = document.getElementById('wavefunctionCanvas');
        if (waveCanvas) {
            waveCanvas.width = waveCanvas.offsetWidth;
            waveCanvas.height = waveCanvas.offsetHeight;
            this.setupThreeJsRenderer(waveCanvas);
        }

        // Detailed Canvas
        const detailedCanvas = document.getElementById('detailedCanvas');
        if (detailedCanvas) {
            detailedCanvas.width = detailedCanvas.offsetWidth;
            detailedCanvas.height = detailedCanvas.offsetHeight;
        }
    }

    /**
     * Initialize Three.js for 3D wavefunction visualization
     */
    setupThreeJsRenderer(canvas) {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(
            75,
            canvas.clientWidth / canvas.clientHeight,
            0.1,
            1000
        );
        const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
        renderer.setSize(canvas.clientWidth, canvas.clientHeight);
        renderer.setClearColor(0x0a0a0a, 1);

        camera.position.z = 3;

        // Store for later updates
        this.threeJsRenderer = {
            scene,
            camera,
            renderer,
            mesh: null
        };

        // Start animation loop
        const animate = () => {
            requestAnimationFrame(animate);
            if (this.threeJsRenderer.mesh) {
                this.threeJsRenderer.mesh.rotation.x += 0.002;
                this.threeJsRenderer.mesh.rotation.y += 0.003;
            }
            renderer.render(scene, camera);
        };
        animate();
    }

    /**
     * Initialize all visualizers
     */
    initializeVisualizers() {
        console.log('[Dashboard] Initializing visualizers');
        // Visualizers are already created in initializeDOM
    }

    /**
     * Setup event listeners for UI controls
     */
    setupEventListeners() {
        // Simulation type selector
        document.getElementById('simulationType').addEventListener('change', (e) => {
            this.onSimulationTypeChanged(e.target.value);
        });

        // Parameter sliders
        document.getElementById('wellWidth')?.addEventListener('input', (e) => {
            document.getElementById('widthValue').textContent = e.target.value;
        });

        document.getElementById('numStates')?.addEventListener('input', (e) => {
            document.getElementById('statesValue').textContent = e.target.value;
        });

        // Similar for other sliders
        ['finiteWidth', 'wellDepth', 'finiteNumStates', 'barrierHeight', 
         'barrierWidth', 'particleEnergy', 'omega', 'harmonicNumStates'].forEach(id => {
            const elem = document.getElementById(id);
            if (elem) {
                elem.addEventListener('input', (e) => {
                    const labelId = id + 'Value';
                    const label = document.getElementById(labelId);
                    if (label) label.textContent = e.target.value;
                });
            }
        });

        // Run simulation button
        document.getElementById('runSimulation')?.addEventListener('click', () => {
            this.runSimulation();
        });

        // Visualization toggles
        document.getElementById('showEnergyLevels')?.addEventListener('change', (e) => {
            this.stateManager.toggleGraphType('energy');
            this.updateVisualization();
        });

        document.getElementById('showProbability')?.addEventListener('change', (e) => {
            this.stateManager.toggleGraphType('probability');
            this.updateVisualization();
        });

        document.getElementById('showWavefunction')?.addEventListener('change', (e) => {
            this.stateManager.toggleGraphType('wavefunction');
            this.updateVisualization();
        });

        document.getElementById('showStatistics')?.addEventListener('change', (e) => {
            this.stateManager.toggleGraphType('statistics');
            this.updateStatistics();
        });

        // WebSocket controls
        document.getElementById('enableLiveUpdates')?.addEventListener('change', (e) => {
            if (e.target.checked) {
                this.websocket.subscribe(this.stateManager.getCurrentSimulation());
            } else {
                this.websocket.unsubscribeAll();
            }
        });

        document.getElementById('connectWebSocket')?.addEventListener('click', () => {
            this.websocket.connect();
        });

        // Webhook controls
        document.getElementById('registerWebhook')?.addEventListener('click', () => {
            this.registerWebhook();
        });

        // Detailed visualization toggles
        document.getElementById('toggleComparison')?.addEventListener('click', () => {
            this.showComparisonPlot();
        });

        document.getElementById('toggleTrajectory')?.addEventListener('click', () => {
            this.showTrajectoryPlot();
        });

        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }

    /**
     * Setup WebSocket event handlers
     */
    setupWebSocketHandlers() {
        this.websocket.on('connect', (data) => {
            console.log('[WebSocket] Connected:', data);
            this.updateConnectionStatus(true);
            document.getElementById('connectionStatus').textContent = 'Connected';
            document.getElementById('connectionStatus').className = 'status connected';
        });

        this.websocket.on('disconnect', () => {
            console.log('[WebSocket] Disconnected');
            this.updateConnectionStatus(false);
            document.getElementById('connectionStatus').textContent = 'Disconnected';
            document.getElementById('connectionStatus').className = 'status disconnected';
        });

        this.websocket.on('energy_update', (data) => {
            console.log('[WebSocket] Energy update:', data);
            this.handleEnergyUpdate(data);
        });

        this.websocket.on('probability_update', (data) => {
            console.log('[WebSocket] Probability update:', data);
            this.handleProbabilityUpdate(data);
        });

        this.websocket.on('statistics_update', (data) => {
            console.log('[WebSocket] Statistics update:', data);
            this.updateStatistics(data);
        });

        this.websocket.on('error', (error) => {
            console.error('[WebSocket] Error:', error);
            this.showError('WebSocket error: ' + error);
        });
    }

    /**
     * Setup state manager observers
     */
    setupStateObservers() {
        this.stateManager.subscribe((action, data, state) => {
            console.log(`[State] ${action}:`, data);
            
            switch (action) {
                case 'parameters-changed':
                    this.onParametersChanged(data);
                    break;
                case 'data-updated':
                    this.onDataUpdated(data);
                    break;
                case 'loading-changed':
                    this.onLoadingChanged(data);
                    break;
                case 'simulation-changed':
                    this.onSimulationChanged(data);
                    break;
                case 'display-mode-changed':
                    this.updateVisualization();
                    break;
            }
        });
    }

    /**
     * Check server health
     */
    async checkServerHealth() {
        try {
            const health = await this.api.healthCheck();
            console.log('[Server] Health check:', health);
            document.getElementById('serverStatus').textContent = 
                `Server: ✓ (${health.connected_clients} clients)`;
        } catch (error) {
            console.error('[Server] Health check failed:', error);
            document.getElementById('serverStatus').textContent = 'Server: ✗ Offline';
            this.showError('Cannot connect to server. Is it running?');
        }

        // Check again every 30 seconds
        setTimeout(() => this.checkServerHealth(), 30000);
    }

    /**
     * On simulation type changed
     */
    onSimulationTypeChanged(simType) {
        this.stateManager.setCurrentSimulation(simType);
        
        // Hide all control groups
        document.querySelectorAll('.control-group').forEach(elem => {
            elem.style.display = 'none';
        });
        
        // Show appropriate control group
        document.getElementById(`${simType}-controls`)?.style.removeProperty('display');
    }

    /**
     * Run the selected simulation
     */
    async runSimulation() {
        const simType = this.stateManager.getCurrentSimulation();
        const parameters = this.stateManager.getSimulationParameters(simType);

        this.stateManager.setLoading(simType, true);
        this.updateStatus('Running simulation...');
        document.getElementById('runSimulation').disabled = true;

        const startTime = performance.now();

        try {
            const result = await this.api.fullSimulation(simType, parameters);

            const endTime = performance.now();
            this.lastApiTime = endTime - startTime;

            if (result.success) {
                this.stateManager.setSimulationData(simType, result.data);
                this.updateStatus('Simulation complete');
                console.log(`[API] Simulation took ${this.lastApiTime.toFixed(2)}ms`);
            } else {
                this.showError(result.error);
                this.updateStatus('Simulation failed');
            }
        } catch (error) {
            this.showError('API Error: ' + error.message);
            this.updateStatus('Error');
            console.error('[API] Error:', error);
        } finally {
            this.stateManager.setLoading(simType, false);
            document.getElementById('runSimulation').disabled = false;
        }
    }

    /**
     * Update visualization with current data
     */
    updateVisualization() {
        const simType = this.stateManager.getCurrentSimulation();
        const data = this.stateManager.getSimulationData(simType);
        const graphTypes = this.stateManager.getGraphTypes();

        if (!data) return;

        // Energy Levels
        if (graphTypes.energy && this.visualizers.energyLevels) {
            this.visualizers.energyLevels.setEnergyData(
                data.energy_levels.values,
                {
                    analytical: data.analytical_comparison?.map(a => a.analytical_energy),
                    labels: data.energy_levels.labels,
                    errors: data.analytical_comparison?.map(a => a.error),
                    potentialHeight: data.potential?.height
                }
            );
            this.visualizers.energyLevels.render();
        }

        // Probability Density
        if (graphTypes.probability && this.visualizers.probability) {
            const densities = data.probability_densities.map(pd => pd.values);
            this.visualizers.probability.setProbabilityData(
                data.grid.x,
                densities,
                { labels: data.probability_densities.map(pd => `State ${pd.state}`) }
            );
            this.visualizers.probability.render();
        }

        // Wavefunction (3D if available)
        if (graphTypes.wavefunction && data.wavefunctions) {
            this.updateWavefunctionVisualization(data);
        }

        // Statistics
        if (graphTypes.statistics && data.statistics) {
            this.updateStatistics(data.statistics);
        }

        // Update status
        document.getElementById('lastUpdated').textContent = 
            new Date(data.timestamp).toLocaleTimeString();
        document.getElementById('groundStateEnergy').textContent = 
            data.energy_levels.ground_state?.toFixed(6) || '—';
    }

    /**
     * Update wavefunction visualization
     */
    updateWavefunctionVisualization(data) {
        if (!this.threeJsRenderer || data.wavefunctions.length === 0) return;

        const selectedStates = this.stateManager.getSelectedStates();
        const waveData = data.wavefunctions[selectedStates[0]];

        if (!waveData) return;

        const geometry = new THREE.BufferGeometry();
        const positions = [];
        const colors = [];

        const x = data.grid.x;
        const psi = waveData.psi;

        for (let i = 0; i < x.length; i++) {
            positions.push(
                x[i] / (data.grid.x_max - data.grid.x_min) * 2 - 1,
                psi[i],
                0
            );

            // Color based on value
            const intensity = Math.abs(psi[i]);
            colors.push(
                Math.sin(i * Math.PI / x.length),
                Math.cos(i * Math.PI / x.length),
                intensity
            );
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(
            new Float32Array(positions), 3
        ));
        geometry.setAttribute('color', new THREE.BufferAttribute(
            new Float32Array(colors), 3
        ));

        const material = new THREE.LineBasicMaterial({
            vertexColors: true,
            linewidth: 2
        });

        if (this.threeJsRenderer.mesh) {
            this.threeJsRenderer.scene.remove(this.threeJsRenderer.mesh);
        }

        this.threeJsRenderer.mesh = new THREE.Line(geometry, material);
        this.threeJsRenderer.scene.add(this.threeJsRenderer.mesh);
    }

    /**
     * Update statistics display
     */
    updateStatistics(stats = null) {
        const simType = this.stateManager.getCurrentSimulation();
        const data = this.stateManager.getSimulationData(simType);
        
        if (!data || !data.statistics) return;

        const statsPanel = document.getElementById('statisticsPanel');
        statsPanel.innerHTML = '';

        data.statistics.forEach((stat, i) => {
            const row = document.createElement('div');
            row.className = 'stat-row';
            row.innerHTML = `
                <span class="stat-label">State ${stat.state}:</span>
                <span>⟨x⟩=${stat.expectation_x?.toFixed(3)} | Δx=${stat.uncertainty_x?.toFixed(3)}</span>
            `;
            statsPanel.appendChild(row);
        });
    }

    /**
     * Handle energy update from WebSocket
     */
    handleEnergyUpdate(data) {
        if (this.visualizers.energyLevels) {
            this.visualizers.energyLevels.setEnergyData(data.energies);
            this.visualizers.energyLevels.render();
        }
    }

    /**
     * Handle probability update from WebSocket
     */
    handleProbabilityUpdate(data) {
        if (this.visualizers.probability) {
            // Would update with new probability data
        }
    }

    /**
     * Show comparison plot (numerical vs analytical)
     */
    showComparisonPlot() {
        const simType = this.stateManager.getCurrentSimulation();
        const data = this.stateManager.getSimulationData(simType);

        if (!data || !data.analytical_comparison) {
            this.showError('No analytical data available for this simulation');
            return;
        }

        const canvas = document.getElementById('detailedCanvas');
        const ctx = canvas.getContext('2d');

        // Draw comparison bar chart
        const comparisons = data.analytical_comparison;
        const width = canvas.width;
        const height = canvas.height;
        const barWidth = width / (comparisons.length * 2.5);
        const maxError = Math.max(...comparisons.map(c => c.error));

        ctx.fillStyle = '#0a0a0a';
        ctx.fillRect(0, 0, width, height);

        comparisons.forEach((comp, i) => {
            const x = 50 + i * (barWidth * 2);
            const numHeight = (comp.numerical_energy / maxError) * (height - 100);
            const anaHeight = (comp.analytical_energy / maxError) * (height - 100);

            // Numerical bar
            ctx.fillStyle = '#00ff88';
            ctx.fillRect(x, height - 50 - numHeight, barWidth * 0.4, numHeight);

            // Analytical bar
            ctx.fillStyle = '#ff00ff';
            ctx.fillRect(x + barWidth * 0.5, height - 50 - anaHeight, barWidth * 0.4, anaHeight);

            // Label
            ctx.fillStyle = '#ffffff';
            ctx.font = '10px monospace';
            ctx.textAlign = 'center';
            ctx.fillText(`E_${comp.state}`, x + barWidth * 0.45, height - 20);
        });

        document.getElementById('detailedSection').classList.add('active');
    }

    /**
     * Show trajectory plot (time evolution)
     */
    showTrajectoryPlot() {
        const simType = this.stateManager.getCurrentSimulation();
        const data = this.stateManager.getSimulationData(simType);

        if (simType !== 'tunneling' || !data.trajectory) {
            this.showError('Trajectory data only available for tunneling simulation');
            return;
        }

        const canvas = document.getElementById('detailedCanvas');
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#0a0a0a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Would draw trajectory animation here
        ctx.fillStyle = '#00ff88';
        ctx.font = '12px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('Time Evolution Visualization', canvas.width / 2, canvas.height / 2);

        document.getElementById('detailedSection').classList.add('active');
    }

    /**
     * Register webhook
     */
    async registerWebhook() {
        const url = document.getElementById('webhookUrl').value;
        const event = document.getElementById('webhookEvent').value;

        if (!url) {
            this.showError('Please enter a webhook URL');
            return;
        }

        try {
            await this.api.registerWebhook(event, url);
            this.stateManager.addWebhookSubscription({
                event_type: event,
                webhook_url: url
            });
            document.getElementById('webhookUrl').value = '';
            this.updateWebhookList();
            this.showSuccess('Webhook registered');
        } catch (error) {
            this.showError('Failed to register webhook: ' + error.message);
        }
    }

    /**
     * Update webhook list display
     */
    updateWebhookList() {
        const webhooks = this.stateManager.getWebhooks();
        const list = document.getElementById('webhookList');
        list.innerHTML = '';

        webhooks.forEach(hook => {
            const item = document.createElement('div');
            item.className = 'webhook-item';
            item.innerHTML = `
                <span>${hook.event_type}</span>
                <button class="btn-remove" onclick="dashboard.removeWebhook('${hook.webhook_url}')">✕</button>
            `;
            list.appendChild(item);
        });
    }

    /**
     * Remove webhook
     */
    async removeWebhook(url) {
        try {
            await this.api.unregisterWebhook('', url);
            this.stateManager.removeWebhookSubscription(url);
            this.updateWebhookList();
        } catch (error) {
            this.showError('Failed to remove webhook');
        }
    }

    /**
     * Update UI elements
     */
    onParametersChanged(data) {
        // Parameters changed in state
    }

    onDataUpdated(data) {
        this.updateVisualization();
    }

    onLoadingChanged(data) {
        const button = document.getElementById('runSimulation');
        button.disabled = data.loading;
        button.textContent = data.loading ? '⏳ Running...' : '▶ Run Simulation';
    }

    onSimulationChanged(data) {
        // Simulation type changed
    }

    updateConnectionStatus(connected) {
        // Update connection status indicator
    }

    onWindowResize() {
        // Resize all canvases
        Object.values(this.visualizers).forEach(viz => {
            const canvas = viz.canvas;
            if (canvas) {
                viz.resize(canvas.offsetWidth, canvas.offsetHeight);
            }
        });
    }

    /**
     * UI Helper Methods
     */
    updateStatus(message) {
        document.getElementById('status').textContent = message;
    }

    showError(message) {
        this.updateStatus('⚠️ ' + message);
        console.error(message);
    }

    showSuccess(message) {
        this.updateStatus('✓ ' + message);
        console.log(message);
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new QuantumDashboard();
    console.log('[Dashboard] Initialized');
});
