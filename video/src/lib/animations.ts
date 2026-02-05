import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

/** Slide up + fade in animation */
export const useSlideUp = (delay = 0, distance = 60) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({
    frame: Math.max(0, frame - delay),
    fps,
    config: { damping: 14, stiffness: 120 },
  });
  return {
    opacity: progress,
    transform: `translateY(${interpolate(progress, [0, 1], [distance, 0])}px)`,
  };
};

/** Scale in with bounce */
export const useScaleIn = (delay = 0) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({
    frame: Math.max(0, frame - delay),
    fps,
    config: { damping: 8, stiffness: 150 },
  });
  return {
    opacity: interpolate(progress, [0, 0.3], [0, 1], { extrapolateRight: "clamp" }),
    transform: `scale(${interpolate(progress, [0, 1], [0.3, 1])})`,
  };
};

/** Slow continuous zoom */
export const useSlowZoom = (from = 1.0, to = 1.08) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const scale = interpolate(frame, [0, durationInFrames], [from, to], {
    extrapolateRight: "clamp",
  });
  return { transform: `scale(${scale})` };
};

/** Pulsing glow effect */
export const usePulse = (speed = 0.08, min = 0.7, max = 1.0) => {
  const frame = useCurrentFrame();
  const pulse = interpolate(
    Math.sin(frame * speed),
    [-1, 1],
    [min, max],
  );
  return { opacity: pulse };
};

/** Slide in from left */
export const useSlideInLeft = (delay = 0) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({
    frame: Math.max(0, frame - delay),
    fps,
    config: { damping: 14, stiffness: 100 },
  });
  return {
    opacity: progress,
    transform: `translateX(${interpolate(progress, [0, 1], [-200, 0])}px)`,
  };
};
