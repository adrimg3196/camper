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
  const segmentStartFrame = activeSegment.start * fps;
  const segmentDuration = activeSegment.end - activeSegment.start;
  const segmentProgress = (currentTime - activeSegment.start) / segmentDuration;

  // Animación de entrada con spring más agresivo
  const entryProgress = spring({
    frame: frame - segmentStartFrame,
    fps,
    config: { damping: 10, stiffness: 300, mass: 0.4 },
  });

  // Fade out suave en el último 15%
  const fadeOutProgress = segmentProgress > 0.85
    ? interpolate(segmentProgress, [0.85, 1], [1, 0])
    : 1;

  // Efectos de entrada
  const scale = interpolate(entryProgress, [0, 1], [0.7, 1]);
  const translateY = interpolate(entryProgress, [0, 1], [40, 0]);
  const opacity = entryProgress * fadeOutProgress;

  // Palabras con animación karaoke
  const words = activeSegment.text.split(" ");
  const currentWordIndex = Math.min(
    Math.floor(segmentProgress * words.length * 1.3),
    words.length
  );

  // Efecto de "glow" pulsante
  const glowPulse = Math.sin(frame * 0.15) * 0.3 + 0.7;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 280,
      }}
    >
      <div
        style={{
          transform: `translateY(${translateY}px) scale(${scale})`,
          opacity,
          textAlign: "center",
          maxWidth: "95%",
          padding: "20px 36px",
          background: "linear-gradient(135deg, rgba(0,0,0,0.85) 0%, rgba(20,20,30,0.9) 100%)",
          borderRadius: 20,
          border: "2px solid rgba(250,204,21,0.4)",
          boxShadow: `
            0 8px 32px rgba(0,0,0,0.5),
            0 0 ${20 * glowPulse}px rgba(250,204,21,0.2),
            inset 0 1px 0 rgba(255,255,255,0.1)
          `,
        }}
      >
        <div
          style={{
            fontFamily,
            fontSize: 48,
            fontWeight: 800,
            lineHeight: 1.25,
            letterSpacing: "-0.03em",
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: "12px",
          }}
        >
          {words.map((word, index) => {
            const isVisible = index < currentWordIndex;
            const isCurrentWord = index === currentWordIndex - 1;
            const isPastWord = index < currentWordIndex - 1;

            // Escala para palabra actual
            const wordScale = isCurrentWord
              ? spring({
                  frame: frame - (segmentStartFrame + (index / words.length) * segmentDuration * fps),
                  fps,
                  config: { damping: 8, stiffness: 400 },
                })
              : 1;

            return (
              <span
                key={index}
                style={{
                  display: "inline-block",
                  color: isVisible ? "#ffffff" : "rgba(255,255,255,0.25)",
                  transform: `scale(${isCurrentWord ? 1 + wordScale * 0.1 : 1})`,
                  textShadow: isCurrentWord
                    ? `
                      0 0 30px rgba(250,204,21,1),
                      0 0 60px rgba(250,204,21,0.6),
                      0 2px 4px rgba(0,0,0,0.8)
                    `
                    : isPastWord
                    ? "0 2px 4px rgba(0,0,0,0.5)"
                    : "none",
                  transition: "color 0.1s ease, transform 0.15s ease",
                }}
              >
                {word}
              </span>
            );
          })}
        </div>
      </div>

      {/* Indicador de progreso del segmento */}
      <div
        style={{
          position: "absolute",
          bottom: 240,
          width: "80%",
          height: 4,
          background: "rgba(255,255,255,0.15)",
          borderRadius: 2,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${segmentProgress * 100}%`,
            height: "100%",
            background: "linear-gradient(90deg, #facc15, #fbbf24)",
            borderRadius: 2,
            boxShadow: "0 0 10px rgba(250,204,21,0.5)",
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
