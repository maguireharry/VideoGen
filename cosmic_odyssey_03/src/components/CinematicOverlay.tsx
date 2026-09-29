import React from 'react';
import { interpolate } from 'remotion';
import { ActConfig } from '../types';

interface CinematicOverlayProps {
  act: ActConfig;
  frame: number;
  durationInFrames: number;
  globalFrame: number;
  width: number;
  height: number;
}

export const CinematicOverlay: React.FC<CinematicOverlayProps> = ({
  act,
  frame,
  durationInFrames,
  globalFrame,
  width,
  height,
}) => {
  // Title animations: Title fades in from frame 15 to 45, remains visible until frame 180
  const titleOpacity = interpolate(
    frame,
    [15, 35, 160, 190],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  const titleY = interpolate(frame, [15, 45], [10, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Narration text animations: Fades in from frame 120 to 150, stays until frame 330
  const narrOpacity = interpolate(
    frame,
    [100, 130, 310, 340],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  // Timecode readout (MM:SS:FF)
  const totalSecs = Math.floor(globalFrame / 30);
  const frameRem = globalFrame % 30;
  const mins = String(Math.floor(totalSecs / 60)).padStart(2, '0');
  const secs = String(totalSecs % 60).padStart(2, '0');
  const framesStr = String(frameRem).padStart(2, '0');
  const timecode = `${mins}:${secs}:${framesStr}`;

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width,
        height,
        pointerEvents: 'none',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        fontFamily: "'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
      }}
    >
      {/* Top Cinematic Letterbox */}
      <div
        style={{
          width: '100%',
          height: 48,
          backgroundColor: 'rgba(0, 0, 0, 0.85)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 32px',
          boxSizing: 'border-box',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              backgroundColor: act.accentColor,
              boxShadow: `0 0 10px ${act.accentColor}`,
            }}
          />
          <span
            style={{
              fontSize: 12,
              letterSpacing: '0.25em',
              color: 'rgba(255, 255, 255, 0.7)',
              fontWeight: 600,
              textTransform: 'uppercase',
            }}
          >
            PROJECT 03 • THE SEED OF AURORA
          </span>
        </div>

        <div style={{ display: 'flex', gap: 24, fontSize: 11, color: 'rgba(255, 255, 255, 0.5)', letterSpacing: '0.15em' }}>
          <span>BLENDER • THREE.JS • NANO BANANA</span>
          <span style={{ color: act.accentColor, fontWeight: 'bold' }}>{timecode}</span>
        </div>
      </div>

      {/* Middle Center: Act Chapter Title & Subtitle */}
      <div
        style={{
          position: 'absolute',
          top: 90,
          left: 0,
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          opacity: titleOpacity,
          transform: `translateY(${titleY}px)`,
          textAlign: 'center',
        }}
      >
        <div
          style={{
            fontSize: 28,
            fontWeight: 800,
            letterSpacing: '0.35em',
            color: '#ffffff',
            textShadow: `0 0 20px ${act.accentColor}, 0 0 40px rgba(0,0,0,0.9)`,
            marginBottom: 6,
          }}
        >
          {act.title}
        </div>
        <div
          style={{
            fontSize: 12,
            letterSpacing: '0.3em',
            color: act.accentColor,
            fontWeight: 600,
            textTransform: 'uppercase',
            textShadow: '0 0 10px rgba(0,0,0,0.8)',
          }}
        >
          {act.subtitle}
        </div>
      </div>

      {/* Lower Center: Poetic Narration Subtitle */}
      <div
        style={{
          position: 'absolute',
          bottom: 70,
          left: 0,
          width: '100%',
          display: 'flex',
          justifyContent: 'center',
          opacity: narrOpacity,
          padding: '0 40px',
          boxSizing: 'border-box',
        }}
      >
        <div
          style={{
            maxWidth: 880,
            textAlign: 'center',
            fontSize: 19,
            fontWeight: 400,
            fontStyle: 'italic',
            letterSpacing: '0.08em',
            color: '#f8fafc',
            backgroundColor: 'rgba(15, 23, 42, 0.65)',
            backdropFilter: 'blur(8px)',
            padding: '10px 28px',
            borderRadius: 30,
            border: `1px solid ${act.accentColor}44`,
            boxShadow: `0 8px 32px rgba(0, 0, 0, 0.6), 0 0 15px ${act.accentColor}33`,
            textShadow: '0 2px 4px rgba(0,0,0,0.9)',
          }}
        >
          "{act.narration}"
        </div>
      </div>

      {/* Bottom Cinematic Letterbox */}
      <div
        style={{
          width: '100%',
          height: 48,
          backgroundColor: 'rgba(0, 0, 0, 0.85)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 32px',
          boxSizing: 'border-box',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)',
        }}
      >
        <span
          style={{
            fontSize: 11,
            letterSpacing: '0.2em',
            color: 'rgba(255, 255, 255, 0.4)',
          }}
        >
          COSMIC CHRONICLES • 60.0S CINEMA
        </span>

        <span
          style={{
            fontSize: 11,
            letterSpacing: '0.2em',
            color: 'rgba(255, 255, 255, 0.4)',
          }}
        >
          FRAME {globalFrame + 1} / 1800
        </span>
      </div>
    </div>
  );
};
