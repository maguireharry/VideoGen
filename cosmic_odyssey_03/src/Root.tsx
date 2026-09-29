import React from 'react';
import { Composition } from 'remotion';
import { CosmicOdysseyComposition } from './Composition';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="CosmicOdyssey"
      component={CosmicOdysseyComposition}
      durationInFrames={1800} // Exactly 60.0 seconds @ 30 FPS
      fps={30}
      width={1280}
      height={720}
    />
  );
};
