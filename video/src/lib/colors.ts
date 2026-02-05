/** Category-based color schemes for video backgrounds */
export const categoryColors: Record<string, { from: string; via: string; to: string }> = {
  "camping": { from: "#052e16", via: "#14532d", to: "#166534" },
  "tiendas-camping": { from: "#052e16", via: "#15803d", to: "#14532d" },
  "sacos-dormir": { from: "#1e1b4b", via: "#312e81", to: "#14532d" },
  "cocina-camping": { from: "#431407", via: "#9a3412", to: "#7c2d12" },
  "iluminacion": { from: "#1c1917", via: "#44403c", to: "#292524" },
  "mochilas": { from: "#172554", via: "#1e3a5f", to: "#14532d" },
  "herramientas": { from: "#1c1917", via: "#292524", to: "#431407" },
  default: { from: "#052e16", via: "#14532d", to: "#0f172a" },
};

export const getColorsForCategory = (category: string) => {
  return categoryColors[category] || categoryColors.default;
};

/** Brand colors */
export const brand = {
  green: "#22c55e",
  orange: "#f97316",
  yellow: "#facc15",
  white: "#ffffff",
  dark: "#0a0a0a",
};
