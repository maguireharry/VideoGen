import React, { useMemo } from 'react';
import * as THREE from 'three';

interface ParticleVortexProps {
  frame: number;
  mode: 'vortex' | 'stream' | 'plasma' | 'shockwave' | 'spores';
  color: string;
}

const COUNT = 1500;

export const ParticleVortex3D: React.FC<ParticleVortexProps> = ({ frame, mode, color }) => {
  // Generate random base positions and speeds
  const { initialPositions, speeds, phases } = useMemo(() => {
    const pos = new Float32Array(COUNT * 3);
    const spd = new Float32Array(COUNT);
    const phs = new Float32Array(COUNT);

    for (let i = 0; i < COUNT; i++) {
      const idx = i * 3;
      // Spherical distribution
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);
      const r = 1.0 + Math.random() * 8.0;

      pos[idx] = r * Math.sin(phi) * Math.cos(theta);
      pos[idx + 1] = r * Math.sin(phi) * Math.sin(theta);
      pos[idx + 2] = r * Math.cos(phi);

      spd[i] = 0.5 + Math.random() * 1.5;
      phs[i] = Math.random() * Math.PI * 2;
    }
    return { initialPositions: pos, speeds: spd, phases: phs };
  }, []);

  // Compute animated positions based on current frame & mode
  const currentPositions = useMemo(() => {
    const pos = new Float32Array(COUNT * 3);
    const t = frame * 0.04;

    for (let i = 0; i < COUNT; i++) {
      const idx = i * 3;
      const x0 = initialPositions[idx];
      const y0 = initialPositions[idx + 1];
      const z0 = initialPositions[idx + 2];
      const speed = speeds[i];
      const phase = phases[i];

      if (mode === 'vortex') {
        // Spiral vortex rotation around Z/Y axis
        const angle = t * speed * 0.4 + phase;
        const rad = Math.sqrt(x0 * x0 + y0 * y0);
        pos[idx] = rad * Math.cos(angle);
        pos[idx + 1] = rad * Math.sin(angle);
        pos[idx + 2] = z0 + Math.sin(t + phase) * 0.5;
      } else if (mode === 'stream') {
        // Hyperspace stream: stars flying fast towards camera (+Z)
        pos[idx] = x0 * 1.5;
        pos[idx + 1] = y0 * 1.5;
        const zProg = (z0 + t * speed * 4.0) % 20.0;
        pos[idx + 2] = zProg - 10.0;
      } else if (mode === 'plasma') {
        // Violent plasma trail: downward thrust with high jitter
        pos[idx] = x0 * 0.6 + Math.sin(t * 3.0 + phase) * 0.3;
        pos[idx + 1] = ((y0 - t * speed * 3.0) % 15.0) - 5.0;
        pos[idx + 2] = z0 * 0.6;
      } else if (mode === 'shockwave') {
        // Concentric expanding ground rings
        const waveProgress = ((t * speed * 0.8) % 1.0);
        const radius = waveProgress * 12.0;
        const ringAngle = phase;
        pos[idx] = radius * Math.cos(ringAngle);
        pos[idx + 1] = -1.5 + Math.sin(ringAngle * 4.0) * 0.2;
        pos[idx + 2] = radius * Math.sin(ringAngle);
      } else {
        // 'spores': Gentle upward floating dandelion light spores
        pos[idx] = x0 + Math.sin(t * 0.5 + phase) * 0.8;
        pos[idx + 1] = ((y0 + t * speed * 0.8) % 16.0) - 8.0;
        pos[idx + 2] = z0 + Math.cos(t * 0.5 + phase) * 0.8;
      }
    }
    return pos;
  }, [frame, mode, initialPositions, speeds, phases]);

  return (
    <points>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          args={[currentPositions, 3]}
        />
      </bufferGeometry>
      <pointsMaterial
        size={mode === 'stream' ? 0.08 : 0.06}
        color={color}
        transparent={true}
        opacity={0.85}
        blending={THREE.AdditiveBlending}
        depthWrite={false}
      />
    </points>
  );
};
