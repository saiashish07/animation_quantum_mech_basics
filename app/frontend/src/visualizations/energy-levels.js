/**
 * Energy Level Visualizer
 * Displays energy levels as horizontal lines with labels and statistics
 */

class EnergyLevelsVisualizer {
    constructor(canvas, options = {}) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;
        
        // Configuration
        this.options = {
            padding: options.padding || 60,
            lineHeight: options.lineHeight || 60,
            colors: options.colors || this.getDefaultColors(),
            fontSize: options.fontSize || 12,
            showAnalytical: options.showAnalytical !== false,
            showError: options.showError !== false,
            ...options
        };

        this.energies = [];
        this.analyticalEnergies = [];
        this.labels = [];
        this.errors = [];
        this.potentialHeight = 0;
    }

    /**
     * Get default color palette
     */
    getDefaultColors() {
        return {
            line: '#00ff88',
            analytical: '#ff00ff',
            selected: '#ffff00',
            text: '#ffffff',
            grid: '#333333',
            background: '#0a0a0a',
            error: '#ff4444'
        };
    }

    /**
     * Set energy data
     */
    setEnergyData(energies, options = {}) {
        this.energies = Array.isArray(energies) ? energies : [];
        this.analyticalEnergies = Array.isArray(options.analytical) ? 
            options.analytical : [];
        this.labels = Array.isArray(options.labels) ? 
            options.labels : this.energies.map((_, i) => `E_${i}`);
        this.errors = Array.isArray(options.errors) ? 
            options.errors : [];
        this.potentialHeight = options.potentialHeight || Math.max(...this.energies) * 1.2;
        this.selectedStates = options.selectedStates || [];
    }

    /**
     * Render energy levels
     */
    render() {
        // Clear canvas
        this.ctx.fillStyle = this.options.colors.background;
        this.ctx.fillRect(0, 0, this.width, this.height);

        // Draw axes
        this.drawAxes();

        // Draw potential well boundaries if provided
        if (this.options.wellBoundaries) {
            this.drawWellBoundaries();
        }

        // Draw grid
        this.drawGrid();

        // Draw energy levels
        this.drawEnergyLevels();

        // Draw legend
        this.drawLegend();

        // Draw statistics
        if (this.options.showStats) {
            this.drawStatistics();
        }
    }

    /**
     * Draw coordinate axes
     */
    drawAxes() {
        const { padding } = this.options;
        const colors = this.options.colors;

        this.ctx.strokeStyle = colors.grid;
        this.ctx.lineWidth = 1;

        // Y-axis
        this.ctx.beginPath();
        this.ctx.moveTo(padding, this.height - padding);
        this.ctx.lineTo(padding, padding);
        this.ctx.stroke();

        // X-axis
        this.ctx.beginPath();
        this.ctx.moveTo(padding, this.height - padding);
        this.ctx.lineTo(this.width - padding, this.height - padding);
        this.ctx.stroke();

        // Labels
        this.ctx.fillStyle = colors.text;
        this.ctx.font = `${this.options.fontSize}px monospace`;
        this.ctx.textAlign = 'right';
        this.ctx.fillText('Energy (E)', padding - 10, padding - 10);
        this.ctx.textAlign = 'center';
        this.ctx.fillText('State', this.width - padding + 20, this.height - padding + 20);
    }

    /**
     * Draw grid lines
     */
    drawGrid() {
        const { padding } = this.options;
        const colors = this.options.colors;
        const plotHeight = this.height - 2 * padding;
        const plotWidth = this.width - 2 * padding;

        this.ctx.strokeStyle = colors.grid;
        this.ctx.lineWidth = 0.5;
        this.ctx.globalAlpha = 0.3;

        // Horizontal grid lines
        const numHLines = 5;
        for (let i = 0; i <= numHLines; i++) {
            const y = this.height - padding - (plotHeight * i / numHLines);
            this.ctx.beginPath();
            this.ctx.moveTo(padding, y);
            this.ctx.lineTo(this.width - padding, y);
            this.ctx.stroke();
        }

        // Vertical grid lines
        const numVLines = Math.max(this.energies.length, 1);
        for (let i = 0; i <= numVLines; i++) {
            const x = padding + (plotWidth * i / numVLines);
            this.ctx.beginPath();
            this.ctx.moveTo(x, padding);
            this.ctx.lineTo(x, this.height - padding);
            this.ctx.stroke();
        }

        this.ctx.globalAlpha = 1.0;
    }

    /**
     * Draw energy level lines
     */
    drawEnergyLevels() {
        const { padding, showAnalytical, showError } = this.options;
        const colors = this.options.colors;
        const plotHeight = this.height - 2 * padding;
        const plotWidth = this.width - 2 * padding;
        const numStates = this.energies.length;

        if (numStates === 0) return;

        // Normalize energies for display
        const minE = Math.min(...this.energies);
        const maxE = Math.max(...this.energies);
        const energyRange = Math.max(maxE - minE, 1e-6);

        this.ctx.font = `${this.options.fontSize}px monospace`;
        this.ctx.textAlign = 'center';

        for (let i = 0; i < numStates; i++) {
            const x = padding + (plotWidth * (i + 0.5) / numStates);
            const yNorm = (this.energies[i] - minE) / energyRange;
            const y = this.height - padding - (plotHeight * yNorm);

            const isSelected = this.selectedStates.includes(i);
            const color = isSelected ? colors.selected : colors.line;

            // Draw energy level line
            this.ctx.strokeStyle = color;
            this.ctx.lineWidth = isSelected ? 3 : 2;
            this.ctx.beginPath();
            this.ctx.moveTo(padding, y);
            this.ctx.lineTo(this.width - padding, y);
            this.ctx.stroke();

            // Draw numerical value label
            this.ctx.fillStyle = color;
            this.ctx.fillText(
                `${this.labels[i]}: ${this.energies[i].toFixed(3)}`,
                x,
                y - 10
            );

            // Draw analytical comparison if available
            if (showAnalytical && this.analyticalEnergies[i] !== undefined) {
                const yAnalytical = this.height - padding - 
                    (plotHeight * (this.analyticalEnergies[i] - minE) / energyRange);
                
                this.ctx.strokeStyle = colors.analytical;
                this.ctx.lineWidth = 1;
                this.ctx.setLineDash([5, 5]);
                this.ctx.beginPath();
                this.ctx.moveTo(padding, yAnalytical);
                this.ctx.lineTo(this.width - padding, yAnalytical);
                this.ctx.stroke();
                this.ctx.setLineDash([]);

                // Draw error indicator if available
                if (showError && this.errors[i] !== undefined) {
                    const errorPercent = this.errors[i];
                    this.ctx.fillStyle = colors.error;
                    this.ctx.font = `${this.options.fontSize - 2}px monospace`;
                    this.ctx.fillText(
                        `Err: ${errorPercent.toFixed(2)}%`,
                        x,
                        y + 15
                    );
                    this.ctx.font = `${this.options.fontSize}px monospace`;
                }
            }
        }
    }

    /**
     * Draw well boundaries
     */
    drawWellBoundaries() {
        const { padding } = this.options;
        const colors = this.options.colors;
        const { left, right } = this.options.wellBoundaries;

        this.ctx.fillStyle = colors.background;
        this.ctx.globalAlpha = 0.2;

        // Left boundary
        if (left !== undefined) {
            this.ctx.fillRect(0, 0, left, this.height);
        }

        // Right boundary
        if (right !== undefined) {
            this.ctx.fillRect(right, 0, this.width - right, this.height);
        }

        this.ctx.globalAlpha = 1.0;
    }

    /**
     * Draw legend
     */
    drawLegend() {
        const colors = this.options.colors;
        const legendX = this.width - 200;
        const legendY = this.options.padding;

        this.ctx.fillStyle = colors.background;
        this.ctx.globalAlpha = 0.8;
        this.ctx.fillRect(legendX - 10, legendY - 10, 200, 80);
        this.ctx.globalAlpha = 1.0;

        this.ctx.font = `${this.options.fontSize}px monospace`;
        this.ctx.fillStyle = colors.text;

        let y = legendY + 10;
        const lineHeight = 18;

        // Numerical line
        this.ctx.strokeStyle = colors.line;
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(legendX, y);
        this.ctx.lineTo(legendX + 30, y);
        this.ctx.stroke();
        this.ctx.textAlign = 'left';
        this.ctx.fillText('Numerical', legendX + 40, y + 5);

        y += lineHeight;

        // Analytical line
        if (this.options.showAnalytical) {
            this.ctx.strokeStyle = colors.analytical;
            this.ctx.setLineDash([5, 5]);
            this.ctx.beginPath();
            this.ctx.moveTo(legendX, y);
            this.ctx.lineTo(legendX + 30, y);
            this.ctx.stroke();
            this.ctx.setLineDash([]);
            this.ctx.fillText('Analytical', legendX + 40, y + 5);
        }
    }

    /**
     * Draw energy statistics
     */
    drawStatistics() {
        if (this.energies.length === 0) return;

        const colors = this.options.colors;
        const padding = this.options.padding;

        // Calculate statistics
        const groundState = Math.min(...this.energies);
        const maxEnergy = Math.max(...this.energies);
        const energySpacing = this.energies.length > 1 ?
            (this.energies[1] - this.energies[0]) : 0;

        const stats = [
            `Ground state: ${groundState.toFixed(3)}`,
            `Max energy: ${maxEnergy.toFixed(3)}`,
            `Spacing: ${energySpacing.toFixed(3)}`,
            `States: ${this.energies.length}`
        ];

        // Draw stats box
        const statsX = padding;
        const statsY = this.height - padding + 40;
        const lineHeight = 18;

        this.ctx.fillStyle = colors.text;
        this.ctx.font = `${this.options.fontSize - 2}px monospace`;
        this.ctx.textAlign = 'left';

        stats.forEach((stat, i) => {
            this.ctx.fillText(stat, statsX, statsY + i * lineHeight);
        });
    }

    /**
     * Highlight state
     */
    highlightState(stateIndex) {
        this.selectedStates = [stateIndex];
        this.render();
    }

    /**
     * Get energy at position
     */
    getEnergyAtMouse(mouseX, mouseY) {
        const { padding } = this.options;
        const plotHeight = this.height - 2 * padding;
        const minE = Math.min(...this.energies);
        const maxE = Math.max(...this.energies);
        const energyRange = Math.max(maxE - minE, 1e-6);

        const yNorm = (this.height - padding - mouseY) / plotHeight;
        return minE + yNorm * energyRange;
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
    module.exports = EnergyLevelsVisualizer;
}
