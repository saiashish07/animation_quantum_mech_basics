/**
 * API Service - Handles all backend communication
 * Provides unified interface for quantum simulations with caching and error handling
 */

class QuantumAPIService {
    constructor(apiBaseUrl = 'http://localhost:5000') {
        // Base URL should NOT include /api - endpoints already include it
        this.baseUrl = apiBaseUrl;
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
        this.requestTimeout = 30000; // 30 seconds
        this.retryAttempts = 3;
        this.retryDelay = 1000;
        
        console.log('[QuantumAPIService] Initialized with base URL:', this.baseUrl);
    }

    /**
     * Health check
     */
    async healthCheck() {
        return this.get('/api/health', { cache: false });
    }

    /**
     * Run full simulation with all visualization data
     */
    async fullSimulation(simulationType, parameters = {}) {
        const url = '/api/full-simulation';
        const payload = {
            type: simulationType,
            parameters
        };
        
        try {
            const response = await this.post(url, payload, { cache: false });
            return {
                success: true,
                data: response
            };
        } catch (error) {
            console.error('Simulation error:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Infinite well simulation
     */
    async infiniteWell(width, numStates = 5) {
        return this.fullSimulation('infinite-well', {
            width: parseFloat(width),
            num_states: parseInt(numStates)
        });
    }

    /**
     * Finite well simulation
     */
    async finiteWell(width, height, numStates = 5) {
        return this.fullSimulation('finite-well', {
            width: parseFloat(width),
            height: parseFloat(height),
            num_states: parseInt(numStates)
        });
    }

    /**
     * Tunneling simulation
     */
    async tunneling(barrierHeight, barrierWidth, particleEnergy, 
                   packetSigma = 0.5, duration = 1000) {
        return this.fullSimulation('tunneling', {
            barrier_height: parseFloat(barrierHeight),
            barrier_width: parseFloat(barrierWidth),
            particle_energy: parseFloat(particleEnergy),
            packet_sigma: parseFloat(packetSigma),
            duration: parseInt(duration)
        });
    }

    /**
     * Harmonic oscillator simulation
     */
    async harmonicOscillator(mass = 1.0, omega = 1.0, numStates = 5) {
        return this.fullSimulation('harmonic', {
            mass: parseFloat(mass),
            omega: parseFloat(omega),
            num_states: parseInt(numStates)
        });
    }

    // ========================================================================
    // WEBHOOK API
    // ========================================================================

    /**
     * Register webhook
     */
    async registerWebhook(eventType, webhookUrl, metadata = {}) {
        return this.post('/api/webhooks/register', {
            event_type: eventType,
            webhook_url: webhookUrl,
            metadata
        });
    }

    /**
     * Unregister webhook
     */
    async unregisterWebhook(eventType, webhookUrl) {
        return this.post('/api/webhooks/unregister', {
            event_type: eventType,
            webhook_url: webhookUrl
        });
    }

    /**
     * List all webhooks
     */
    async listWebhooks() {
        return this.get('/api/webhooks/list');
    }

    /**
     * Get webhook status
     */
    async getWebhookStatus() {
        return this.get('/api/webhooks/status');
    }

    // ========================================================================
    // LOW-LEVEL HTTP METHODS
    // ========================================================================

    /**
     * GET request with retry logic
     */
    async get(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        
        if (options.cache !== false) {
            const cached = this.getCache(url);
            if (cached) return cached;
        }

        for (let attempt = 0; attempt < this.retryAttempts; attempt++) {
            try {
                const response = await fetch(url, {
                    method: 'GET',
                    headers: this.getHeaders(),
                    signal: AbortSignal.timeout(this.requestTimeout)
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();
                
                if (options.cache !== false) {
                    this.setCache(url, data);
                }
                
                console.log('[API GET]', endpoint, data);
                return data;

            } catch (error) {
                console.warn(`[API GET] Attempt ${attempt + 1}/${this.retryAttempts} failed for ${endpoint}:`, error.message);
                if (attempt === this.retryAttempts - 1) {
                    throw new Error(`GET ${endpoint} failed after ${this.retryAttempts} attempts: ${error.message}`);
                }
                await this.delay(this.retryDelay * (attempt + 1));
            }
        }
    }

    /**
     * POST request with retry logic
     */
    async post(endpoint, data = {}, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        
        for (let attempt = 0; attempt < this.retryAttempts; attempt++) {
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: this.getHeaders(),
                    body: JSON.stringify(data),
                    signal: AbortSignal.timeout(this.requestTimeout)
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`HTTP ${response.status}: ${errorText}`);
                }

                const result = await response.json();
                console.log('[API POST]', endpoint, result);
                return result;

            } catch (error) {
                console.warn(`[API POST] Attempt ${attempt + 1}/${this.retryAttempts} failed for ${endpoint}:`, error.message);
                if (attempt === this.retryAttempts - 1) {
                    throw new Error(`POST ${endpoint} failed after ${this.retryAttempts} attempts: ${error.message}`);
                }
                await this.delay(this.retryDelay * (attempt + 1));
            }
        }
    }

    /**
     * GET request headers
     */
    getHeaders() {
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };
    }

    /**
     * Delay utility for retries
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // ========================================================================
    // CACHING
    // ========================================================================

    /**
     * Get cached data
     */
    getCache(key) {
        const cached = this.cache.get(key);
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            console.log(`[Cache Hit] ${key}`);
            return cached.data;
        }
        if (cached) {
            this.cache.delete(key);
        }
        return null;
    }

    /**
     * Set cache
     */
    setCache(key, data) {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
    }

    /**
     * Clear specific cache entry
     */
    clearCacheEntry(key) {
        this.cache.delete(key);
    }
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuantumAPIService;
}
