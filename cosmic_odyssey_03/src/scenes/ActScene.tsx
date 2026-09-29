import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { ActConfig } from '../types';
import { BackdropKenBurns } from '../components/BackdropKenBurns';
import { ThreeCanvasWrapper } from '../components/ThreeCanvasWrapper';
import { CinematicOverlay } from '../components/CinematicOverlay';

interface ActSceneProps {
  act: ActConfig;
  globalFrameOffset: number;
}

export const ActScene: React.FC<ActSceneProps> = ({ act, globalFrameOffset }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const globalFrame = globalFrameOffset + frame;

  return (
    <div
      style={{
        position: 'relative',
        width: '100%',
        height: '100%',
        backgroundColor: '#000000',
        overflow: 'hidden',
      }}
    >
      {/* 1. Base Layer: Nano Banana AI Cinematic Matte Painting (with Ken Burns motion) */}
      <BackdropKenBurns
        act={act}
        frame={frame}
        durationInFrames={act.durationInFrames}
        width={width}
        height={height}
      />

      {/* 2. Middle Layer: Three.js Real-Time 3D WebGL (Procedural Blender Seed & Particles) */}
      <ThreeCanvasWrapper
        frame={frame}
        fps={fps}
        act={act}
        width={width}
        height={height}
      />

      {/* 3. Top Layer: Remotion Cinematic Overlay (Kinetic Typography, Subtitles, HUD) */}
      <CinematicOverlay
        act={act}
        frame={frame}
        durationInFrames={act.durationInFrames}
        globalFrame={globalFrame}
        width={width}
        height={height}
      />
    </div>
  );
};
