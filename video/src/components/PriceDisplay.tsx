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

  // Price slide up
  const priceProgress = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  // Discount badge bounce (delayed)
  const badgeProgress = spring({
    frame: Math.max(0, frame - 20),
    fps,
    config: { damping: 8, stiffness: 150 },
  });

  const priceY = interpolate(priceProgress, [0, 1], [40, 0]);
  const priceOpacity = interpolate(priceProgress, [0, 0.4], [0, 1], {
    extrapolateRight: "clamp",
  });

  const badgeScale = interpolate(badgeProgress, [0, 1], [0.2, 1]);
  const badgeOpacity = interpolate(badgeProgress, [0, 0.3], [0, 1], {
    extrapolateRight: "clamp",
  });

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
          transform: `translateY(${priceY}px)`,
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

        {/* Current price */}
        <div
          style={{
            fontFamily,
            fontSize: 72,
            fontWeight: 900,
            color: "#facc15",
            textShadow: "0 4px 20px rgba(250,204,21,0.3), 0 2px 8px rgba(0,0,0,0.5)",
            letterSpacing: "-0.03em",
          }}
        >
          {formatPrice(price)} EUR
        </div>

        {/* Discount badge */}
        {discount && discount > 0 && (
          <div
            style={{
              display: "inline-flex",
              marginTop: 16,
              transform: `scale(${badgeScale})`,
              opacity: badgeOpacity,
            }}
          >
            <div
              style={{
                background: "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                color: "white",
                fontFamily,
                fontSize: 32,
                fontWeight: 800,
                padding: "10px 28px",
                borderRadius: 50,
                boxShadow: "0 4px 15px rgba(239,68,68,0.4)",
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
