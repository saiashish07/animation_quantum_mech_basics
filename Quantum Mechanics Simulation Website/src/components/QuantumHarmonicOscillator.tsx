import { useEffect, useRef, useState } from 'react';
import { motion } from 'motion/react';
import { Slider } from './ui/slider';
import { Label } from './ui/label';
import { Card } from './ui/card';

export function QuantumHarmonicOscillator() {
  const waveCanvasRef = useRef<HTMLCanvasElement>(null);
  const probabilityCanvasRef = useRef<HTMLCanvasElement>(null);
  const energyCanvasRef = useRef<HTMLCanvasElement>(null);
  const [quantumNumber, setQuantumNumber] = useState(0);
  const [springConstant, setSpringConstant] = useState(1);
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

    // Hermite polynomial calculation
    const hermite = (n: number, x: number): number => {
      if (n === 0) return 1;
      if (n === 1) return 2 * x;
      if (n === 2) return 4 * x * x - 2;
      if (n === 3) return 8 * x * x * x - 12 * x;
      if (n === 4) return 16 * Math.pow(x, 4) - 48 * x * x + 12;
      if (n === 5) return 32 * Math.pow(x, 5) - 160 * Math.pow(x, 3) + 120 * x;
      return 0;
    };

    const factorial = (n: number): number => {
      if (n <= 1) return 1;
      return n * factorial(n - 1);
    };

    const animate = () => {
      const width = 700;
      const height = 250;
      const n = quantumNumber;
      const omega = springConstant;

      // Clear canvases
      [waveCtx, probCtx, energyCtx].forEach(ctx => {
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, width, height);
      });

      // Draw grid
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

      const centerX = width / 2;
      const scale = 80;

      // === WAVE FUNCTION CANVAS ===
      // Draw potential V(x) = ½kx²
      waveCtx.strokeStyle = '#ef4444';
      waveCtx.lineWidth = 2;
      waveCtx.beginPath();
      for (let x = 0; x < width; x++) {
        const xPos = (x - centerX) / scale;
        const V = 0.5 * omega * xPos * xPos;
        const y = height - 30 - V * 40;
        if (x === 0) {
          waveCtx.moveTo(x, y);
        } else {
          waveCtx.lineTo(x, y);
        }
      }
      waveCtx.stroke();

      // Draw wave function ψₙ(x)
      waveCtx.strokeStyle = '#3b82f6';
      waveCtx.lineWidth = 2.5;
      waveCtx.beginPath();
      
      for (let x = 0; x < width; x++) {
        const xPos = (x - centerX) / scale;
        const normalization = 1 / Math.sqrt(Math.pow(2, n) * factorial(n)) * Math.pow(omega / Math.PI, 0.25);
        const psi = normalization * hermite(n, Math.sqrt(omega) * xPos) * Math.exp(-omega * xPos * xPos / 2);
        const y = height / 2 - psi * 100 * Math.cos(time * 0.02);
        
        if (x === 0) {
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

      // Energy level line
      const En = (n + 0.5) * omega;
      const energyY = height - 30 - En * 40;
      waveCtx.strokeStyle = '#10b981';
      waveCtx.lineWidth = 2;
      waveCtx.setLineDash([5, 5]);
      waveCtx.beginPath();
      waveCtx.moveTo(0, energyY);
      waveCtx.lineTo(width, energyY);
      waveCtx.stroke();
      waveCtx.setLineDash([]);

      // Labels
      waveCtx.fillStyle = '#3b82f6';
      waveCtx.font = '14px monospace';
      waveCtx.fillText('Wave Function ψₙ(x)', 10, 25);
      waveCtx.fillStyle = '#ef4444';
      waveCtx.fillText('V(x) = ½kx²', 10, 45);
      waveCtx.fillStyle = '#10b981';
      waveCtx.fillText(`Eₙ = ${En.toFixed(2)}ℏω`, 10, 65);

      // === PROBABILITY DENSITY CANVAS ===
      // Draw potential
      probCtx.strokeStyle = '#ef4444';
      probCtx.lineWidth = 2;
      probCtx.globalAlpha = 0.3;
      probCtx.beginPath();
      for (let x = 0; x < width; x++) {
        const xPos = (x - centerX) / scale;
        const V = 0.5 * omega * xPos * xPos;
        const y = height - 30 - V * 40;
        if (x === 0) {
          probCtx.moveTo(x, y);
        } else {
          probCtx.lineTo(x, y);
        }
      }
      probCtx.stroke();
      probCtx.globalAlpha = 1;

      // Draw probability density
      probCtx.fillStyle = 'rgba(139, 92, 246, 0.4)';
      probCtx.beginPath();
      probCtx.moveTo(0, height);
      
      for (let x = 0; x < width; x++) {
        const xPos = (x - centerX) / scale;
        const normalization = 1 / Math.sqrt(Math.pow(2, n) * factorial(n)) * Math.pow(omega / Math.PI, 0.25);
        const psi = normalization * hermite(n, Math.sqrt(omega) * xPos) * Math.exp(-omega * xPos * xPos / 2);
        const probability = psi * psi;
        const y = height - probability * 800;
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
        const xPos = (x - centerX) / scale;
        const normalization = 1 / Math.sqrt(Math.pow(2, n) * factorial(n)) * Math.pow(omega / Math.PI, 0.25);
        const psi = normalization * hermite(n, Math.sqrt(omega) * xPos) * Math.exp(-omega * xPos * xPos / 2);
        const probability = psi * psi;
        const y = height - probability * 800;
        if (x === 0) {
          probCtx.moveTo(x, y);
        } else {
          probCtx.lineTo(x, y);
        }
      }
      probCtx.stroke();

      // Classical turning points
      const classicalAmplitude = Math.sqrt(2 * En / omega);
      const turnPoint1 = centerX - classicalAmplitude * scale;
      const turnPoint2 = centerX + classicalAmplitude * scale;
      
      probCtx.strokeStyle = '#fbbf24';
      probCtx.lineWidth = 2;
      probCtx.setLineDash([3, 3]);
      probCtx.beginPath();
      probCtx.moveTo(turnPoint1, 0);
      probCtx.lineTo(turnPoint1, height);
      probCtx.moveTo(turnPoint2, 0);
      probCtx.lineTo(turnPoint2, height);
      probCtx.stroke();
      probCtx.setLineDash([]);

      // Labels
      probCtx.fillStyle = '#8b5cf6';
      probCtx.font = '14px monospace';
      probCtx.fillText('Probability Density |ψₙ(x)|²', 10, 25);
      probCtx.fillStyle = '#fbbf24';
      probCtx.font = '11px monospace';
      probCtx.fillText('Yellow lines: Classical turning points', 10, 45);

      // === ENERGY LEVEL DIAGRAM ===
      const maxN = 8;

      // Draw potential well
      energyCtx.strokeStyle = '#ef4444';
      energyCtx.lineWidth = 2;
      energyCtx.beginPath();
      for (let x = 0; x < width; x++) {
        const xPos = (x - centerX) / scale;
        const V = 0.5 * omega * xPos * xPos;
        const y = height - 30 - V * 40;
        if (x === 0) {
          energyCtx.moveTo(x, y);
        } else {
          energyCtx.lineTo(x, y);
        }
      }
      energyCtx.stroke();

      // Draw energy levels
      for (let i = 0; i < maxN; i++) {
        const E = (i + 0.5) * omega;
        const y = height - 30 - E * 40;

        if (y < 20) continue;

        // Classical amplitude
        const amplitude = Math.sqrt(2 * E / omega) * scale;
        const x1 = centerX - amplitude;
        const x2 = centerX + amplitude;

        energyCtx.strokeStyle = i === n ? '#3b82f6' : 'rgba(59, 130, 246, 0.3)';
        energyCtx.lineWidth = i === n ? 2.5 : 1.5;
        energyCtx.setLineDash(i === n ? [] : [5, 5]);
        energyCtx.beginPath();
        energyCtx.moveTo(x1, y);
        energyCtx.lineTo(x2, y);
        energyCtx.stroke();

        // Label
        energyCtx.fillStyle = i === n ? '#3b82f6' : '#60a5fa';
        energyCtx.font = i === n ? 'bold 12px monospace' : '10px monospace';
        energyCtx.fillText(`n=${i}`, width - 80, y + 4);
        energyCtx.fillText(`E=${(i + 0.5).toFixed(1)}ℏω`, width - 50, y + 4);
      }
      energyCtx.setLineDash([]);

      // Labels
      energyCtx.fillStyle = '#10b981';
      energyCtx.font = '14px monospace';
      energyCtx.fillText('Energy Levels', 10, 25);
      energyCtx.fillStyle = '#34d399';
      energyCtx.font = '12px monospace';
      energyCtx.fillText('Eₙ = (n + ½)ℏω', 10, 45);
      energyCtx.fillText('Equal spacing!', 10, 60);

      // Ground state note
      if (n === 0) {
        energyCtx.fillStyle = '#fbbf24';
        energyCtx.font = '11px monospace';
        energyCtx.fillText('Zero-point energy: E₀ = ½ℏω ≠ 0', 10, height - 15);
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
  }, [quantumNumber, springConstant]);

  const energy = (quantumNumber + 0.5) * springConstant;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-blue-100 mb-2">Quantum Harmonic Oscillator</h2>
        <p className="text-blue-300/70 text-sm mb-4">
          A particle in a parabolic potential (like a mass on a spring). Energy levels are equally spaced, and ground state has non-zero energy.
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
            min={0}
            max={7}
            step={1}
            className="w-full"
          />
          <p className="text-blue-300/60 text-xs">
            n=0 is ground state with minimum energy ½ℏω
          </p>
        </div>

        <div className="space-y-3">
          <Label className="text-blue-200">Angular Frequency (ω): {springConstant.toFixed(1)}</Label>
          <Slider
            value={[springConstant]}
            onValueChange={(v) => setSpringConstant(v[0])}
            min={0.5}
            max={2}
            step={0.1}
            className="w-full"
          />
          <p className="text-blue-300/60 text-xs">
            Related to spring constant: ω = √(k/m)
          </p>
        </div>
      </div>

      <Card className="bg-blue-950/30 border-blue-500/20 p-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-blue-400/70">Energy</p>
            <p className="text-blue-100">Eₙ = {energy.toFixed(2)} ℏω</p>
          </div>
          <div>
            <p className="text-blue-400/70">Level Spacing</p>
            <p className="text-blue-100">ΔE = {springConstant.toFixed(2)} ℏω</p>
          </div>
          <div>
            <p className="text-blue-400/70">Nodes</p>
            <p className="text-blue-100">{quantumNumber}</p>
          </div>
          <div>
            <p className="text-blue-400/70">Classical Amplitude</p>
            <p className="text-blue-100">{Math.sqrt(2 * energy / springConstant).toFixed(2)}</p>
          </div>
        </div>
      </Card>
    </div>
  );
}
