import { useEffect, useRef, useState } from 'react';
import { motion } from 'motion/react';
import { Slider } from './ui/slider';
import { Label } from './ui/label';
import { Button } from './ui/button';

export function ParticleBox() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [energyLevel, setEnergyLevel] = useState(1);
  const [isAnimating, setIsAnimating] = useState(true);
  const animationRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;
    const boxWidth = 600;
    const boxHeight = 300;
    const boxX = (width - boxWidth) / 2;
    const boxY = (height - boxHeight) / 2;
    let time = 0;

    const animate = () => {
      ctx.fillStyle = 'rgba(15, 23, 42, 0.95)';
      ctx.fillRect(0, 0, width, height);

      // Draw the box
      ctx.strokeStyle = '#3b82f6';
      ctx.lineWidth = 3;
      ctx.strokeRect(boxX, boxY, boxWidth, boxHeight);

      // Draw energy levels
      ctx.strokeStyle = 'rgba(59, 130, 246, 0.3)';
      ctx.lineWidth = 1;
      ctx.setLineDash([5, 5]);
      for (let n = 1; n <= 5; n++) {
        const energyY = boxY + boxHeight - (boxHeight / 6) * n;
        ctx.beginPath();
        ctx.moveTo(boxX, energyY);
        ctx.lineTo(boxX + boxWidth, energyY);
        ctx.stroke();
        
        // Label energy level
        ctx.fillStyle = '#60a5fa';
        ctx.setLineDash([]);
        ctx.fillText(`n=${n}`, boxX - 40, energyY + 5);
        ctx.setLineDash([5, 5]);
      }
      ctx.setLineDash([]);

      // Wave function for particle in a box: ψ(x) = √(2/L) * sin(nπx/L)
      const n = energyLevel;
      ctx.beginPath();
      ctx.strokeStyle = '#8b5cf6';
      ctx.lineWidth = 2;

      for (let x = 0; x <= boxWidth; x++) {
        const xNorm = x / boxWidth;
        const psi = Math.sqrt(2) * Math.sin(n * Math.PI * xNorm);
        const y = boxY + boxHeight / 2 - psi * 60 * Math.cos(time * 0.02);
        
        if (x === 0) {
          ctx.moveTo(boxX + x, y);
        } else {
          ctx.lineTo(boxX + x, y);
        }
      }
      ctx.stroke();

      // Draw probability density
      ctx.fillStyle = 'rgba(139, 92, 246, 0.2)';
      ctx.beginPath();
      ctx.moveTo(boxX, boxY + boxHeight / 2);
      for (let x = 0; x <= boxWidth; x++) {
        const xNorm = x / boxWidth;
        const psi = Math.sqrt(2) * Math.sin(n * Math.PI * xNorm);
        const probability = psi * psi;
        const y = boxY + boxHeight / 2 - probability * 80;
        ctx.lineTo(boxX + x, y);
      }
      ctx.lineTo(boxX + boxWidth, boxY + boxHeight / 2);
      ctx.closePath();
      ctx.fill();

      // Draw particles
      ctx.fillStyle = '#60a5fa';
      for (let i = 0; i < 100; i++) {
        const x = (Math.random() * boxWidth);
        const xNorm = x / boxWidth;
        const psi = Math.sqrt(2) * Math.sin(n * Math.PI * xNorm);
        const probability = psi * psi / 2;
        
        if (Math.random() < probability) {
          ctx.beginPath();
          ctx.arc(
            boxX + x,
            boxY + boxHeight / 2 + (Math.random() - 0.5) * 40,
            2,
            0,
            Math.PI * 2
          );
          ctx.fill();
        }
      }

      // Display energy
      ctx.fillStyle = '#3b82f6';
      ctx.fillText(`E${n} = (n²π²ℏ²)/(2mL²)`, boxX, boxY - 20);

      if (isAnimating) {
        time += 1;
      }
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [energyLevel, isAnimating]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div>
        <h2 className="text-blue-100 mb-2">Particle in a Box</h2>
        <p className="text-blue-300/70 text-sm">
          Infinite square well potential | ψₙ(x) = √(2/L)·sin(nπx/L)
        </p>
      </div>

      <canvas
        ref={canvasRef}
        width={800}
        height={400}
        className="w-full border border-blue-500/30 rounded-lg bg-slate-950/50"
      />

      <div className="flex gap-6 items-end">
        <div className="flex-1 space-y-2">
          <Label className="text-blue-200">Quantum Number (n): {energyLevel}</Label>
          <Slider
            value={[energyLevel]}
            onValueChange={(v) => setEnergyLevel(v[0])}
            min={1}
            max={5}
            step={1}
            className="w-full"
          />
        </div>
        <Button
          onClick={() => setIsAnimating(!isAnimating)}
          variant={isAnimating ? "default" : "outline"}
          className="bg-blue-600 hover:bg-blue-700"
        >
          {isAnimating ? 'Pause' : 'Play'}
        </Button>
      </div>
    </motion.div>
  );
}
