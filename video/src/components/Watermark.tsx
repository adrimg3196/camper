import React from "react";
import { AbsoluteFill } from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont();

export const Watermark: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 80,
      }}
    >
      <span
        style={{
          fontFamily,
          fontSize: 24,
          fontWeight: 600,
          color: "rgba(255,255,255,0.35)",
          letterSpacing: "0.05em",
        }}
      >
        @camperoutlet
      </span>
    </AbsoluteFill>
  );
};
