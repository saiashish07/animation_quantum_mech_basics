import { useEffect, useRef, useState } from 'react';
import { motion } from 'motion/react';
import { Button } from './ui/button';
import { Label } from './ui/label';

export function DoubleSlit() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isObserving, setIsObserving] = useState(false);
  const [detections, setDetections] = useState<Array<{x: number, y: number}>>([]);
  const animationRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;
    const slitX = 200;
    const screenX = 600;
    const slit1Y = height / 2 - 60;
    const slit2Y = height / 2 + 60;
    const slitWidth = 10;
    const slitHeight = 40;

    let particles: Array<{
      x: number;
      y: number;
      vx: number;
      vy: number;
      slit?: number;
      wave?: boolean;
    }> = [];

    const animate = () => {
      ctx.fillStyle = 'rgba(15, 23, 42, 0.05)';
      ctx.fillRect(0, 0, width, height);

      // Draw barrier with slits
      ctx.fillStyle = '#1e293b';
      ctx.fillRect(slitX, 0, 20, slit1Y - slitHeight / 2);
      ctx.fillRect(slitX, slit1Y + slitHeight / 2, 20, slit2Y - slit1Y - slitHeight);
      ctx.fillRect(slitX, slit2Y + slitHeight / 2, 20, height - slit2Y - slitHeight / 2);

      ctx.strokeStyle = '#3b82f6';
      ctx.lineWidth = 2;
      ctx.strokeRect(slitX, slit1Y - slitHeight / 2, 20, slitHeight);
      ctx.strokeRect(slitX, slit2Y - slitHeight / 2, 20, slitHeight);

      // Draw detection screen
      ctx.strokeStyle = '#8b5cf6';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(screenX, 0);
      ctx.lineTo(screenX, height);
      ctx.stroke();

      // Emit particles
      if (Math.random() < 0.1) {
        particles.push({
          x: 50,
          y: height / 2 + (Math.random() - 0.5) * 100,
          vx: 3,
          vy: 0,
          wave: !isObserving
        });
      }

      // Update particles
      particles = particles.filter(p => {
        p.x += p.vx;
        p.y += p.vy;

        // Check if particle reaches slits
        if (p.x >= slitX && p.x <= slitX + 20 && !p.slit) {
          if (!isObserving) {
            // Wave behavior - goes through both slits
            if (Math.abs(p.y - slit1Y) < slitHeight / 2 || Math.abs(p.y - slit2Y) < slitHeight / 2) {
              p.slit = Math.random() < 0.5 ? 1 : 2;
            } else {
              return false; // Absorbed by barrier
            }
          } else {
            // Particle behavior - goes through one slit
            const dist1 = Math.abs(p.y - slit1Y);
            const dist2 = Math.abs(p.y - slit2Y);
            
            if (dist1 < slitHeight / 2) {
              p.slit = 1;
              p.vy = (Math.random() - 0.5) * 0.5;
            } else if (dist2 < slitHeight / 2) {
              p.slit = 2;
              p.vy = (Math.random() - 0.5) * 0.5;
            } else {
              return false; // Absorbed by barrier
            }
          }
        }

        // Apply interference if wave behavior
        if (p.slit && !isObserving && p.x > slitX + 20) {
          const d1 = Math.sqrt(Math.pow(p.x - slitX, 2) + Math.pow(p.y - slit1Y, 2));
          const d2 = Math.sqrt(Math.pow(p.x - slitX, 2) + Math.pow(p.y - slit2Y, 2));
          const pathDiff = d2 - d1;
          const wavelength = 30;
          const phase = (pathDiff / wavelength) * 2 * Math.PI;
          const interference = Math.cos(phase);
          
          // Affect trajectory based on interference
          p.vy += interference * 0.01;
        }

        // Check if reached screen
        if (p.x >= screenX) {
          const newDetections = [...detections, {x: screenX, y: p.y}];
          if (newDetections.length > 500) {
            newDetections.shift();
          }
          setDetections(newDetections);
          return false;
        }

        // Draw particle
        if (p.wave && p.slit) {
          // Draw as wave
          ctx.globalAlpha = 0.3;
          ctx.strokeStyle = p.slit === 1 ? '#60a5fa' : '#8b5cf6';
          ctx.lineWidth = 1;
          ctx.beginPath();
          for (let i = -15; i < 15; i++) {
            const waveX = p.x + i * 2;
            const waveY = p.y + Math.sin(i * 0.3 + p.x * 0.1) * 8;
            if (i === -15) {
              ctx.moveTo(waveX, waveY);
            } else {
              ctx.lineTo(waveX, waveY);
            }
          }
          ctx.stroke();
          ctx.globalAlpha = 1;
        } else {
          ctx.fillStyle = p.slit === 1 ? '#60a5fa' : '#8b5cf6';
          ctx.beginPath();
          ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
          ctx.fill();
        }

        return p.x < width;
      });

      // Draw detections on screen
      detections.forEach(d => {
        ctx.fillStyle = 'rgba(96, 165, 250, 0.5)';
        ctx.beginPath();
        ctx.arc(d.x, d.y, 2, 0, Math.PI * 2);
        ctx.fill();
      });

      // Draw interference pattern histogram
      if (detections.length > 0) {
        const bins = 40;
        const binHeight = height / bins;
        const histogram = new Array(bins).fill(0);
        
        detections.forEach(d => {
          const bin = Math.floor(d.y / binHeight);
          if (bin >= 0 && bin < bins) {
            histogram[bin]++;
          }
        });

        const maxCount = Math.max(...histogram, 1);
        ctx.fillStyle = 'rgba(139, 92, 246, 0.6)';
        histogram.forEach((count, i) => {
          const barWidth = (count / maxCount) * 80;
          ctx.fillRect(screenX + 10, i * binHeight, barWidth, binHeight - 1);
        });
      }

      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isObserving, detections]);

  const handleReset = () => {
    setDetections([]);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div>
        <h2 className="text-blue-100 mb-2">Double Slit Experiment</h2>
        <p className="text-blue-300/70 text-sm">
          Wave-particle duality demonstration | I(θ) ∝ cos²(πd·sinθ/λ)
        </p>
      </div>

      <canvas
        ref={canvasRef}
        width={800}
        height={400}
        className="w-full border border-blue-500/30 rounded-lg bg-slate-950/50"
      />

      <div className="flex gap-4 items-center">
        <Label className="text-blue-200">Observer Effect:</Label>
        <Button
          onClick={() => setIsObserving(!isObserving)}
          variant={isObserving ? "default" : "outline"}
          className={isObserving ? "bg-red-600 hover:bg-red-700" : "bg-blue-600 hover:bg-blue-700"}
        >
          {isObserving ? '👁️ Observing (Particle)' : '🌊 Not Observing (Wave)'}
        </Button>
        <Button onClick={handleReset} variant="outline">
          Reset Detections
        </Button>
        <span className="text-blue-300/70 text-sm ml-auto">
          Detections: {detections.length}
        </span>
      </div>
    </motion.div>
  );
}
