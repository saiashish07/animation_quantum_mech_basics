import { useEffect, useRef, useState } from 'react';
import { motion } from 'motion/react';
import { Slider } from './ui/slider';
import { Label } from './ui/label';

export function SchrodingerEquation() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [potentialType, setPotentialType] = useState(1);
  const animationRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;
    let time = 0;

    // Solve time-dependent Schrödinger equation (simplified)
    const wavePacket = (x: number, t: number, k0: number, sigma: number) => {
      const x0 = 0.5;
      const omega = (k0 * k0) / 2;
      const exponent = -Math.pow(x - x0 - k0 * t * 0.001, 2) / (2 * sigma * sigma);
      const phase = k0 * x - omega * t * 0.01;
      return Math.exp(exponent) * Math.cos(phase);
    };

    const getPotential = (x: number) => {
      switch (potentialType) {
        case 1: // Harmonic oscillator
          return 50 * Math.pow(x - 0.5, 2);
        case 2: // Square barrier
          return (x > 0.4 && x < 0.6) ? 0.15 : 0;
        case 3: // Double well
          return 50 * Math.pow(Math.pow(x - 0.5, 2) - 0.02, 2);
        default:
          return 0;
      }
    };

    const animate = () => {
      ctx.fillStyle = 'rgba(15, 23, 42, 0.95)';
      ctx.fillRect(0, 0, width, height);

      // Draw grid
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

      // Draw potential V(x)
      ctx.beginPath();
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 2;
      for (let x = 0; x < width; x++) {
        const xNorm = x / width;
        const V = getPotential(xNorm);
        const y = height - 50 - V * 1000;
        if (x === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }
      ctx.stroke();

      // Draw wave function ψ(x,t)
      ctx.beginPath();
      ctx.strokeStyle = '#3b82f6';
      ctx.lineWidth = 2;
      for (let x = 0; x < width; x++) {
        const xNorm = x / width;
        const psi = wavePacket(xNorm, time, 20, 0.05);
        const y = height - 50 - psi * 100;
        if (x === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }
      ctx.stroke();

      // Draw probability density |ψ|²
      ctx.fillStyle = 'rgba(139, 92, 246, 0.3)';
      ctx.beginPath();
      ctx.moveTo(0, height - 50);
      for (let x = 0; x < width; x++) {
        const xNorm = x / width;
        const psi = wavePacket(xNorm, time, 20, 0.05);
        const probability = psi * psi;
        const y = height - 50 - probability * 200;
        ctx.lineTo(x, y);
      }
      ctx.lineTo(width, height - 50);
      ctx.closePath();
      ctx.fill();

      // Draw imaginary part
      ctx.beginPath();
      ctx.strokeStyle = '#8b5cf6';
      ctx.lineWidth = 1;
      ctx.globalAlpha = 0.5;
      for (let x = 0; x < width; x++) {
        const xNorm = x / width;
        const x0 = 0.5;
        const sigma = 0.05;
        const k0 = 20;
        const omega = (k0 * k0) / 2;
        const exponent = -Math.pow(xNorm - x0 - k0 * time * 0.001, 2) / (2 * sigma * sigma);
        const phase = k0 * xNorm - omega * time * 0.01;
        const psiIm = Math.exp(exponent) * Math.sin(phase);
        const y = height - 50 - psiIm * 100;
        if (x === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }
      ctx.stroke();
      ctx.globalAlpha = 1;

      // Labels
      ctx.fillStyle = '#3b82f6';
      ctx.fillText('Re[ψ(x,t)]', 10, 30);
      ctx.fillStyle = '#8b5cf6';
      ctx.fillText('Im[ψ(x,t)]', 10, 50);
      ctx.fillStyle = '#a78bfa';
      ctx.fillText('|ψ(x,t)|²', 10, 70);
      ctx.fillStyle = '#ef4444';
      ctx.fillText('V(x)', 10, 90);

      // Equation
      ctx.fillStyle = '#60a5fa';
      ctx.fillText('iℏ∂ψ/∂t = -ℏ²/2m ∂²ψ/∂x² + V(x)ψ', width / 2 - 120, 30);

      time += 1;
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [potentialType]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div>
        <h2 className="text-blue-100 mb-2">Time-Dependent Schrödinger Equation</h2>
        <p className="text-blue-300/70 text-sm">
          Wave packet evolution in different potentials
        </p>
      </div>

      <canvas
        ref={canvasRef}
        width={800}
        height={400}
        className="w-full border border-blue-500/30 rounded-lg bg-slate-950/50"
      />

      <div className="space-y-2">
        <Label className="text-blue-200">Potential Type:</Label>
        <div className="flex gap-2">
          <motion.button
            onClick={() => setPotentialType(1)}
            className={`px-4 py-2 rounded-lg border transition-colors ${
              potentialType === 1
                ? 'bg-blue-600 border-blue-400 text-blue-100'
                : 'bg-slate-900/50 border-blue-500/20 text-blue-300/70'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Harmonic Oscillator
          </motion.button>
          <motion.button
            onClick={() => setPotentialType(2)}
            className={`px-4 py-2 rounded-lg border transition-colors ${
              potentialType === 2
                ? 'bg-blue-600 border-blue-400 text-blue-100'
                : 'bg-slate-900/50 border-blue-500/20 text-blue-300/70'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Square Barrier
          </motion.button>
          <motion.button
            onClick={() => setPotentialType(3)}
            className={`px-4 py-2 rounded-lg border transition-colors ${
              potentialType === 3
                ? 'bg-blue-600 border-blue-400 text-blue-100'
                : 'bg-slate-900/50 border-blue-500/20 text-blue-300/70'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Double Well
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
}
