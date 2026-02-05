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

/**
 * Shortens an Amazon affiliate URL to a readable form.
 * e.g. "https://www.amazon.es/dp/B072K5C973?tag=camperdeals-21"
 *   -> "amazon.es/dp/B072K5C973"
 */
function shortenUrl(url: string): string {
  try {
    const u = new URL(url);
    // Show domain + path (no query params) - cleaner for video
    const short = u.hostname.replace("www.", "") + u.pathname;
    return short.length > 35 ? short.slice(0, 35) + "..." : short;
  } catch {
    return url.slice(0, 35);
  }
}

export const CallToAction: React.FC<{ affiliateUrl?: string }> = ({
  affiliateUrl,
}) => {
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

  // URL entrance (delayed after button)
  const urlEntrance = spring({
    frame: Math.max(0, frame - 15),
    fps,
    config: { damping: 14, stiffness: 80 },
  });
  const urlOpacity = interpolate(urlEntrance, [0, 0.5], [0, 1], {
    extrapolateRight: "clamp",
  });
  const urlTranslateY = interpolate(urlEntrance, [0, 1], [15, 0]);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: affiliateUrl ? 160 : 220,
      }}
    >
      <div
        style={{
          transform: `translateY(${translateY}px) scale(${pulse})`,
          opacity,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 16,
        }}
      >
        {/* Main CTA button */}
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
            {affiliateUrl ? "Busca en Amazon" : "Link en bio!"}
          </span>
        </div>

        {/* Affiliate URL shown below the button */}
        {affiliateUrl && (
          <div
            style={{
              opacity: urlOpacity,
              transform: `translateY(${urlTranslateY}px)`,
            }}
          >
            <div
              style={{
                background: "rgba(0,0,0,0.6)",
                backdropFilter: "blur(8px)",
                padding: "10px 24px",
                borderRadius: 12,
                border: "1px solid rgba(255,255,255,0.15)",
              }}
            >
              <span
                style={{
                  fontFamily,
                  fontSize: 24,
                  fontWeight: 500,
                  color: "#facc15",
                  letterSpacing: "0.01em",
                }}
              >
                {shortenUrl(affiliateUrl)}
              </span>
            </div>
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
