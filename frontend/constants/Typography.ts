/**
 * Typography system for Lottery Adviser
 */

export const Typography = {
  // Font families
  fonts: {
    regular: "System",
    medium: "System",
    bold: "System",
    // TODO: Add custom fonts (Inter, Roboto, etc.) via expo-font
  },

  // Font sizes
  sizes: {
    xs: 12,
    sm: 14,
    base: 16,
    lg: 18,
    xl: 20,
    "2xl": 24,
    "3xl": 30,
    "4xl": 36,
    "5xl": 48,
  },

  // Line heights
  lineHeights: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75,
  },

  // Font weights
  weights: {
    normal: "400" as const,
    medium: "500" as const,
    semibold: "600" as const,
    bold: "700" as const,
  },
} as const;

// Predefined text styles
export const TextStyles = {
  h1: {
    fontSize: Typography.sizes["4xl"],
    fontWeight: Typography.weights.bold,
    lineHeight: Typography.sizes["4xl"] * Typography.lineHeights.tight, // 36 * 1.2 = 43.2
  },
  h2: {
    fontSize: Typography.sizes["3xl"],
    fontWeight: Typography.weights.bold,
    lineHeight: Typography.sizes["3xl"] * Typography.lineHeights.tight, // 30 * 1.2 = 36
  },
  h3: {
    fontSize: Typography.sizes["2xl"],
    fontWeight: Typography.weights.semibold,
    lineHeight: Typography.sizes["2xl"] * Typography.lineHeights.normal, // 24 * 1.5 = 36
  },
  h4: {
    fontSize: Typography.sizes.xl,
    fontWeight: Typography.weights.semibold,
    lineHeight: Typography.sizes.xl * Typography.lineHeights.normal, // 20 * 1.5 = 30
  },
  body: {
    fontSize: Typography.sizes.base,
    fontWeight: Typography.weights.normal,
    lineHeight: Typography.sizes.base * Typography.lineHeights.normal, // 16 * 1.5 = 24
  },
  bodyLarge: {
    fontSize: Typography.sizes.lg,
    fontWeight: Typography.weights.normal,
    lineHeight: Typography.sizes.lg * Typography.lineHeights.normal, // 18 * 1.5 = 27
  },
  bodySmall: {
    fontSize: Typography.sizes.sm,
    fontWeight: Typography.weights.normal,
    lineHeight: Typography.sizes.sm * Typography.lineHeights.normal, // 14 * 1.5 = 21
  },
  caption: {
    fontSize: Typography.sizes.xs,
    fontWeight: Typography.weights.normal,
    lineHeight: Typography.sizes.xs * Typography.lineHeights.normal, // 12 * 1.5 = 18
  },
  button: {
    fontSize: Typography.sizes.base,
    fontWeight: Typography.weights.semibold,
    lineHeight: Typography.sizes.base * Typography.lineHeights.tight, // 16 * 1.2 = 19.2
  },
} as const;
