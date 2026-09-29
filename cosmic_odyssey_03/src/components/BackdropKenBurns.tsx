import React from 'react';
import { Img, interpolate, staticFile } from 'remotion';
import { ActConfig } from '../types';

interface BackdropKenBurnsProps {
  act: ActConfig;
  frame: number;
  durationInFrames: number;
  width: number;
  height: number;
}

export const BackdropKenBurns: React.FC<BackdropKenBurnsProps> = ({
  act,
  frame,
  durationInFrames,
  width,
  height,
}) => {
  // Cinematic slow zoom & drift
  const zoom = interpolate(frame, [0, durationInFrames], [1.0, 1.12], {
    extrapolateRight: 'clamp',
  });
  const panX = interpolate(frame, [0, durationInFrames], [-1.5, 1.5], {
    extrapolateRight: 'clamp',
  });
  const panY = interpolate(frame, [0, durationInFrames], [1.0, -1.0], {
    extrapolateRight: 'clamp',
  });

  // Fade-in at start of act (first 15 frames) and fade-out at end (last 15 frames)
  const fadeIn = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });
  const fadeOut = interpolate(
    frame,
    [durationInFrames - 15, durationInFrames],
    [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  const opacity = Math.min(fadeIn, fadeOut);

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width,
        height,
        overflow: 'hidden',
        backgroundColor: '#030712',
      }}
    >
      <Img
        src={staticFile(act.backdropImage)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `scale(${zoom}) translate(${panX}%, ${panY}%)`,
          opacity,
          filter: 'contrast(1.08) brightness(0.95)',
        }}
      />
    </div>
  );
};
