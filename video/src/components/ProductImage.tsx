import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/**
 * Product image component.
 * imageUrl can be:
 *   - A filename like "product.jpg" → resolved via staticFile() from public/
 *   - A full URL like "https://..."  → loaded directly (may fail in headless)
 */
export const ProductImage: React.FC<{ imageUrl: string }> = ({ imageUrl }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Resolve source: local file or remote URL
  const src = imageUrl.startsWith("http") ? imageUrl : staticFile(imageUrl);

  // Spring entrance
  const entrance = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 80 },
  });

  // Slow continuous zoom
  const zoom = interpolate(frame, [0, durationInFrames], [1.0, 1.06], {
    extrapolateRight: "clamp",
  });

  const scale = interpolate(entrance, [0, 1], [0.7, 1]) * zoom;
  const opacity = interpolate(entrance, [0, 0.4], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        paddingTop: 200,
        paddingBottom: 500,
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
          borderRadius: 24,
          overflow: "hidden",
          boxShadow: "0 25px 60px rgba(0,0,0,0.5), 0 10px 20px rgba(0,0,0,0.3)",
          border: "3px solid rgba(255,255,255,0.1)",
        }}
      >
        <Img
          src={src}
          style={{
            width: 700,
            height: 700,
            objectFit: "cover",
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
