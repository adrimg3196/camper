import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Outfit";

const { fontFamily } = loadFont();

export const CallToAction: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance animation
  const entrance = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  const translateY = interpolate(entrance, [0, 1], [30, 0]);
  const opacity = interpolate(entrance, [0, 0.5], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Pulsing glow effect
  const pulse = interpolate(
    Math.sin(frame * 0.12),
    [-1, 1],
    [0.85, 1.0],
  );

  const glowIntensity = interpolate(
    Math.sin(frame * 0.12),
    [-1, 1],
    [10, 25],
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 220,
      }}
    >
      <div
        style={{
          transform: `translateY(${translateY}px) scale(${pulse})`,
          opacity,
        }}
      >
        <div
          style={{
            background: "linear-gradient(135deg, #22c55e 0%, #16a34a 100%)",
            padding: "18px 48px",
            borderRadius: 60,
            boxShadow: `0 0 ${glowIntensity}px rgba(34,197,94,0.5), 0 4px 15px rgba(0,0,0,0.3)`,
          }}
        >
          <span
            style={{
              fontFamily,
              fontSize: 40,
              fontWeight: 700,
              color: "white",
              letterSpacing: "0.02em",
            }}
          >
            Link en bio!
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
