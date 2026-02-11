import React, { useMemo } from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { getColorsForCategory } from "../lib/colors";

// Generate consistent particle positions based on seed
function seededRandom(seed: number) {
  const x = Math.sin(seed * 9999) * 10000;
  return x - Math.floor(x);
}

interface Particle {
  x: number;
  y: number;
  size: number;
  speed: number;
  opacity: number;
}

export const Background: React.FC<{ category: string }> = ({ category }) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();
  const colors = getColorsForCategory(category);

  // Generate particles once
  const particles = useMemo<Particle[]>(() => {
    return Array.from({ length: 20 }, (_, i) => ({
      x: seededRandom(i * 1) * 100,
      y: seededRandom(i * 2) * 100,
      size: 2 + seededRandom(i * 3) * 4,
      speed: 0.3 + seededRandom(i * 4) * 0.7,
      opacity: 0.1 + seededRandom(i * 5) * 0.3,
    }));
  }, []);

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
      {/* Floating particles */}
      {particles.map((p, i) => {
        const yOffset = (frame * p.speed) % 120;
        const yPos = ((p.y + yOffset) % 120) - 10;
        const pulse = 0.7 + 0.3 * Math.sin((frame + i * 10) * 0.08);
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: `${p.x}%`,
              top: `${yPos}%`,
              width: p.size,
              height: p.size,
              borderRadius: "50%",
              backgroundColor: "rgba(255,255,255,0.8)",
              opacity: p.opacity * pulse,
              boxShadow: `0 0 ${p.size * 2}px rgba(255,255,255,0.5)`,
            }}
          />
        );
      })}
      {/* Light flare overlay */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(ellipse at 50% 30%, rgba(255,255,255,0.08) 0%, transparent 60%)",
        }}
      />
      {/* Vignette */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.65) 100%)",
        }}
      />
    </AbsoluteFill>
  );
};
