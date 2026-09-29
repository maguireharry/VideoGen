import React from 'react';
import { Audio, Sequence, staticFile, useCurrentFrame, interpolate } from 'remotion';
import { ACTS } from './types';
import { ActScene } from './scenes/ActScene';

export const CosmicOdysseyComposition: React.FC = () => {
  const frame = useCurrentFrame();

  // Final fade-out to black at 58.5s - 60.0s (frames 1755 - 1800)
  const masterFadeOut = interpolate(
    frame,
    [1740, 1795],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <div
      style={{
        flex: 1,
        width: '100%',
        height: '100%',
        backgroundColor: '#000000',
        position: 'relative',
      }}
    >
      {/* 60.0s Master Audio Soundtrack */}
      <Audio src={staticFile('audio/cosmic_soundtrack.wav')} />

      {/* 5 Narrative Acts */}
      {ACTS.map((act) => (
        <Sequence
          key={act.actIndex}
          from={act.startFrame}
          durationInFrames={act.durationInFrames}
        >
          <ActScene act={act} globalFrameOffset={act.startFrame} />
        </Sequence>
      ))}

      {/* Master Final Fade to Black */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundColor: '#000000',
          opacity: masterFadeOut,
          pointerEvents: 'none',
        }}
      />
    </div>
  );
};
