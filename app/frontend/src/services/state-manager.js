/**
 * State Manager - Centralized state management for all simulations
 * Handles parameter storage, computation results, and UI synchronization
 */

class QuantumStateManager {
    constructor() {
        this.state = {
            // Simulation parameters
            simulations: {
                'infinite-well': {
                    parameters: { width: 5.0, num_states: 5 },
                    data: null,
                    loading: false,
                    error: null,
                    lastUpdated: null
                },
                'finite-well': {
                    parameters: { width: 5.0, height: 50.0, num_states: 5 },
                    data: null,
                    loading: false,
                    error: null,
                    lastUpdated: null
                },
                'tunneling': {
                    parameters: {
                        barrier_height: 30.0,
                        barrier_width: 2.0,
                        particle_energy: 20.0,
                        packet_sigma: 0.5,
                        duration: 1000
                    },
                    data: null,
                    loading: false,
                    error: null,
                    lastUpdated: null
                },
                'harmonic': {
                    parameters: { mass: 1.0, omega: 1.0, num_states: 5 },
                    data: null,
                    loading: false,
                    error: null,
                    lastUpdated: null
                }
            },

            // UI state
            ui: {
                currentSimulation: 'infinite-well',
                selectedStates: [0],
                displayMode: 'wavefunction', // wavefunction, probability, energy-levels
                graphTypes: {
                    energy: true,
                    probability: true,
                    wavefunction: true,
                    statistics: true,
                    comparison: true
                },
                zoomLevel: 1.0
            },

            // WebSocket state
            websocket: {
                connected: false,
                subscriptions: [],
                clientId: null,
                liveUpdatesEnabled: false
            },

            // Webhook state
            webhooks: {
                registered: [],
                events: []
            }
        };

        // State observers
        this.observers = [];
    }

    /**
     * Get full state
     */
    getState() {
        return JSON.parse(JSON.stringify(this.state));
    }

    /**
     * Update simulation parameters
     */
    updateSimulationParameters(simType, parameters) {
        if (simType in this.state.simulations) {
            this.state.simulations[simType].parameters = {
                ...this.state.simulations[simType].parameters,
                ...parameters
            };
            this.notifyObservers('parameters-changed', { simType, parameters });
            return true;
        }
        return false;
    }

    /**
     * Get simulation parameters
     */
    getSimulationParameters(simType) {
        if (simType in this.state.simulations) {
            return this.state.simulations[simType].parameters;
        }
        return null;
    }

    /**
     * Set simulation data (result from API)
     */
    setSimulationData(simType, data) {
        if (simType in this.state.simulations) {
            this.state.simulations[simType].data = data;
            this.state.simulations[simType].lastUpdated = new Date().toISOString();
            this.state.simulations[simType].error = null;
            this.notifyObservers('data-updated', { simType, data });
            return true;
        }
        return false;
    }

    /**
     * Get simulation data
     */
    getSimulationData(simType) {
        if (simType in this.state.simulations) {
            return this.state.simulations[simType].data;
        }
        return null;
    }

    /**
     * Set loading state
     */
    setLoading(simType, loading) {
        if (simType in this.state.simulations) {
            this.state.simulations[simType].loading = loading;
            this.notifyObservers('loading-changed', { simType, loading });
        }
    }

    /**
     * Set error state
     */
    setError(simType, error) {
        if (simType in this.state.simulations) {
            this.state.simulations[simType].error = error;
            this.notifyObservers('error-changed', { simType, error });
        }
    }

    /**
     * Get error state
     */
    getError(simType) {
        if (simType in this.state.simulations) {
            return this.state.simulations[simType].error;
        }
        return null;
    }

    /**
     * Set current simulation
     */
    setCurrentSimulation(simType) {
        if (simType in this.state.simulations) {
            this.state.ui.currentSimulation = simType;
            this.notifyObservers('simulation-changed', { simType });
            return true;
        }
        return false;
    }

    /**
     * Get current simulation
     */
    getCurrentSimulation() {
        return this.state.ui.currentSimulation;
    }

    /**
     * Set selected states for display
     */
    setSelectedStates(stateIndices) {
        this.state.ui.selectedStates = Array.isArray(stateIndices) ? 
            stateIndices : [stateIndices];
        this.notifyObservers('selected-states-changed', { states: stateIndices });
    }

