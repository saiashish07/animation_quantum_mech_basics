import { useEffect, useRef, useState } from 'react';
import { motion } from 'motion/react';
import { Slider } from './ui/slider';
import { Label } from './ui/label';
import { Card } from './ui/card';

export function FiniteBarrier() {
  const waveCanvasRef = useRef<HTMLCanvasElement>(null);
  const probabilityCanvasRef = useRef<HTMLCanvasElement>(null);
  const transmissionCanvasRef = useRef<HTMLCanvasElement>(null);
  const [barrierHeight, setBarrierHeight] = useState(8);
  const [barrierWidth, setBarrierWidth] = useState(5);
  const [particleEnergy, setParticleEnergy] = useState(6);
  const animationRef = useRef<number>();

  useEffect(() => {
    const waveCanvas = waveCanvasRef.current;
    const probCanvas = probabilityCanvasRef.current;
    const transCanvas = transmissionCanvasRef.current;
    
    if (!waveCanvas || !probCanvas || !transCanvas) return;

    const waveCtx = waveCanvas.getContext('2d');
    const probCtx = probCanvas.getContext('2d');
    const transCtx = transCanvas.getContext('2d');
    
    if (!waveCtx || !probCtx || !transCtx) return;

    let time = 0;

    const animate = () => {
      const width = 700;
      const height = 250;

      // Clear canvases
      [waveCtx, probCtx, transCtx].forEach(ctx => {
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, width, height);
      });

      // Draw grid
      [waveCtx, probCtx, transCtx].forEach(ctx => {
        ctx.strokeStyle = 'rgba(59, 130, 246, 0.1)';
        ctx.lineWidth = 1;
        for (let i = 0; i < width; i += 50) {
          ctx.beginPath();
          ctx.moveTo(i, 0);
          ctx.lineTo(i, height);
          ctx.stroke();
        }
        for (let i = 0; i < height; i += 50) {
          ctx.beginPath();
          ctx.moveTo(0, i);
          ctx.lineTo(width, i);
          ctx.stroke();
        }
      });

      const barrierStart = 300;
      const barrierPixelWidth = barrierWidth * 20;
      const barrierEnd = barrierStart + barrierPixelWidth;
      const V0 = barrierHeight;
      const E = particleEnergy;

      // === WAVE FUNCTION CANVAS ===
      // Draw barrier
      const barrierHeightPixels = (V0 / 15) * 150;
      waveCtx.fillStyle = 'rgba(239, 68, 68, 0.2)';
      waveCtx.fillRect(barrierStart, height / 2 - barrierHeightPixels / 2, barrierPixelWidth, barrierHeightPixels);
      waveCtx.strokeStyle = '#ef4444';
      waveCtx.lineWidth = 2;
      waveCtx.strokeRect(barrierStart, height / 2 - barrierHeightPixels / 2, barrierPixelWidth, barrierHeightPixels);

      // Energy level line
      const energyY = height / 2 - (E / 15) * 150;
      waveCtx.strokeStyle = '#10b981';
      waveCtx.lineWidth = 2;
      waveCtx.setLineDash([5, 5]);
      waveCtx.beginPath();
      waveCtx.moveTo(0, energyY);
      waveCtx.lineTo(width, energyY);
      waveCtx.stroke();
      waveCtx.setLineDash([]);

      // Calculate wave parameters
      const k1 = Math.sqrt(E); // wave vector in region I and III
      const amplitude = 60;

      let k2, isEvanescent;
      if (E < V0) {
        // Evanescent wave inside barrier
        k2 = Math.sqrt(V0 - E);
        isEvanescent = true;
      } else {
        // Propagating wave inside barrier
        k2 = Math.sqrt(E - V0);
        isEvanescent = false;
      }

      // Transmission coefficient (simplified)
      let T;
      if (E >= V0) {
        T = 1 / (1 + Math.pow(V0, 2) * Math.pow(Math.sin(k2 * barrierWidth), 2) / (4 * E * (E - V0)));
      } else {
        T = 1 / (1 + Math.pow(V0, 2) * Math.pow(Math.sinh(k2 * barrierWidth), 2) / (4 * E * (V0 - E)));
      }
      const R = 1 - T; // Reflection coefficient

      // Draw wave function
      waveCtx.strokeStyle = '#3b82f6';
      waveCtx.lineWidth = 2.5;
      waveCtx.beginPath();

      // Region I (incident + reflected)
      for (let x = 0; x < barrierStart; x++) {
        const xPos = x / 20;
        const incident = Math.cos(k1 * xPos - time * 0.05);
        const reflected = Math.sqrt(R) * Math.cos(-k1 * xPos - time * 0.05);
        const psi = incident + reflected;
        const y = height / 2 - psi * amplitude;
        if (x === 0) {
          waveCtx.moveTo(x, y);
        } else {
          waveCtx.lineTo(x, y);
        }
      }

      // Region II (inside barrier)
      waveCtx.strokeStyle = '#a78bfa';
      for (let x = barrierStart; x <= barrierEnd; x++) {
        const xPos = (x - barrierStart) / 20;
        let psi;
        if (isEvanescent) {
          psi = Math.exp(-k2 * xPos) * Math.cos(time * 0.05);
        } else {
          psi = Math.cos(k2 * xPos - time * 0.05);
        }
        const y = height / 2 - psi * amplitude * 0.7;
        waveCtx.lineTo(x, y);
      }

      // Region III (transmitted)
      waveCtx.strokeStyle = '#10b981';
      for (let x = barrierEnd; x < width; x++) {
        const xPos = (x - barrierEnd) / 20;
        const psi = Math.sqrt(T) * Math.cos(k1 * xPos - time * 0.05);
        const y = height / 2 - psi * amplitude;
        waveCtx.lineTo(x, y);
      }
      waveCtx.stroke();

      // Labels
      waveCtx.fillStyle = '#3b82f6';
      waveCtx.font = '14px monospace';
      waveCtx.fillText('Wave Function ψ(x)', 10, 25);
      waveCtx.fillStyle = '#60a5fa';
      waveCtx.font = '11px monospace';
      waveCtx.fillText('Blue: Incident+Reflected', 10, 45);
      waveCtx.fillStyle = '#a78bfa';
      waveCtx.fillText('Purple: Inside barrier', 10, 60);
      waveCtx.fillStyle = '#10b981';
      waveCtx.fillText('Green: Transmitted', 10, 75);

      // === PROBABILITY DENSITY CANVAS ===
      // Draw barrier
      probCtx.fillStyle = 'rgba(239, 68, 68, 0.2)';
      probCtx.fillRect(barrierStart, height / 2 - barrierHeightPixels / 2, barrierPixelWidth, barrierHeightPixels);
      probCtx.strokeStyle = '#ef4444';
      probCtx.lineWidth = 2;
      probCtx.strokeRect(barrierStart, height / 2 - barrierHeightPixels / 2, barrierPixelWidth, barrierHeightPixels);

      // Draw probability density
      probCtx.fillStyle = 'rgba(139, 92, 246, 0.4)';
      probCtx.beginPath();
      probCtx.moveTo(0, height);

      for (let x = 0; x < width; x++) {
        let psi = 0;
        
        if (x < barrierStart) {
          // Region I
          const xPos = x / 20;
          const incident = 1;
          const reflected = Math.sqrt(R);
          // Time-averaged probability
          psi = incident * incident + reflected * reflected + 2 * incident * reflected * Math.cos(2 * k1 * xPos);
        } else if (x <= barrierEnd) {
          // Region II
          const xPos = (x - barrierStart) / 20;
          if (isEvanescent) {
            psi = Math.exp(-2 * k2 * xPos);
          } else {
            psi = 0.5;
          }
        } else {
          // Region III
          psi = T;
        }

        const probability = Math.abs(psi);
        const y = height - probability * 120;
        probCtx.lineTo(x, y);
      }
      probCtx.lineTo(width, height);
      probCtx.closePath();
      probCtx.fill();

      // Outline
      probCtx.strokeStyle = '#8b5cf6';
      probCtx.lineWidth = 2;
      probCtx.beginPath();
      for (let x = 0; x < width; x++) {
        let psi = 0;
        
        if (x < barrierStart) {
          const xPos = x / 20;
          const incident = 1;
          const reflected = Math.sqrt(R);
          psi = incident * incident + reflected * reflected + 2 * incident * reflected * Math.cos(2 * k1 * xPos);
        } else if (x <= barrierEnd) {
          const xPos = (x - barrierStart) / 20;
          if (isEvanescent) {
            psi = Math.exp(-2 * k2 * xPos);
          } else {
            psi = 0.5;
          }
        } else {
          psi = T;
        }

        const probability = Math.abs(psi);
        const y = height - probability * 120;
        if (x === 0) {
          probCtx.moveTo(x, y);
        } else {
          probCtx.lineTo(x, y);
        }
      }
      probCtx.stroke();

      // Labels
      probCtx.fillStyle = '#8b5cf6';
      probCtx.font = '14px monospace';
      probCtx.fillText('Probability Density |ψ(x)|²', 10, 25);
      probCtx.fillStyle = '#a78bfa';
      probCtx.font = '12px monospace';
      probCtx.fillText('Shows interference pattern before barrier', 10, 45);

      // === TRANSMISSION DIAGRAM ===
      // Draw energy levels and barrier
      transCtx.fillStyle = 'rgba(239, 68, 68, 0.2)';
      transCtx.fillRect(barrierStart, 50, barrierPixelWidth, height - 100);
      transCtx.strokeStyle = '#ef4444';
      transCtx.lineWidth = 3;
      transCtx.beginPath();
      transCtx.moveTo(barrierStart, height - 50 - barrierHeightPixels);
      transCtx.lineTo(barrierStart, height - 50);
      transCtx.lineTo(barrierEnd, height - 50);
      transCtx.lineTo(barrierEnd, height - 50 - barrierHeightPixels);
      transCtx.stroke();

      // Base line
      transCtx.strokeStyle = '#475569';
      transCtx.lineWidth = 2;
      transCtx.beginPath();
      transCtx.moveTo(0, height - 50);
      transCtx.lineTo(width, height - 50);
      transCtx.stroke();

      // Energy level
      transCtx.strokeStyle = '#10b981';
      transCtx.lineWidth = 2.5;
      transCtx.setLineDash([10, 5]);
      transCtx.beginPath();
      transCtx.moveTo(0, height - 50 - (E / 15) * 150);
      transCtx.lineTo(width, height - 50 - (E / 15) * 150);
      transCtx.stroke();
      transCtx.setLineDash([]);

      // Transmission and reflection percentages
      transCtx.fillStyle = '#10b981';
      transCtx.font = 'bold 16px monospace';
      transCtx.fillText(`Transmission: ${(T * 100).toFixed(1)}%`, width - 220, 30);
      transCtx.fillStyle = '#ef4444';
      transCtx.fillText(`Reflection: ${(R * 100).toFixed(1)}%`, width - 220, 50);

      // Labels
      transCtx.fillStyle = '#3b82f6';
      transCtx.font = '14px monospace';
      transCtx.fillText('Energy Diagram', 10, 25);
      transCtx.fillStyle = '#10b981';
      transCtx.font = '12px monospace';
      transCtx.fillText(`E = ${E.toFixed(1)}`, 10, 45);
      transCtx.fillStyle = '#ef4444';
      transCtx.fillText(`V₀ = ${V0.toFixed(1)}`, 10, 60);

      // Classical vs Quantum note
      if (E < V0) {
        transCtx.fillStyle = '#fbbf24';
        transCtx.font = '13px monospace';
        transCtx.fillText('⚡ Quantum tunneling! (E < V₀)', width / 2 - 120, height - 20);
      } else {
        transCtx.fillStyle = '#60a5fa';
        transCtx.font = '13px monospace';
        transCtx.fillText('Classical barrier penetration (E > V₀)', width / 2 - 140, height - 20);
      }

      time += 1;
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [barrierHeight, barrierWidth, particleEnergy]);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-blue-100 mb-2">Finite Potential Barrier</h2>
        <p className="text-blue-300/70 text-sm mb-4">
          A particle encounters a finite energy barrier. Classically impossible, quantum mechanics allows transmission even when E &lt; V₀.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="bg-slate-950/50 border-blue-500/20 p-4">
          <canvas
            ref={waveCanvasRef}
            width={700}
            height={250}
            className="w-full border border-blue-500/30 rounded-lg"
          />
        </Card>

        <Card className="bg-slate-950/50 border-blue-500/20 p-4">
          <canvas
            ref={transmissionCanvasRef}
            width={700}
            height={250}
            className="w-full border border-blue-500/30 rounded-lg"
          />
        </Card>
      </div>

      <Card className="bg-slate-950/50 border-blue-500/20 p-4">
        <canvas
          ref={probabilityCanvasRef}
          width={700}
          height={250}
          className="w-full border border-blue-500/30 rounded-lg"
        />
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
        <div className="space-y-3">
          <Label className="text-blue-200">Particle Energy (E): {particleEnergy.toFixed(1)} eV</Label>
          <Slider
            value={[particleEnergy]}
            onValueChange={(v) => setParticleEnergy(v[0])}
            min={2}
            max={12}
            step={0.5}
            className="w-full"
          />
          <p className="text-blue-300/60 text-xs">
            Energy of the incident particle
          </p>
        </div>

        <div className="space-y-3">
          <Label className="text-blue-200">Barrier Height (V₀): {barrierHeight.toFixed(1)} eV</Label>
          <Slider
            value={[barrierHeight]}
            onValueChange={(v) => setBarrierHeight(v[0])}
            min={4}
            max={12}
            step={0.5}
            className="w-full"
          />
          <p className="text-blue-300/60 text-xs">
            Height of the potential barrier
          </p>
        </div>

        <div className="space-y-3">
          <Label className="text-blue-200">Barrier Width: {barrierWidth.toFixed(1)} nm</Label>
          <Slider
            value={[barrierWidth]}
            onValueChange={(v) => setBarrierWidth(v[0])}
            min={2}
            max={10}
            step={0.5}
            className="w-full"
          />
          <p className="text-blue-300/60 text-xs">
            Thickness of the barrier
          </p>
        </div>
      </div>

      <Card className="bg-blue-950/30 border-blue-500/20 p-4">
        <div className="text-sm space-y-2">
          <p className="text-blue-100">
            <span className="text-blue-400">Classical prediction:</span> {particleEnergy < barrierHeight ? 'Cannot pass (E < V₀)' : 'Can pass (E > V₀)'}
          </p>
          <p className="text-blue-100">
            <span className="text-blue-400">Quantum result:</span> Partial transmission in all cases
          </p>
        </div>
      </Card>
    </div>
  );
}
