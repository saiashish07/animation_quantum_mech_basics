/**
 * Probability Density Heatmap Visualizer
 * Displays |ψ|² as 2D heatmap or 3D surface using Canvas 2D
 */

class ProbabilityDensityVisualizer {
    constructor(canvas, options = {}) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;

        this.options = {
            padding: options.padding || 60,
            colorScheme: options.colorScheme || 'hot', // hot, cool, viridis
            showColorbar: options.showColorbar !== false,
            interpolation: options.interpolation || 'smooth',
            ...options
        };

        this.x = [];
        this.densities = []; // Array of density arrays for different states
        this.labels = [];
        this.imageData = null;
    }

    /**
     * Get color from value using colormap
     */
    getColor(value, min, max) {
        const normalized = Math.max(0, Math.min(1, (value - min) / (max - min + 1e-10)));
        
        let r, g, b;
        
        switch (this.options.colorScheme) {
            case 'hot':
                // Hot: black -> red -> yellow -> white
                if (normalized < 0.33) {
                    r = Math.round(normalized * 3 * 255);
                    g = 0;
                    b = 0;
                } else if (normalized < 0.67) {
                    r = 255;
                    g = Math.round((normalized - 0.33) * 3 * 255);
                    b = 0;
                } else {
                    r = 255;
                    g = 255;
                    b = Math.round((normalized - 0.67) * 3 * 255);
                }
                break;

            case 'cool':
                // Cool: blue -> cyan -> white
                r = Math.round(normalized * 255);
                g = Math.round(normalized * 255);
                b = 255;
                break;

            case 'viridis':
                // Viridis-like: purple -> cyan -> green -> yellow
                if (normalized < 0.25) {
                    r = Math.round(68 * (1 - normalized * 4));
                    g = 0;
                    b = Math.round(84 + 176 * normalized * 4);
                } else if (normalized < 0.5) {
                    r = 0;
                    g = Math.round(170 * (normalized - 0.25) * 4);
                    b = Math.round(84 + (117 - 84) * (normalized - 0.25) * 4);
                } else if (normalized < 0.75) {
                    r = Math.round(170 * (normalized - 0.5) * 4);
                    g = Math.round(170 + 40 * (normalized - 0.5) * 4);
                    b = Math.round(60 - 60 * (normalized - 0.5) * 4);
                } else {
                    r = Math.round(170 + 85 * (normalized - 0.75) * 4);
                    g = Math.round(210 + 45 * (normalized - 0.75) * 4);
                    b = 0;
                }
                break;

            default:
                r = g = b = Math.round(normalized * 255);
        }

        return `rgb(${Math.round(r)},${Math.round(g)},${Math.round(b)})`;
    }

    /**
     * Set probability density data
     */
    setProbabilityData(x, densities, options = {}) {
        this.x = x;
        this.densities = densities; // Array of probability density arrays
        this.labels = options.labels || densities.map((_, i) => `State ${i}`);
    }

    /**
     * Render heatmap
     */
    render() {
        if (this.densities.length === 0) return;

        // Clear canvas
        this.ctx.fillStyle = '#0a0a0a';
        this.ctx.fillRect(0, 0, this.width, this.height);

        // Draw heatmap
        this.drawHeatmap();

        // Draw axes and labels
        this.drawAxes();

        // Draw colorbar if enabled
        if (this.options.showColorbar) {
            this.drawColorbar();
        }
    }

    /**
     * Draw 2D heatmap
     */
    drawHeatmap() {
        const { padding } = this.options;
        const plotWidth = this.width - 2 * padding - 60; // Space for colorbar
        const plotHeight = this.height - 2 * padding;

        const numX = this.x.length;
        const numY = this.densities.length;

        if (numX === 0 || numY === 0) return;

        const cellWidth = plotWidth / numX;
        const cellHeight = plotHeight / numY;

        // Find min/max for normalization
        let min = Infinity, max = -Infinity;
        for (let density of this.densities) {
            for (let val of density) {
                min = Math.min(min, val);
                max = Math.max(max, val);
            }
        }
        min = max === min ? 0 : min;

        // Draw heatmap cells
        for (let yi = 0; yi < numY; yi++) {
            for (let xi = 0; xi < numX; xi++) {
                const value = this.densities[yi][xi] || 0;
                const x = padding + xi * cellWidth;
                const y = padding + yi * cellHeight;

                this.ctx.fillStyle = this.getColor(value, min, max);
                this.ctx.fillRect(x, y, cellWidth, cellHeight);

                // Draw cell border for clarity
                this.ctx.strokeStyle = 'rgba(255,255,255,0.1)';
                this.ctx.lineWidth = 0.5;
                this.ctx.strokeRect(x, y, cellWidth, cellHeight);
            }
        }

        // Draw y-axis state labels
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '12px monospace';
        this.ctx.textAlign = 'right';
        for (let i = 0; i < numY; i++) {
            const y = padding + i * cellHeight + cellHeight / 2;
            this.ctx.fillText(this.labels[i], padding - 10, y + 4);
        }
    }

    /**
     * Draw axes and labels
     */
    drawAxes() {
        const { padding } = this.options;
        const colors = {
            text: '#ffffff',
            grid: '#333333'
        };

        this.ctx.strokeStyle = colors.grid;
        this.ctx.lineWidth = 1;

        // Y-axis
        this.ctx.beginPath();
        this.ctx.moveTo(padding, padding);
        this.ctx.lineTo(padding, this.height - padding);
        this.ctx.stroke();

        // X-axis
        this.ctx.beginPath();
        this.ctx.moveTo(padding, this.height - padding);
        this.ctx.lineTo(this.width - padding - 60, this.height - padding);
        this.ctx.stroke();

        // Labels
        this.ctx.fillStyle = colors.text;
        this.ctx.font = '12px monospace';
        this.ctx.textAlign = 'center';
        
        // X-axis label
        this.ctx.save();
        this.ctx.translate(padding + (this.width - 2 * padding - 60) / 2, this.height - 20);
        this.ctx.fillText('Position (x)', 0, 0);
        this.ctx.restore();

        // Y-axis label
        this.ctx.save();
        this.ctx.translate(15, padding + (this.height - 2 * padding) / 2);
        this.ctx.rotate(-Math.PI / 2);
        this.ctx.textAlign = 'center';
        this.ctx.fillText('Quantum State', 0, 0);
        this.ctx.restore();
    }

    /**
     * Draw colorbar
     */
    drawColorbar() {
        const { padding } = this.options;
        const plotWidth = this.width - 2 * padding - 60;
        const plotHeight = this.height - 2 * padding;

        const colorbarX = padding + plotWidth + 20;
        const colorbarY = padding;
        const colorbarWidth = 20;
        const colorbarHeight = plotHeight;

        // Draw colorbar gradient
        for (let i = 0; i < colorbarHeight; i++) {
            const normalized = 1 - (i / colorbarHeight);
            const color = this.getColor(normalized, 0, 1);
            
            this.ctx.fillStyle = color;
            this.ctx.fillRect(colorbarX, colorbarY + i, colorbarWidth, 1);
        }

        // Draw colorbar border
        this.ctx.strokeStyle = '#666666';
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(colorbarX, colorbarY, colorbarWidth, colorbarHeight);

        // Find min/max
        let min = Infinity, max = -Infinity;
        for (let density of this.densities) {
            for (let val of density) {
                min = Math.min(min, val);
                max = Math.max(max, val);
            }
        }

        // Draw scale labels
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '10px monospace';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(max.toFixed(3), colorbarX + colorbarWidth + 5, colorbarY + 10);
        this.ctx.fillText(min.toFixed(3), colorbarX + colorbarWidth + 5, colorbarY + colorbarHeight - 5);
    }

    /**
     * Render single state as line plot
     */
    renderSingleState(stateIndex) {
        if (!this.densities[stateIndex]) return;

        const { padding } = this.options;
        const density = this.densities[stateIndex];

        // Clear
        this.ctx.fillStyle = '#0a0a0a';
        this.ctx.fillRect(0, 0, this.width, this.height);

        // Draw axes
        this.ctx.strokeStyle = '#333333';
        this.ctx.lineWidth = 1;
        
        // Y-axis
        this.ctx.beginPath();
        this.ctx.moveTo(padding, padding);
        this.ctx.lineTo(padding, this.height - padding);
        this.ctx.stroke();

        // X-axis
        this.ctx.beginPath();
        this.ctx.moveTo(padding, this.height - padding);
        this.ctx.lineTo(this.width - padding, this.height - padding);
        this.ctx.stroke();

        // Find min/max
        const min = Math.min(...density);
        const max = Math.max(...density);
        const range = Math.max(max - min, 1e-10);

        // Draw line plot
        this.ctx.strokeStyle = '#00ff88';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();

        for (let i = 0; i < density.length; i++) {
            const xNorm = i / (density.length - 1);
            const yNorm = (density[i] - min) / range;
            const x = padding + xNorm * (this.width - 2 * padding);
            const y = this.height - padding - yNorm * (this.height - 2 * padding);

            if (i === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
        }
        this.ctx.stroke();

        // Fill area under curve
        this.ctx.lineTo(this.width - padding, this.height - padding);
        this.ctx.lineTo(padding, this.height - padding);
        this.ctx.fillStyle = 'rgba(0, 255, 136, 0.2)';
        this.ctx.fill();

        // Title
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '14px monospace';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(
            `Probability Density: ${this.labels[stateIndex]}`,
            this.width / 2,
            padding - 10
        );
    }

    /**
     * Resize canvas
     */
    resize(width, height) {
        this.canvas.width = width;
        this.canvas.height = height;
        this.width = width;
        this.height = height;
        this.render();
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProbabilityDensityVisualizer;
}
