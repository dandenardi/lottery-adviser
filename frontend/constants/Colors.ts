/**
 * Color palette for Lottery Adviser
 * Green (luck) + Gold (prize) theme
 */

export const Colors = {
  light: {
    // Primary colors
    primary: "#10B981", // Green (luck)
    primaryLight: "#34D399",
    primaryDark: "#059669",

    // Secondary colors
    secondary: "#F59E0B", // Gold (prize)
    secondaryLight: "#FBBF24",
    secondaryDark: "#D97706",

    // Background
    background: "#FFFFFF",
    backgroundSecondary: "#F9FAFB",

    // Card/Surface
    card: "#F3F4F6",
    cardElevated: "#FFFFFF",

    // Text
    text: "#111827",
    textSecondary: "#6B7280",
    textTertiary: "#9CA3AF",

    // Border
    border: "#E5E7EB",
    borderLight: "#F3F4F6",

    // Status colors
    success: "#10B981",
    error: "#EF4444",
    warning: "#F59E0B",
    info: "#3B82F6",

    // Number ball colors
    numberHot: "#EF4444", // Red for hot numbers
    numberCold: "#3B82F6", // Blue for cold numbers
    numberNeutral: "#6B7280", // Gray for neutral numbers

    // Premium
    premium: "#F59E0B",
    premiumGradientStart: "#F59E0B",
    premiumGradientEnd: "#D97706",
  },

  dark: {
    // Primary colors
    primary: "#34D399", // Lighter green for dark mode
    primaryLight: "#6EE7B7",
    primaryDark: "#10B981",

    // Secondary colors
    secondary: "#FBBF24", // Lighter gold for dark mode
    secondaryLight: "#FCD34D",
    secondaryDark: "#F59E0B",

    // Background
    background: "#111827",
    backgroundSecondary: "#1F2937",

    // Card/Surface
    card: "#1F2937",
    cardElevated: "#374151",

    // Text
    text: "#F9FAFB",
    textSecondary: "#9CA3AF",
    textTertiary: "#6B7280",

    // Border
    border: "#374151",
    borderLight: "#4B5563",

    // Status colors
    success: "#34D399",
    error: "#F87171",
    warning: "#FBBF24",
    info: "#60A5FA",

    // Number ball colors
    numberHot: "#F87171", // Lighter red for dark mode
    numberCold: "#60A5FA", // Lighter blue for dark mode
    numberNeutral: "#9CA3AF", // Lighter gray for dark mode

    // Premium
    premium: "#FBBF24",
    premiumGradientStart: "#FBBF24",
    premiumGradientEnd: "#F59E0B",
  },
} as const;

export type ColorScheme = keyof typeof Colors;
export type ColorName = keyof typeof Colors.light;
