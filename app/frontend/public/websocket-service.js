/**
 * WebSocket Service - Real-time communication with backend
 * Handles subscriptions, live updates, and event streaming
 */

class QuantumWebSocketService {
    constructor(baseUrl = 'http://localhost:5000', options = {}) {
        this.baseUrl = baseUrl;
        this.socket = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        
        // Event handlers
        this.eventHandlers = {
            connect: [],
            disconnect: [],
            error: [],
            energy_update: [],
            probability_update: [],
            wavefunction_update: [],
            statistics_update: [],
            simulation_complete: [],
            subscribed: [],
            unsubscribed: []
        };

        // Active subscriptions
        this.activeSubscriptions = new Set();

        // Auto-connect
        if (options.autoConnect !== false) {
            this.connect();
        }
    }

    /**
     * Connect to WebSocket server
     */
    connect() {
        if (this.socket && this.isConnected) {
            console.log('[WebSocket] Already connected');
            return;
        }

        try {
            // Try to load Socket.IO library if available
            if (typeof io === 'undefined') {
                console.warn('[WebSocket] Socket.IO not loaded. Install: <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>');
                this.setupFallback();
                return;
            }

            this.socket = io(this.baseUrl, {
                reconnection: true,
                reconnectionDelay: this.reconnectDelay,
                reconnectionDelayMax: 5000,
                reconnectionAttempts: this.maxReconnectAttempts
            });

            this.setupEventHandlers();
            console.log('[WebSocket] Connecting...');

        } catch (error) {
            console.error('[WebSocket] Connection error:', error);
            this.setupFallback();
        }
    }

    /**
     * Setup core event handlers
     */
    setupEventHandlers() {
        this.socket.on('connect', () => {
            console.log('[WebSocket] Connected');
            this.isConnected = true;
            this.reconnectAttempts = 0;
            this.emit('connect', { clientId: this.socket.id });
        });

        this.socket.on('disconnect', () => {
            console.log('[WebSocket] Disconnected');
            this.isConnected = false;
            this.emit('disconnect');
        });

        this.socket.on('error', (error) => {
            console.error('[WebSocket] Error:', error);
            this.emit('error', error);
        });

        // Simulation events
        this.socket.on('energy_update', (data) => {
            this.emit('energy_update', data);
        });

        this.socket.on('probability_update', (data) => {
            this.emit('probability_update', data);
        });

        this.socket.on('wavefunction_update', (data) => {
            this.emit('wavefunction_update', data);
        });

        this.socket.on('statistics_update', (data) => {
            this.emit('statistics_update', data);
        });

        this.socket.on('simulation_complete', (data) => {
            this.emit('simulation_complete', data);
        });

        // Subscription events
        this.socket.on('subscribed', (data) => {
            this.emit('subscribed', data);
        });

        this.socket.on('unsubscribed', (data) => {
            this.emit('unsubscribed', data);
        });
    }

    /**
     * Fallback for when Socket.IO is not available
     */
    setupFallback() {
        console.log('[WebSocket] Using polling fallback');
        // Could implement polling-based updates here
    }

    /**
     * Subscribe to simulation room for live updates
     */
    subscribe(room) {
        if (!this.isConnected) {
            console.warn('[WebSocket] Not connected');
            return;
        }

        if (!this.activeSubscriptions.has(room)) {
            this.socket.emit('subscribe', { room });
            this.activeSubscriptions.add(room);
            console.log(`[WebSocket] Subscribed to room: ${room}`);
        }
    }

    /**
     * Unsubscribe from room
     */
    unsubscribe(room) {
        if (!this.isConnected) return;

        this.socket.emit('unsubscribe', { room });
        this.activeSubscriptions.delete(room);
        console.log(`[WebSocket] Unsubscribed from room: ${room}`);
    }

    /**
     * Request live streaming updates
     */
    requestLiveUpdate(simulationType, parameters = {}, room = null) {
        if (!this.isConnected) {
            console.warn('[WebSocket] Not connected');
            return;
        }

        const roomId = room || simulationType;
        this.subscribe(roomId);

        this.socket.emit('request_live_update', {
            simulation_type: simulationType,
            parameters,
            room: roomId
        });

        console.log(`[WebSocket] Requested live updates for ${simulationType}`);
    }

    /**
     * Register event handler
     */
    on(event, handler) {
        if (event in this.eventHandlers) {
            this.eventHandlers[event].push(handler);
        } else {
            console.warn(`[WebSocket] Unknown event: ${event}`);
        }
    }

    /**
     * Unregister event handler
     */
    off(event, handler) {
        if (event in this.eventHandlers) {
            this.eventHandlers[event] = this.eventHandlers[event].filter(h => h !== handler);
        }
    }

    /**
     * Emit event to handlers
     */
    emit(event, data) {
        if (event in this.eventHandlers) {
            this.eventHandlers[event].forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error(`[WebSocket] Event handler error for ${event}:`, error);
                }
            });
        }
    }

    /**
     * Get connection status
     */
    getStatus() {
        return {
            isConnected: this.isConnected,
            socketId: this.socket ? this.socket.id : null,
            activeSubscriptions: Array.from(this.activeSubscriptions),
            reconnectAttempts: this.reconnectAttempts
        };
    }

    /**
     * Disconnect
     */
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.isConnected = false;
            console.log('[WebSocket] Disconnected');
        }
    }

    /**
     * Reconnect
     */
    reconnect() {
        this.disconnect();
        this.connect();
    }

    /**
     * Get active subscriptions
     */
    getSubscriptions() {
        return Array.from(this.activeSubscriptions);
    }

    /**
     * Unsubscribe from all
     */
    unsubscribeAll() {
        this.activeSubscriptions.forEach(room => this.unsubscribe(room));
        this.activeSubscriptions.clear();
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuantumWebSocketService;
}
