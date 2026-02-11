import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont();

interface DialogueSegment {
  start: number;
  end: number;
  text: string;
}

export const DialogueSubtitles: React.FC<{
  segments: DialogueSegment[];
}> = ({ segments }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Encontrar el segmento activo basado en el frame actual
  const currentTime = frame / fps;
  const activeSegment = segments.find(
    (seg) => currentTime >= seg.start && currentTime < seg.end
  );

  if (!activeSegment) {
    return null;
  }

  // Calcular progreso dentro del segmento
  const segmentDuration = activeSegment.end - activeSegment.start;
  const segmentProgress = (currentTime - activeSegment.start) / segmentDuration;

  // Animaciones de entrada y salida
  const entryProgress = spring({
    frame: Math.max(0, frame - activeSegment.start * fps),
    fps,
    config: { damping: 12, stiffness: 200, mass: 0.5 },
  });

  // Fade out en el último 20% del segmento
  const fadeOutProgress = segmentProgress > 0.8
    ? interpolate(segmentProgress, [0.8, 1], [1, 0])
    : 1;

  const scale = interpolate(entryProgress, [0, 1], [0.8, 1]);
  const translateY = interpolate(entryProgress, [0, 1], [30, 0]);
  const opacity = entryProgress * fadeOutProgress;

  // Palabras animadas individualmente
  const words = activeSegment.text.split(" ");
  const wordsPerSecond = words.length / segmentDuration;
  const currentWordIndex = Math.min(
    Math.floor(segmentProgress * words.length * 1.2), // 1.2x para que termine antes
    words.length
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        paddingBottom: 200, // Posición en la parte inferior-centro
      }}
    >
      <div
        style={{
          transform: `translateY(${translateY}px) scale(${scale})`,
          opacity,
          textAlign: "center",
          maxWidth: "90%",
          padding: "16px 32px",
          background: "rgba(0,0,0,0.7)",
          borderRadius: 16,
          backdropFilter: "blur(10px)",
          boxShadow: "0 8px 32px rgba(0,0,0,0.3)",
        }}
      >
        <div
          style={{
            fontFamily,
            fontSize: 42,
            fontWeight: 700,
            lineHeight: 1.3,
            letterSpacing: "-0.02em",
          }}
        >
          {words.map((word, index) => {
            const isVisible = index < currentWordIndex;
            const isCurrentWord = index === currentWordIndex - 1;

            return (
              <span
                key={index}
                style={{
                  color: isVisible ? "#ffffff" : "rgba(255,255,255,0.3)",
                  textShadow: isCurrentWord
                    ? "0 0 20px rgba(250,204,21,0.8)"
                    : "0 2px 4px rgba(0,0,0,0.5)",
                  transition: "color 0.1s ease",
                  marginRight: 10,
                }}
              >
                {word}
              </span>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
