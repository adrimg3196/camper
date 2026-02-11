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

export const PriceDisplay: React.FC<{
  price: number;
  originalPrice?: number | null;
  discount?: number | null;
}> = ({ price, originalPrice, discount }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Price slide up with bounce
  const priceProgress = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 120, mass: 0.8 },
  });

  // Discount badge bounce (delayed) - more dramatic
  const badgeProgress = spring({
    frame: Math.max(0, frame - 15),
    fps,
    config: { damping: 6, stiffness: 200, mass: 0.5 },
  });

  // Pulsing glow on price
  const pricePulse = interpolate(
    Math.sin(frame * 0.1),
    [-1, 1],
    [0.8, 1.0],
  );

  const priceY = interpolate(priceProgress, [0, 1], [50, 0]);
  const priceOpacity = interpolate(priceProgress, [0, 0.3], [0, 1], {
    extrapolateRight: "clamp",
  });
  const priceScale = interpolate(priceProgress, [0, 1], [0.8, 1]);

  const badgeScale = interpolate(badgeProgress, [0, 1], [0, 1]);
  const badgeRotate = interpolate(badgeProgress, [0, 0.5, 1], [-15, 5, 0]);
  const badgeOpacity = interpolate(badgeProgress, [0, 0.2], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Badge shake after landing
  const badgeShake = frame > 25 ? Math.sin((frame - 25) * 0.3) * 2 : 0;

  const formatPrice = (p: number) => p.toFixed(2).replace(".", ",");

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 380,
      }}
    >
      <div
        style={{
          transform: `translateY(${priceY}px) scale(${priceScale})`,
          opacity: priceOpacity,
          textAlign: "center",
        }}
      >
        {/* Original price with strikethrough */}
        {originalPrice && originalPrice > price && (
          <div
            style={{
              fontFamily,
              fontSize: 36,
              color: "rgba(255,255,255,0.5)",
              textDecoration: "line-through",
              marginBottom: 8,
            }}
          >
            {formatPrice(originalPrice)} EUR
          </div>
        )}

        {/* Current price with pulsing glow */}
        <div
          style={{
            fontFamily,
            fontSize: 72,
            fontWeight: 900,
            color: "#facc15",
            textShadow: `0 0 ${20 * pricePulse}px rgba(250,204,21,0.5), 0 4px 20px rgba(250,204,21,0.3), 0 2px 8px rgba(0,0,0,0.5)`,
            letterSpacing: "-0.03em",
          }}
        >
          {formatPrice(price)} €
        </div>

        {/* Discount badge with bounce and shake */}
        {discount && discount > 0 && (
          <div
            style={{
              display: "inline-flex",
              marginTop: 16,
              transform: `scale(${badgeScale}) rotate(${badgeRotate + badgeShake}deg)`,
              opacity: badgeOpacity,
            }}
          >
            <div
              style={{
                background: "linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)",
                color: "white",
                fontFamily,
                fontSize: 34,
                fontWeight: 800,
                padding: "12px 32px",
                borderRadius: 50,
                boxShadow: "0 6px 20px rgba(239,68,68,0.5), inset 0 1px 0 rgba(255,255,255,0.2)",
                border: "2px solid rgba(255,255,255,0.15)",
              }}
            >
              -{discount}% OFF
            </div>
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
