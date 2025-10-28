import { useEffect, useRef, useState } from 'react';
import { motion } from 'motion/react';
import { Slider } from './ui/slider';
import { Label } from './ui/label';
import { Card } from './ui/card';

export function QuantumTunneling() {
  const simulationCanvasRef = useRef<HTMLCanvasElement>(null);
  const transmissionCanvasRef = useRef<HTMLCanvasElement>(null);
  const [barrierHeight, setBarrierHeight] = useState(100);
  const [barrierWidth, setBarrierWidth] = useState(80);
  const [particleEnergy, setParticleEnergy] = useState(60);
  const animationRef = useRef<number>();
  const particlesRef = useRef<Array<{
    x: number;
    y: number;
    vx: number;
    tunneled: boolean;
    reflected: boolean;
    active: boolean;
  }>>([]);

  useEffect(() => {
    const simCanvas = simulationCanvasRef.current;
    const transCanvas = transmissionCanvasRef.current;
    
    if (!simCanvas || !transCanvas) return;

    const simCtx = simCanvas.getContext('2d');
    const transCtx = transCanvas.getContext('2d');
    
    if (!simCtx || !transCtx) return;

    let stats = { total: 0, tunneled: 0, reflected: 0 };
    let frameCount = 0;

    const barrierX = 300;
    const width = 700;
    const height = 300;

    const animate = () => {
      // Clear canvases
      simCtx.fillStyle = 'rgba(15, 23, 42, 0.1)';
      simCtx.fillRect(0, 0, width, height);
      transCtx.fillStyle = '#0f172a';
      transCtx.fillRect(0, 0, width, height);

      // Draw grid on simulation
      simCtx.strokeStyle = 'rgba(59, 130, 246, 0.05)';
      simCtx.lineWidth = 1;
      for (let i = 0; i < width; i += 50) {
        simCtx.beginPath();
        simCtx.moveTo(i, 0);
        simCtx.lineTo(i, height);
        simCtx.stroke();
      }

      // === SIMULATION CANVAS ===
      // Draw barrier
      const barrierHeightPixels = (barrierHeight / 150) * (height / 2);
      simCtx.fillStyle = 'rgba(239, 68, 68, 0.2)';
      simCtx.fillRect(barrierX, height / 2 - barrierHeightPixels / 2, barrierWidth, barrierHeightPixels);
      simCtx.strokeStyle = '#ef4444';
      simCtx.lineWidth = 3;
      simCtx.strokeRect(barrierX, height / 2 - barrierHeightPixels / 2, barrierWidth, barrierHeightPixels);

      // Labels on barrier
      simCtx.fillStyle = '#ef4444';
      simCtx.font = 'bold 14px monospace';
      simCtx.fillText(`V₀ = ${barrierHeight}`, barrierX + barrierWidth / 2 - 35, height / 2 - barrierHeightPixels / 2 - 10);

      // Energy level
      const energyY = height / 2 + (height / 2) * (1 - particleEnergy / 150);
      simCtx.strokeStyle = '#10b981';
      simCtx.lineWidth = 2;
      simCtx.setLineDash([5, 5]);
      simCtx.beginPath();
      simCtx.moveTo(0, energyY);
      simCtx.lineTo(width, energyY);
      simCtx.stroke();
      simCtx.setLineDash([]);
      simCtx.fillStyle = '#10b981';
      simCtx.font = '12px monospace';
      simCtx.fillText(`E = ${particleEnergy}`, 10, energyY - 5);

      // Emit particles
      if (frameCount % 15 === 0) {
        particlesRef.current.push({
          x: 50,
          y: height / 2 + (Math.random() - 0.5) * 60,
          vx: 2.5,
          tunneled: false,
          reflected: false,
          active: true
        });
      }

      // Update particles
      particlesRef.current = particlesRef.current.filter(particle => {
        if (!particle.active) return false;

        particle.x += particle.vx;

        // Interaction with barrier
        if (particle.x >= barrierX && particle.x <= barrierX + barrierWidth && !particle.tunneled && !particle.reflected) {
          // Calculate tunneling probability
          const T = particleEnergy >= barrierHeight 
            ? 1 
            : Math.exp(-2 * Math.sqrt(Math.max(0, barrierHeight - particleEnergy)) * barrierWidth / 100);
          
          if (Math.random() < T) {
            particle.tunneled = true;
          } else {
            particle.reflected = true;
            particle.vx = -particle.vx;
            particle.x = barrierX - 5;
            stats.reflected++;
            stats.total++;
          }
        }

        // Check if tunneled particle passed barrier
        if (particle.tunneled && particle.x > barrierX + barrierWidth + 5 && particle.active) {
          stats.tunneled++;
          stats.total++;
        }

        // Remove if off screen
        if (particle.x > width || particle.x < 0) {
          particle.active = false;
          return false;
        }

        // Draw particle
        let color;
        if (particle.tunneled) {
          color = '#8b5cf6'; // Purple for tunneled
        } else if (particle.reflected) {
          color = '#ef4444'; // Red for reflected
        } else {
          color = '#3b82f6'; // Blue for incident
        }

        simCtx.fillStyle = color;
        simCtx.beginPath();
        simCtx.arc(particle.x, particle.y, 4, 0, Math.PI * 2);
        simCtx.fill();

        // Wave visualization
        simCtx.globalAlpha = 0.3;
        simCtx.strokeStyle = color;
        simCtx.lineWidth = 1;
        simCtx.beginPath();
        for (let i = -10; i < 10; i++) {
          const waveX = particle.x + i * 3;
          const waveY = particle.y + Math.sin(i * 0.3 + frameCount * 0.1) * 4;
          if (i === -10) {
            simCtx.moveTo(waveX, waveY);
          } else {
            simCtx.lineTo(waveX, waveY);
          }
        }
        simCtx.stroke();
        simCtx.globalAlpha = 1;

        return true;
      });

      // Statistics display
      simCtx.fillStyle = '#3b82f6';
      simCtx.font = 'bold 16px monospace';
      simCtx.fillText('Quantum Tunneling Simulation', 10, 25);
      
      if (stats.total > 0) {
        const tunneledPercent = (stats.tunneled / stats.total * 100).toFixed(1);
        const reflectedPercent = (stats.reflected / stats.total * 100).toFixed(1);
        
        simCtx.fillStyle = '#8b5cf6';
        simCtx.font = 'bold 14px monospace';
        simCtx.fillText(`Tunneled: ${tunneledPercent}% (${stats.tunneled})`, width - 220, 25);
        simCtx.fillStyle = '#ef4444';
        simCtx.fillText(`Reflected: ${reflectedPercent}% (${stats.reflected})`, width - 220, 45);
      }

      simCtx.fillStyle = '#60a5fa';
      simCtx.font = '11px monospace';
      simCtx.fillText('Blue: Incident | Purple: Tunneled | Red: Reflected', 10, height - 15);

      // === TRANSMISSION GRAPH ===
      transCtx.strokeStyle = 'rgba(59, 130, 246, 0.1)';
      transCtx.lineWidth = 1;
      for (let i = 0; i < width; i += 50) {
        transCtx.beginPath();
        transCtx.moveTo(i, 0);
        transCtx.lineTo(i, height);
        transCtx.stroke();
      }
      for (let i = 0; i < height; i += 50) {
        transCtx.beginPath();
        transCtx.moveTo(0, i);
        transCtx.lineTo(width, i);
        transCtx.stroke();
      }

      // Draw axes
      transCtx.strokeStyle = '#475569';
      transCtx.lineWidth = 2;
      transCtx.beginPath();
      transCtx.moveTo(50, height - 40);
      transCtx.lineTo(width - 30, height - 40);
      transCtx.moveTo(50, height - 40);
      transCtx.lineTo(50, 30);
      transCtx.stroke();

      // Labels
      transCtx.fillStyle = '#3b82f6';
      transCtx.font = 'bold 14px monospace';
      transCtx.fillText('Transmission Coefficient vs Energy', 10, 25);
      
      transCtx.fillStyle = '#94a3b8';
      transCtx.font = '11px monospace';
      transCtx.fillText('T', 30, 35);
      transCtx.fillText('1.0', 20, 45);
      transCtx.fillText('0.5', 20, height / 2);
      transCtx.fillText('0.0', 20, height - 45);
      transCtx.fillText('Energy (E)', width / 2 - 30, height - 15);
      transCtx.fillText('0', 45, height - 25);
      transCtx.fillText('V₀', barrierHeight * 3 + 40, height - 25);

      // Draw transmission curve
      transCtx.strokeStyle = '#8b5cf6';
      transCtx.lineWidth = 3;
      transCtx.beginPath();
      
      for (let E = 0; E <= 150; E += 1) {
        let T;
        if (E >= barrierHeight) {
          T = 1 / (1 + Math.pow(barrierHeight, 2) / (4 * E * (E - barrierHeight)));
        } else {
          const kappa = Math.sqrt(Math.max(0, barrierHeight - E));
          T = Math.exp(-2 * kappa * barrierWidth / 100);
        }
        
        const x = 50 + (E / 150) * (width - 80);
        const y = height - 40 - T * (height - 70);
        
        if (E === 0) {
          transCtx.moveTo(x, y);
        } else {
          transCtx.lineTo(x, y);
        }
      }
      transCtx.stroke();

      // Mark current energy
      const currentT = particleEnergy >= barrierHeight 
        ? 1 / (1 + Math.pow(barrierHeight, 2) / (4 * particleEnergy * (particleEnergy - barrierHeight)))
        : Math.exp(-2 * Math.sqrt(Math.max(0, barrierHeight - particleEnergy)) * barrierWidth / 100);
      
      const currentX = 50 + (particleEnergy / 150) * (width - 80);
      const currentY = height - 40 - currentT * (height - 70);
      
      transCtx.fillStyle = '#10b981';
      transCtx.beginPath();
      transCtx.arc(currentX, currentY, 6, 0, Math.PI * 2);
      transCtx.fill();
      
      // Vertical line to current energy
      transCtx.strokeStyle = '#10b981';
      transCtx.lineWidth = 2;
      transCtx.setLineDash([3, 3]);
      transCtx.beginPath();
      transCtx.moveTo(currentX, currentY);
      transCtx.lineTo(currentX, height - 40);
      transCtx.stroke();
      transCtx.setLineDash([]);

      // Display transmission coefficient
      transCtx.fillStyle = '#10b981';
      transCtx.font = 'bold 13px monospace';
      transCtx.fillText(`T = ${(currentT * 100).toFixed(1)}%`, currentX + 10, currentY - 10);

      // Barrier height marker
      if (barrierHeight <= 150) {
        const barrierX = 50 + (barrierHeight / 150) * (width - 80);
        transCtx.strokeStyle = '#ef4444';
        transCtx.lineWidth = 2;
        transCtx.setLineDash([5, 5]);
        transCtx.beginPath();
        transCtx.moveTo(barrierX, 30);
        transCtx.lineTo(barrierX, height - 40);
        transCtx.stroke();
        transCtx.setLineDash([]);
        transCtx.fillStyle = '#ef4444';
        transCtx.font = '11px monospace';
        transCtx.fillText('V₀', barrierX - 10, 25);
      }

      frameCount++;
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [barrierHeight, barrierWidth, particleEnergy]);

  const handleReset = () => {
    particlesRef.current = [];
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-blue-100 mb-2">Quantum Tunneling</h2>
        <p className="text-blue-300/70 text-sm mb-4">
          Particles can pass through energy barriers that would be impossible to cross classically. Probability depends on barrier height, width, and particle energy.
        </p>
      </div>

      <Card className="bg-slate-950/50 border-blue-500/20 p-4">
        <canvas
          ref={simulationCanvasRef}
          width={700}
          height={300}
          className="w-full border border-blue-500/30 rounded-lg"
        />
      </Card>

      <Card className="bg-slate-950/50 border-blue-500/20 p-4">
        <canvas
          ref={transmissionCanvasRef}
          width={700}
          height={300}
          className="w-full border border-blue-500/30 rounded-lg"
        />
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
        <div className="space-y-3">
          <Label className="text-blue-200">Particle Energy (E): {particleEnergy}</Label>
          <Slider
            value={[particleEnergy]}
            onValueChange={(v) => setParticleEnergy(v[0])}
            min={20}
            max={140}
            step={5}
            className="w-full"
          />
          <p className="text-blue-300/60 text-xs">
            Higher energy = more tunneling
          </p>
        </div>

        <div className="space-y-3">
          <Label className="text-blue-200">Barrier Height (V₀): {barrierHeight}</Label>
          <Slider
            value={[barrierHeight]}
            onValueChange={(v) => { setBarrierHeight(v[0]); handleReset(); }}
            min={50}
            max={130}
            step={5}
            className="w-full"
          />
          <p className="text-blue-300/60 text-xs">
            Higher barrier = less tunneling
          </p>
        </div>

        <div className="space-y-3">
          <Label className="text-blue-200">Barrier Width: {barrierWidth} nm</Label>
          <Slider
            value={[barrierWidth]}
            onValueChange={(v) => { setBarrierWidth(v[0]); handleReset(); }}
            min={40}
            max={120}
            step={10}
            className="w-full"
          />
          <p className="text-blue-300/60 text-xs">
            Wider barrier = less tunneling
          </p>
        </div>
      </div>

      <Card className="bg-blue-950/30 border-blue-500/20 p-4">
        <div className="text-sm space-y-2">
          <p className="text-blue-100">
            <span className="text-blue-400">Tunneling formula:</span> T ≈ e^(-2√(2m(V₀-E))·d/ℏ) for E &lt; V₀
          </p>
          <p className="text-blue-100">
            <span className="text-blue-400">Applications:</span> Nuclear fusion, scanning tunneling microscopes, tunnel diodes
          </p>
        </div>
      </Card>
    </div>
  );
}
