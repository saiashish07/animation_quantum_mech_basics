/**
 * Core WebGL Visualization System
 * Handles Three.js setup and common visualization utilities
 */

class QuantumVisualizerCore {
    constructor(canvas) {
        this.canvas = canvas;
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.animationId = null;
        this.plotObjects = {
            wavefunction: null,
            probability: null,
            potential: null,
            energyLevels: null
        };

        this.init();
        this.onWindowResize = this.onWindowResize.bind(this);
    }

    init() {
        // Scene setup
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0f172a);

        // Camera setup
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.canvas.clientWidth / this.canvas.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(0, 5, 15);
        this.camera.lookAt(0, 0, 0);

        // Renderer setup
        this.renderer = new THREE.WebGLRenderer({ 
            canvas: this.canvas,
            antialias: true,
            alpha: true
        });
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        this.renderer.shadowMap.enabled = true;

        // Lighting
        this.setupLighting();

        // Grid
        this.addGrid();

        // Event listeners
        window.addEventListener('resize', this.onWindowResize);

        // Start animation loop
        this.animate();
    }

    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(ambientLight);

        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 10);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        this.scene.add(directionalLight);

        // Point light for accent
        const pointLight = new THREE.PointLight(0x0ea5e9, 0.3);
        pointLight.position.set(-10, 5, 10);
        this.scene.add(pointLight);
    }

    addGrid() {
        const gridSize = 20;
        const gridDivisions = 20;
        const gridHelper = new THREE.GridHelper(gridSize, gridDivisions, 0x444444, 0x222222);
        gridHelper.position.y = -2;
        this.scene.add(gridHelper);
    }

    /**
     * Plot wavefunction and probability density
     */
    plotWavefunction(x, psi, potential = null, energyLevels = null, options = {}) {
        // Clear previous plots
        if (this.plotObjects.wavefunction) {
            this.scene.remove(this.plotObjects.wavefunction);
        }
        if (this.plotObjects.probability) {
            this.scene.remove(this.plotObjects.probability);
        }
        if (this.plotObjects.potential) {
            this.scene.remove(this.plotObjects.potential);
        }
        if (this.plotObjects.energyLevels) {
            this.scene.remove(this.plotObjects.energyLevels);
        }

        const defaults = {
            showWavefunction: true,
            showProbability: false,
            showPotential: true,
            showEnergyLevels: true,
            color: 0x0ea5e9,
            scale: 1.0
        };
        const settings = { ...defaults, ...options };

        // Normalize data for visualization
        const xMin = x[0];
        const xMax = x[x.length - 1];
        const xRange = xMax - xMin;

        // Plot wavefunction
        if (settings.showWavefunction && psi) {
            this.plotObjects.wavefunction = this.createLinePlot(
                x, psi, 0x0ea5e9, settings.scale
            );
            this.scene.add(this.plotObjects.wavefunction);
        }

        // Plot probability density
        if (settings.showProbability && psi) {
            const probDensity = psi.map(p => Math.abs(p) ** 2);
            this.plotObjects.probability = this.createLinePlot(
                x, probDensity, 0x10b981, settings.scale * 0.5
            );
            this.scene.add(this.plotObjects.probability);
        }

        // Plot potential
        if (settings.showPotential && potential) {
            this.plotObjects.potential = this.createFilledPlot(
                x, potential, 0xff6b6b, 0.2
            );
            this.scene.add(this.plotObjects.potential);
        }

        // Plot energy levels
        if (settings.showEnergyLevels && energyLevels) {
            this.plotObjects.energyLevels = this.createEnergyLevelLines(
                x, energyLevels, xMin, xMax
            );
            this.scene.add(this.plotObjects.energyLevels);
        }
    }

    /**
     * Create a line plot from data
     */
    createLinePlot(x, y, color, scale = 1.0) {
        const geometry = new THREE.BufferGeometry();
        const points = [];

        const xMin = x[0];
        const xMax = x[x.length - 1];
        const xRange = xMax - xMin;

        const yMax = Math.max(...y.map(v => Math.abs(v)));

        for (let i = 0; i < x.length; i++) {
            const xNorm = ((x[i] - xMin) / xRange) * 20 - 10;
            const yNorm = (y[i] / (yMax || 1)) * 5 * scale;
            points.push(new THREE.Vector3(xNorm, yNorm, 0));
        }

        geometry.setFromPoints(points);

        const material = new THREE.LineBasicMaterial({
            color: color,
            linewidth: 2,
            fog: false
        });

        const line = new THREE.Line(geometry, material);
        return line;
    }

    /**
     * Create a filled area plot
     */
    createFilledPlot(x, y, color, opacity = 0.3) {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];

        const xMin = x[0];
        const xMax = x[x.length - 1];
        const xRange = xMax - xMin;

        const yMax = Math.max(...y.map(v => Math.abs(v)));

        // Create vertices for the filled area
        for (let i = 0; i < x.length; i++) {
            const xNorm = ((x[i] - xMin) / xRange) * 20 - 10;
            const yNorm = (y[i] / (yMax || 1)) * 5;
            
            // Top vertex
            vertices.push(xNorm, yNorm, 0);
            // Bottom vertex
            vertices.push(xNorm, 0, 0);
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(
            new Float32Array(vertices), 3
        ));

        // Create faces
        const indices = [];
        for (let i = 0; i < x.length - 1; i++) {
            const a = i * 2;
            const b = i * 2 + 1;
            const c = (i + 1) * 2;
            const d = (i + 1) * 2 + 1;

            indices.push(a, b, c);
            indices.push(b, d, c);
        }

        geometry.setIndex(new THREE.BufferAttribute(
            new Uint32Array(indices), 1
        ));
        geometry.computeVertexNormals();

        const material = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: opacity,
            side: THREE.DoubleSide
        });

        const mesh = new THREE.Mesh(geometry, material);
        return mesh;
    }

    /**
     * Create energy level lines
     */
    createEnergyLevelLines(x, energies, xMin, xMax) {
        const group = new THREE.Group();

        const xRange = xMax - xMin;
        const maxEnergy = Math.max(...energies);

        for (let i = 0; i < energies.length; i++) {
            const energy = energies[i];
            const yNorm = (energy / (maxEnergy || 1)) * 5;

            const geometry = new THREE.BufferGeometry();
            const points = [
                new THREE.Vector3(-10, yNorm, 0),
                new THREE.Vector3(10, yNorm, 0)
            ];
            geometry.setFromPoints(points);

            const material = new THREE.LineBasicMaterial({
                color: 0xf59e0b,
                transparent: true,
                opacity: 0.6,
                dashed: true
            });

            const line = new THREE.Line(geometry, material);
            group.add(line);
        }

        return group;
    }

    /**
     * Update visualization
     */
    updateVisualization(x, psi, potential = null, energyLevels = null, options = {}) {
        this.plotWavefunction(x, psi, potential, energyLevels, options);
    }

    /**
     * Animation loop
     */
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        this.renderer.render(this.scene, this.camera);
    }

    /**
     * Handle window resize
     */
    onWindowResize() {
        const width = this.canvas.clientWidth;
        const height = this.canvas.clientHeight;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    /**
     * Cleanup
     */
    dispose() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        window.removeEventListener('resize', this.onWindowResize);
        this.renderer.dispose();
    }
}
