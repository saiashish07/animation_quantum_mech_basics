import { useEffect, useRef, useState } from 'react';
import { motion } from 'motion/react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Label } from './ui/label';

type OrbitalType = '1s' | '2s' | '2p' | '3s' | '3p' | '3d';

export function AtomicOrbitals() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [orbital, setOrbital] = useState<OrbitalType>('1s');
  const animationRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    let angle = 0;

    // Simplified orbital wave functions
    const getOrbitalProbability = (r: number, theta: number, phi: number, type: OrbitalType) => {
      const a0 = 50; // Bohr radius in pixels

      switch (type) {
        case '1s':
          return Math.exp(-2 * r / a0);
        case '2s':
          return (1 - r / a0) * Math.exp(-r / a0);
        case '2p':
          return (r / a0) * Math.exp(-r / (2 * a0)) * Math.abs(Math.cos(theta));
        case '3s':
          return (1 - 2 * r / (3 * a0) + 2 * r * r / (27 * a0 * a0)) * Math.exp(-r / (3 * a0));
        case '3p':
          return (r / a0) * (1 - r / (6 * a0)) * Math.exp(-r / (3 * a0)) * Math.abs(Math.cos(theta));
        case '3d':
          return (r * r / (a0 * a0)) * Math.exp(-r / (3 * a0)) * Math.pow(Math.sin(theta), 2) * Math.abs(Math.cos(2 * phi));
        default:
          return 0;
      }
    };

    const animate = () => {
      ctx.fillStyle = 'rgba(15, 23, 42, 0.1)';
      ctx.fillRect(0, 0, width, height);

      // Draw nucleus
      ctx.fillStyle = '#ef4444';
      ctx.beginPath();
      ctx.arc(centerX, centerY, 8, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#fca5a5';
      ctx.fillText('⊕', centerX - 5, centerY + 5);

      // Draw orbital probability cloud
      const samples = 3000;
      for (let i = 0; i < samples; i++) {
        const r = Math.random() * 150;
        const theta = Math.random() * Math.PI;
        const phi = Math.random() * 2 * Math.PI + angle;

        const probability = getOrbitalProbability(r, theta, phi, orbital);

        if (Math.random() < probability) {
          // Convert spherical to Cartesian coordinates
          const x = centerX + r * Math.sin(theta) * Math.cos(phi);
          const y = centerY + r * Math.sin(theta) * Math.sin(phi);
          const z = r * Math.cos(theta);

          // Color based on z-depth
          const brightness = (z + 150) / 300;
          const alpha = probability * 0.3;

          // Different colors for different orbitals
          let color;
          switch (orbital) {
            case '1s':
            case '2s':
            case '3s':
              color = `rgba(96, 165, 250, ${alpha})`;
              break;
            case '2p':
            case '3p':
              color = `rgba(139, 92, 246, ${alpha})`;
              break;
            case '3d':
              color = `rgba(236, 72, 153, ${alpha})`;
              break;
            default:
              color = `rgba(96, 165, 250, ${alpha})`;
          }

          ctx.fillStyle = color;
          const size = brightness * 2 + 1;
          ctx.beginPath();
          ctx.arc(x, y, size, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // Draw orbital axes
      ctx.strokeStyle = 'rgba(59, 130, 246, 0.3)';
      ctx.lineWidth = 1;
      ctx.setLineDash([5, 5]);
      
      // X axis
      ctx.beginPath();
      ctx.moveTo(centerX - 180, centerY);
      ctx.lineTo(centerX + 180, centerY);
      ctx.stroke();
      
      // Y axis
      ctx.beginPath();
      ctx.moveTo(centerX, centerY - 180);
      ctx.lineTo(centerX, centerY + 180);
      ctx.stroke();
      
      ctx.setLineDash([]);

      // Draw orbital lobes for p and d orbitals
      if (orbital.includes('p') || orbital.includes('d')) {
        ctx.strokeStyle = 'rgba(139, 92, 246, 0.5)';
        ctx.lineWidth = 2;
        
        if (orbital.includes('p')) {
          // Draw p-orbital lobes
          ctx.beginPath();
          for (let t = 0; t < Math.PI * 2; t += 0.1) {
            const r = 80 * Math.abs(Math.cos(t));
            const x = centerX + r * Math.cos(t + angle);
            const y = centerY + r * Math.sin(t + angle);
            if (t === 0) {
              ctx.moveTo(x, y);
            } else {
              ctx.lineTo(x, y);
            }
          }
          ctx.stroke();
        }
      }

      // Labels
      ctx.fillStyle = '#3b82f6';
      ctx.fillText(`Orbital: ${orbital.toUpperCase()}`, 20, 30);
      ctx.fillStyle = '#8b5cf6';
      ctx.fillText(`n = ${orbital[0]}, l = ${orbital === '1s' || orbital === '2s' || orbital === '3s' ? '0' : orbital.includes('p') ? '1' : '2'}`, 20, 50);
      ctx.fillStyle = '#60a5fa';
      const orbitalNames: Record<OrbitalType, string> = {
        '1s': 'ψ₁ₛ = (1/πa₀³)^(1/2) · e^(-r/a₀)',
        '2s': 'ψ₂ₛ = (1/32πa₀³)^(1/2) · (2-r/a₀) · e^(-r/2a₀)',
        '2p': 'ψ₂ₚ = (1/32πa₀³)^(1/2) · (r/a₀) · e^(-r/2a₀) · cosθ',
        '3s': 'ψ₃ₛ = (1/243πa₀³)^(1/2) · (27-18r/a₀+2r²/a₀²) · e^(-r/3a₀)',
        '3p': 'ψ₃ₚ = (√2/81√π a₀³)^(1/2) · (6-r/a₀)(r/a₀) · e^(-r/3a₀) · cosθ',
        '3d': 'ψ₃ₐ = (1/81√6π a₀³)^(1/2) · (r²/a₀²) · e^(-r/3a₀) · sin²θ · cos2φ'
      };
      ctx.fillText(orbitalNames[orbital], 20, height - 20);

      angle += 0.01;
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [orbital]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div>
        <h2 className="text-blue-100 mb-2">Atomic Orbitals</h2>
        <p className="text-blue-300/70 text-sm">
          Electron probability density distributions | ψₙₗₘ(r,θ,φ) solutions
        </p>
      </div>

      <canvas
        ref={canvasRef}
        width={800}
        height={400}
        className="w-full border border-blue-500/30 rounded-lg bg-slate-950/50"
      />

      <div className="space-y-2">
        <Label className="text-blue-200">Select Orbital:</Label>
        <Select value={orbital} onValueChange={(v) => setOrbital(v as OrbitalType)}>
          <SelectTrigger className="w-full bg-slate-900/50 border-blue-500/20 text-blue-100">
            <SelectValue />
          </SelectTrigger>
          <SelectContent className="bg-slate-900 border-blue-500/20">
            <SelectItem value="1s">1s (n=1, l=0)</SelectItem>
            <SelectItem value="2s">2s (n=2, l=0)</SelectItem>
            <SelectItem value="2p">2p (n=2, l=1)</SelectItem>
            <SelectItem value="3s">3s (n=3, l=0)</SelectItem>
            <SelectItem value="3p">3p (n=3, l=1)</SelectItem>
            <SelectItem value="3d">3d (n=3, l=2)</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </motion.div>
  );
}
