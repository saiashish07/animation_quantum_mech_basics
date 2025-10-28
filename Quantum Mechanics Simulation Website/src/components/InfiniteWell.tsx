import { useEffect, useRef, useState } from 'react';
import { motion } from 'motion/react';
import { Slider } from './ui/slider';
import { Label } from './ui/label';
import { Card } from './ui/card';

export function InfiniteWell() {
  const waveCanvasRef = useRef<HTMLCanvasElement>(null);
  const probabilityCanvasRef = useRef<HTMLCanvasElement>(null);
  const energyCanvasRef = useRef<HTMLCanvasElement>(null);
  const [quantumNumber, setQuantumNumber] = useState(1);
  const [wellWidth, setWellWidth] = useState(10);
  const animationRef = useRef<number>();

  useEffect(() => {
    const waveCanvas = waveCanvasRef.current;
    const probCanvas = probabilityCanvasRef.current;
    const energyCanvas = energyCanvasRef.current;
    
    if (!waveCanvas || !probCanvas || !energyCanvas) return;

    const waveCtx = waveCanvas.getContext('2d');
    const probCtx = probCanvas.getContext('2d');
    const energyCtx = energyCanvas.getContext('2d');
    
    if (!waveCtx || !probCtx || !energyCtx) return;

    let time = 0;

    const animate = () => {
      const width = 700;
      const height = 250;
      const n = quantumNumber;
      const L = wellWidth;

      // Clear canvases
      waveCtx.fillStyle = '#0f172a';
      waveCtx.fillRect(0, 0, width, height);
      probCtx.fillStyle = '#0f172a';
      probCtx.fillRect(0, 0, width, height);
      energyCtx.fillStyle = '#0f172a';
      energyCtx.fillRect(0, 0, width, height);

      // Draw grid for all canvases
      [waveCtx, probCtx, energyCtx].forEach(ctx => {
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

      const wellStart = 100;
      const wellEnd = width - 100;
      const wellLength = wellEnd - wellStart;

      // === WAVE FUNCTION CANVAS ===
      // Draw infinite walls
      waveCtx.fillStyle = 'rgba(239, 68, 68, 0.3)';
      waveCtx.fillRect(0, 0, wellStart, height);
      waveCtx.fillRect(wellEnd, 0, width - wellEnd, height);
      waveCtx.strokeStyle = '#ef4444';
      waveCtx.lineWidth = 3;
      waveCtx.beginPath();
      waveCtx.moveTo(wellStart, 0);
      waveCtx.lineTo(wellStart, height);
      waveCtx.moveTo(wellEnd, 0);
      waveCtx.lineTo(wellEnd, height);
      waveCtx.stroke();

      // Draw wave function ψ(x) = √(2/L) * sin(nπx/L)
      waveCtx.strokeStyle = '#3b82f6';
      waveCtx.lineWidth = 2.5;
      waveCtx.beginPath();
      for (let x = wellStart; x <= wellEnd; x++) {
        const xNorm = (x - wellStart) / wellLength;
        const psi = Math.sqrt(2 / L) * Math.sin(n * Math.PI * xNorm) * Math.cos(time * 0.02);
        const y = height / 2 - psi * 80;
        if (x === wellStart) {
          waveCtx.moveTo(x, y);
        } else {
          waveCtx.lineTo(x, y);
        }
      }
      waveCtx.stroke();

      // Zero line
      waveCtx.strokeStyle = 'rgba(148, 163, 184, 0.5)';
      waveCtx.lineWidth = 1;
      waveCtx.setLineDash([5, 5]);
      waveCtx.beginPath();
      waveCtx.moveTo(0, height / 2);
      waveCtx.lineTo(width, height / 2);
      waveCtx.stroke();
      waveCtx.setLineDash([]);

      // Labels
      waveCtx.fillStyle = '#3b82f6';
      waveCtx.font = '14px monospace';
      waveCtx.fillText('Wave Function ψ(x)', 10, 25);
      waveCtx.fillStyle = '#60a5fa';
      waveCtx.font = '12px monospace';
      waveCtx.fillText(`ψₙ(x) = √(2/L) sin(nπx/L)`, 10, 45);

      // === PROBABILITY DENSITY CANVAS ===
      // Draw walls
      probCtx.fillStyle = 'rgba(239, 68, 68, 0.3)';
      probCtx.fillRect(0, 0, wellStart, height);
      probCtx.fillRect(wellEnd, 0, width - wellEnd, height);
      probCtx.strokeStyle = '#ef4444';
      probCtx.lineWidth = 3;
      probCtx.beginPath();
      probCtx.moveTo(wellStart, 0);
      probCtx.lineTo(wellStart, height);
      probCtx.moveTo(wellEnd, 0);
      probCtx.lineTo(wellEnd, height);
      probCtx.stroke();

      // Draw probability density |ψ|²
      probCtx.fillStyle = 'rgba(139, 92, 246, 0.4)';
      probCtx.beginPath();
      probCtx.moveTo(wellStart, height);
      for (let x = wellStart; x <= wellEnd; x++) {
        const xNorm = (x - wellStart) / wellLength;
        const psi = Math.sqrt(2 / L) * Math.sin(n * Math.PI * xNorm);
        const probability = psi * psi;
        const y = height - probability * 150;
        probCtx.lineTo(x, y);
      }
      probCtx.lineTo(wellEnd, height);
      probCtx.closePath();
      probCtx.fill();

      // Draw outline
      probCtx.strokeStyle = '#8b5cf6';
      probCtx.lineWidth = 2;
      probCtx.beginPath();
      for (let x = wellStart; x <= wellEnd; x++) {
        const xNorm = (x - wellStart) / wellLength;
        const psi = Math.sqrt(2 / L) * Math.sin(n * Math.PI * xNorm);
        const probability = psi * psi;
        const y = height - probability * 150;
        if (x === wellStart) {
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
      probCtx.fillText('Shows where particle is likely to be found', 10, 45);

      // === ENERGY LEVEL DIAGRAM ===
      const maxN = 6;
      const energyScale = 200;

      // Draw potential well
      energyCtx.strokeStyle = '#ef4444';
      energyCtx.lineWidth = 3;
      energyCtx.beginPath();
      energyCtx.moveTo(wellStart, height);
      energyCtx.lineTo(wellStart, 50);
      energyCtx.lineTo(wellEnd, 50);
      energyCtx.lineTo(wellEnd, height);
      energyCtx.stroke();

      // Draw energy levels
      for (let i = 1; i <= maxN; i++) {
        const energy = (i * i * Math.PI * Math.PI) / (2 * L * L);
        const y = height - 50 - energy * energyScale;

        if (y < 50) continue;

        energyCtx.strokeStyle = i === n ? '#3b82f6' : 'rgba(59, 130, 246, 0.3)';
        energyCtx.lineWidth = i === n ? 2.5 : 1.5;
        energyCtx.setLineDash(i === n ? [] : [5, 5]);
        energyCtx.beginPath();
        energyCtx.moveTo(wellStart + 20, y);
        energyCtx.lineTo(wellEnd - 20, y);
        energyCtx.stroke();

        // Label
        energyCtx.fillStyle = i === n ? '#3b82f6' : '#60a5fa';
        energyCtx.font = i === n ? 'bold 13px monospace' : '11px monospace';
        energyCtx.fillText(`n=${i}`, wellEnd + 10, y + 4);
        energyCtx.fillText(`E=${i}²`, wellEnd + 55, y + 4);
      }
      energyCtx.setLineDash([]);

      // Labels
      energyCtx.fillStyle = '#10b981';
      energyCtx.font = '14px monospace';
      energyCtx.fillText('Energy Level Diagram', 10, 25);
      energyCtx.fillStyle = '#34d399';
      energyCtx.font = '12px monospace';
      energyCtx.fillText('Eₙ = n²π²ℏ²/(2mL²)', 10, 45);

      // Ground state marker
      energyCtx.fillStyle = '#60a5fa';
      energyCtx.font = '11px monospace';
      energyCtx.fillText('← Current level', wellEnd + 110, height - 50 - ((n * n * Math.PI * Math.PI) / (2 * L * L)) * energyScale + 4);

      time += 1;
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [quantumNumber, wellWidth]);

  const energy = (quantumNumber * quantumNumber * Math.PI * Math.PI) / (2 * wellWidth * wellWidth);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-blue-100 mb-2">Infinite Potential Well (Particle in a Box)</h2>
        <p className="text-blue-300/70 text-sm mb-4">
          A particle confined between two infinitely high potential barriers. The particle can only exist in discrete energy states.
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
            ref={energyCanvasRef}
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

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        <div className="space-y-3">
          <Label className="text-blue-200">Quantum Number (n): {quantumNumber}</Label>
          <Slider
            value={[quantumNumber]}
            onValueChange={(v) => setQuantumNumber(v[0])}
            min={1}
            max={6}
            step={1}
            className="w-full"
          />
          <p className="text-blue-300/60 text-xs">
            Higher n = more nodes in wave function, higher energy
          </p>
        </div>

        <div className="space-y-3">
          <Label className="text-blue-200">Well Width (L): {wellWidth.toFixed(1)} nm</Label>
          <Slider
            value={[wellWidth]}
            onValueChange={(v) => setWellWidth(v[0])}
            min={5}
            max={15}
            step={0.5}
            className="w-full"
          />
          <p className="text-blue-300/60 text-xs">
            Larger well = lower energy levels, more states possible
          </p>
        </div>
      </div>

      <Card className="bg-blue-950/30 border-blue-500/20 p-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-blue-400/70">Energy Level</p>
            <p className="text-blue-100">E₍ₙ₎ = {energy.toFixed(3)}</p>
          </div>
          <div>
            <p className="text-blue-400/70">Wavelength</p>
            <p className="text-blue-100">λₙ = {(2 * wellWidth / quantumNumber).toFixed(2)} nm</p>
          </div>
          <div>
            <p className="text-blue-400/70">Nodes</p>
            <p className="text-blue-100">{quantumNumber - 1}</p>
          </div>
          <div>
            <p className="text-blue-400/70">Normalization</p>
            <p className="text-blue-100">√(2/L)</p>
          </div>
        </div>
      </Card>
    </div>
  );
}
