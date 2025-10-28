import { useEffect, useRef, useState } from 'react';
import { motion } from 'motion/react';
import { Slider } from './ui/slider';
import { Label } from './ui/label';

export function WaveFunction() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [frequency, setFrequency] = useState(2);
  const [amplitude, setAmplitude] = useState(50);
  const [phase, setPhase] = useState(0);
  const animationRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;
    let time = 0;

    const animate = () => {
      ctx.fillStyle = 'rgba(15, 23, 42, 0.1)';
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

      // Draw wave function (real part)
      ctx.beginPath();
      ctx.strokeStyle = '#3b82f6';
      ctx.lineWidth = 2;
      for (let x = 0; x < width; x++) {
        const k = (frequency * 2 * Math.PI) / width;
        const omega = frequency * 0.1;
        const y = height / 2 + amplitude * Math.sin(k * x - omega * time + phase);
        if (x === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }
      ctx.stroke();

      // Draw probability density |ψ|²
      ctx.beginPath();
      ctx.strokeStyle = '#8b5cf6';
      ctx.lineWidth = 2;
      ctx.globalAlpha = 0.6;
      for (let x = 0; x < width; x++) {
        const k = (frequency * 2 * Math.PI) / width;
        const omega = frequency * 0.1;
        const psi = Math.sin(k * x - omega * time + phase);
        const probability = psi * psi;
        const y = height / 2 + amplitude * probability;
        if (x === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }
      ctx.stroke();
      ctx.globalAlpha = 1;

      // Draw particles at high probability positions
      ctx.fillStyle = '#60a5fa';
      for (let x = 0; x < width; x += 10) {
        const k = (frequency * 2 * Math.PI) / width;
        const omega = frequency * 0.1;
        const psi = Math.sin(k * x - omega * time + phase);
        const probability = psi * psi;
        
        if (Math.random() < probability) {
          ctx.beginPath();
          ctx.arc(x, height / 2, 2, 0, Math.PI * 2);
          ctx.fill();
        }
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
  }, [frequency, amplitude, phase]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div>
        <h2 className="text-blue-100 mb-2">Wave Function Visualization</h2>
        <p className="text-blue-300/70 text-sm">
          ψ(x,t) = A·sin(kx - ωt + φ) | Blue: Real part, Purple: Probability density |ψ|²
        </p>
      </div>

      <canvas
        ref={canvasRef}
        width={800}
        height={400}
        className="w-full border border-blue-500/30 rounded-lg bg-slate-950/50"
      />

      <div className="grid grid-cols-3 gap-6">
        <div className="space-y-2">
          <Label className="text-blue-200">Frequency (ω): {frequency}</Label>
          <Slider
            value={[frequency]}
            onValueChange={(v) => setFrequency(v[0])}
            min={1}
            max={8}
            step={0.5}
            className="w-full"
          />
        </div>
        <div className="space-y-2">
          <Label className="text-blue-200">Amplitude (A): {amplitude}</Label>
          <Slider
            value={[amplitude]}
            onValueChange={(v) => setAmplitude(v[0])}
            min={20}
            max={100}
            step={5}
            className="w-full"
          />
        </div>
        <div className="space-y-2">
          <Label className="text-blue-200">Phase (φ): {phase.toFixed(2)}</Label>
          <Slider
            value={[phase]}
            onValueChange={(v) => setPhase(v[0])}
            min={0}
            max={Math.PI * 2}
            step={0.1}
            className="w-full"
          />
        </div>
      </div>
    </motion.div>
  );
}
