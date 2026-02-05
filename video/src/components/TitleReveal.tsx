import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Outfit";

const { fontFamily } = loadFont();

export const TitleReveal: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  const translateY = interpolate(progress, [0, 1], [50, 0]);
  const opacity = interpolate(progress, [0, 0.5], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Truncate if too long
  const displayText = text.length > 60 ? text.substring(0, 57) + "..." : text;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-start",
        alignItems: "center",
        paddingTop: 80,
        paddingLeft: 60,
        paddingRight: 60,
      }}
    >
      <div
        style={{
          transform: `translateY(${translateY}px)`,
          opacity,
          textAlign: "center",
        }}
      >
        <h1
          style={{
            fontFamily,
            fontSize: 56,
            fontWeight: 800,
            color: "white",
            lineHeight: 1.2,
            textShadow: "0 4px 20px rgba(0,0,0,0.7), 0 2px 4px rgba(0,0,0,0.5)",
            margin: 0,
            letterSpacing: "-0.02em",
          }}
        >
          {displayText}
        </h1>
      </div>
    </AbsoluteFill>
  );
};
