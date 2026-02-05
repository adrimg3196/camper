import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { getColorsForCategory } from "../lib/colors";

export const Background: React.FC<{ category: string }> = ({ category }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const colors = getColorsForCategory(category);

  // Slowly rotate the gradient angle
  const angle = interpolate(frame, [0, durationInFrames], [135, 165], {
    extrapolateRight: "clamp",
  });

  // Subtle scale animation on background
  const scale = interpolate(frame, [0, durationInFrames], [1.0, 1.15], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill>
      {/* Base dark layer */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundColor: "#0a0a0a",
        }}
      />
      {/* Animated gradient */}
      <div
        style={{
          position: "absolute",
          inset: "-15%",
          background: `linear-gradient(${angle}deg, ${colors.from} 0%, ${colors.via} 45%, ${colors.to} 100%)`,
          transform: `scale(${scale})`,
          opacity: 0.85,
        }}
      />
      {/* Noise/texture overlay */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(ellipse at 50% 30%, rgba(255,255,255,0.05) 0%, transparent 70%)",
        }}
      />
      {/* Vignette */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.6) 100%)",
        }}
      />
    </AbsoluteFill>
  );
};
