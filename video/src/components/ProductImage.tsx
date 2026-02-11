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

interface ProductImageProps {
  imageUrl: string;
  isAnimated?: boolean; // Activar animaciones de "producto que habla"
}

/**
 * Product image component with optional "talking product" animations.
 * When isAnimated=true, the product bounces, rotates and pulses
 * as if it were alive and speaking to the viewer.
 */
export const ProductImage: React.FC<ProductImageProps> = ({
  imageUrl,
  isAnimated = true,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Resolve source: local file or remote URL
  const src = imageUrl.startsWith("http") ? imageUrl : staticFile(imageUrl);

  // Spring entrance (más dramático)
  const entrance = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 100, mass: 0.8 },
  });

  // Slow continuous zoom
  const baseZoom = interpolate(frame, [0, durationInFrames], [1.0, 1.08], {
    extrapolateRight: "clamp",
  });

  // === ANIMACIONES DE "PRODUCTO QUE HABLA" ===

  // 1. Bounce vertical (como si saltara de emoción)
  const bounceSpeed = 0.12;
  const bounceAmount = isAnimated ? Math.sin(frame * bounceSpeed) * 8 : 0;

  // 2. Rotación suave (como si se moviera al hablar)
  const rotationSpeed = 0.08;
  const rotationAmount = isAnimated ? Math.sin(frame * rotationSpeed) * 2.5 : 0;

  // 3. Escala pulsante (respira mientras habla)
  const pulseSpeed = 0.1;
  const pulseAmount = isAnimated ? 1 + Math.sin(frame * pulseSpeed) * 0.03 : 1;

  // 4. Inclinación lateral (como asintiendo)
  const tiltSpeed = 0.06;
  const tiltAmount = isAnimated ? Math.sin(frame * tiltSpeed * 2) * 1.5 : 0;

  // 5. Efecto de "salto" en momentos clave (cada ~2 segundos)
  const jumpInterval = fps * 2;
  const jumpProgress = (frame % jumpInterval) / jumpInterval;
  const isJumping = jumpProgress < 0.15 && isAnimated;
  const jumpBounce = isJumping
    ? spring({
        frame: frame % jumpInterval,
        fps,
        config: { damping: 8, stiffness: 300 },
      }) * 15
    : 0;

  // Combinar transformaciones
  const scale = interpolate(entrance, [0, 1], [0.5, 1]) * baseZoom * pulseAmount;
  const translateY = bounceAmount - jumpBounce;
  const rotation = rotationAmount + tiltAmount;

  const opacity = interpolate(entrance, [0, 0.3], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Glow dinámico (más intenso cuando "salta")
  const glowIntensity = isAnimated
    ? 0.4 + Math.sin(frame * 0.1) * 0.2 + (isJumping ? 0.3 : 0)
    : 0.3;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        paddingTop: 180,
        paddingBottom: 480,
      }}
    >
      {/* Sombra animada debajo del producto */}
      {isAnimated && (
        <div
          style={{
            position: "absolute",
            width: 500,
            height: 40,
            background: "radial-gradient(ellipse, rgba(0,0,0,0.4) 0%, transparent 70%)",
            borderRadius: "50%",
            transform: `translateY(${380 + bounceAmount * 0.5}px) scaleX(${0.9 + Math.sin(frame * 0.1) * 0.1})`,
            opacity: 0.6 - (jumpBounce / 30),
          }}
        />
      )}

      <div
        style={{
          transform: `
            translateY(${translateY}px)
            rotate(${rotation}deg)
            scale(${scale})
          `,
          opacity,
          borderRadius: 28,
          overflow: "hidden",
          boxShadow: `
            0 ${25 + jumpBounce}px ${60 + jumpBounce * 2}px rgba(0,0,0,0.5),
            0 10px 20px rgba(0,0,0,0.3),
            0 0 ${40 * glowIntensity}px rgba(250,204,21,${glowIntensity * 0.5}),
            inset 0 0 0 3px rgba(255,255,255,0.1)
          `,
          transition: "box-shadow 0.1s ease",
        }}
      >
        <Img
          src={src}
          style={{
            width: 650,
            height: 650,
            objectFit: "cover",
          }}
        />

        {/* Overlay de brillo animado */}
        {isAnimated && (
          <div
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: `linear-gradient(
                ${135 + Math.sin(frame * 0.05) * 20}deg,
                rgba(255,255,255,${0.1 + Math.sin(frame * 0.08) * 0.05}) 0%,
                transparent 50%,
                rgba(250,204,21,${0.05 + Math.sin(frame * 0.1) * 0.03}) 100%
              )`,
              pointerEvents: "none",
            }}
          />
        )}
      </div>

      {/* Partículas de energía alrededor del producto */}
      {isAnimated && (
        <EnergyParticles frame={frame} />
      )}
    </AbsoluteFill>
  );
};

// Componente de partículas de energía
const EnergyParticles: React.FC<{ frame: number }> = ({ frame }) => {
  const particles = Array.from({ length: 6 }, (_, i) => {
    const angle = (i / 6) * Math.PI * 2 + frame * 0.02;
    const radius = 380 + Math.sin(frame * 0.1 + i) * 20;
    const x = Math.cos(angle) * radius;
    const y = Math.sin(angle) * radius * 0.3; // Elipse
    const size = 4 + Math.sin(frame * 0.15 + i * 2) * 2;
    const opacity = 0.4 + Math.sin(frame * 0.12 + i) * 0.3;

    return (
      <div
        key={i}
        style={{
          position: "absolute",
          width: size,
          height: size,
          borderRadius: "50%",
          background: `radial-gradient(circle, rgba(250,204,21,${opacity}) 0%, transparent 70%)`,
          transform: `translate(${x}px, ${y}px)`,
          boxShadow: `0 0 ${size * 3}px rgba(250,204,21,${opacity * 0.5})`,
        }}
      />
    );
  });

  return <>{particles}</>;
};