    /**
     * Get selected states
     */
    getSelectedStates() {
        return this.state.ui.selectedStates;
    }

    /**
     * Toggle state selection
     */
    toggleStateSelection(stateIndex) {
        if (this.state.ui.selectedStates.includes(stateIndex)) {
            this.state.ui.selectedStates = this.state.ui.selectedStates.filter(
                s => s !== stateIndex
            );
        } else {
            this.state.ui.selectedStates.push(stateIndex);
        }
        this.notifyObservers('selected-states-changed', {
            states: this.state.ui.selectedStates
        });
    }

    /**
     * Set display mode
     */
    setDisplayMode(mode) {
        const validModes = ['wavefunction', 'probability', 'energy-levels', 'statistics'];
        if (validModes.includes(mode)) {
            this.state.ui.displayMode = mode;
            this.notifyObservers('display-mode-changed', { mode });
            return true;
        }
        return false;
    }

    /**
     * Get display mode
     */
    getDisplayMode() {
        return this.state.ui.displayMode;
    }

    /**
     * Toggle graph type visibility
     */
    toggleGraphType(graphType) {
        if (graphType in this.state.ui.graphTypes) {
            this.state.ui.graphTypes[graphType] = !this.state.ui.graphTypes[graphType];
            this.notifyObservers('graph-visibility-changed', {
                graphType,
                visible: this.state.ui.graphTypes[graphType]
            });
            return true;
        }
        return false;
    }

    /**
     * Get graph types visibility
     */
    getGraphTypes() {
        return this.state.ui.graphTypes;
    }

    /**
     * Update WebSocket status
     */
    updateWebSocketStatus(status) {
        this.state.websocket = {
            ...this.state.websocket,
            ...status
        };
        this.notifyObservers('websocket-status-changed', status);
    }

    /**
     * Add webhook subscription
     */
    addWebhookSubscription(hook) {
        this.state.webhooks.registered.push(hook);
        this.notifyObservers('webhook-added', { hook });
    }

    /**
     * Remove webhook subscription
     */
    removeWebhookSubscription(webhookUrl) {
        this.state.webhooks.registered = this.state.webhooks.registered.filter(
            h => h.webhook_url !== webhookUrl
        );
        this.notifyObservers('webhook-removed', { webhookUrl });
    }

    /**
     * Get webhook subscriptions
     */
    getWebhooks() {
        return this.state.webhooks.registered;
    }

    /**
     * Log webhook event
     */
    logWebhookEvent(event) {
        this.state.webhooks.events.push({
            ...event,
            timestamp: new Date().toISOString()
        });
        
        // Keep last 100 events
        if (this.state.webhooks.events.length > 100) {
            this.state.webhooks.events = this.state.webhooks.events.slice(-100);
        }
        
        this.notifyObservers('webhook-event', event);
    }

    /**
     * Get webhook events
     */
    getWebhookEvents(limit = 50) {
        return this.state.webhooks.events.slice(-limit);
    }

    /**
     * Subscribe to state changes
     */
    subscribe(observer) {
        this.observers.push(observer);
        return () => {
            this.observers = this.observers.filter(o => o !== observer);
        };
    }

    /**
     * Notify all observers
     */
    notifyObservers(action, data) {
        this.observers.forEach(observer => {
            try {
                observer(action, data, this.state);
            } catch (error) {
                console.error('Observer error:', error);
            }
        });
    }

    /**
     * Get simulation statistics summary
     */
    getSimulationSummary(simType) {
        const sim = this.state.simulations[simType];
        if (!sim || !sim.data) {
            return null;
        }

        return {
            simulationType: simType,
            timestamp: sim.lastUpdated,
            parameters: sim.parameters,
            energies: sim.data.energy_levels?.values || [],
            numStates: (sim.data.energy_levels?.values || []).length,
            groundStateEnergy: sim.data.energy_levels?.ground_state || null
        };
    }

    /**
     * Clear all data
     */
    clearAllData() {
        Object.keys(this.state.simulations).forEach(simType => {
            this.state.simulations[simType].data = null;
            this.state.simulations[simType].error = null;
        });
        this.notifyObservers('all-data-cleared', {});
    }

    /**
     * Reset to initial state
     */
    reset() {
        this.state = new QuantumStateManager().state;
        this.notifyObservers('reset', {});
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuantumStateManager;
}
