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
    lineHeight: Typography.lineHeights.tight,
  },
  h2: {
    fontSize: Typography.sizes["3xl"],
    fontWeight: Typography.weights.bold,
    lineHeight: Typography.lineHeights.tight,
  },
  h3: {
    fontSize: Typography.sizes["2xl"],
    fontWeight: Typography.weights.semibold,
    lineHeight: Typography.lineHeights.normal,
  },
  h4: {
    fontSize: Typography.sizes.xl,
    fontWeight: Typography.weights.semibold,
    lineHeight: Typography.lineHeights.normal,
  },
  body: {
    fontSize: Typography.sizes.base,
    fontWeight: Typography.weights.normal,
    lineHeight: Typography.lineHeights.normal,
  },
  bodyLarge: {
    fontSize: Typography.sizes.lg,
    fontWeight: Typography.weights.normal,
    lineHeight: Typography.lineHeights.normal,
  },
  bodySmall: {
    fontSize: Typography.sizes.sm,
    fontWeight: Typography.weights.normal,
    lineHeight: Typography.lineHeights.normal,
  },
  caption: {
    fontSize: Typography.sizes.xs,
    fontWeight: Typography.weights.normal,
    lineHeight: Typography.lineHeights.normal,
  },
  button: {
    fontSize: Typography.sizes.base,
    fontWeight: Typography.weights.semibold,
    lineHeight: Typography.lineHeights.tight,
  },
} as const;
