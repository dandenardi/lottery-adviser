/**
 * PremiumBadge Component
 * Animated badge showing premium status
 */

import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { Colors } from "@/constants/Colors";
import { BorderRadius, Spacing } from "@/constants/Layout";
import { Typography } from "@/constants/Typography";

interface PremiumBadgeProps {
  size?: "small" | "medium" | "large";
}

const SIZES = {
  small: {
    paddingHorizontal: Spacing.sm,
    paddingVertical: 4,
    fontSize: Typography.sizes.xs,
  },
  medium: {
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    fontSize: Typography.sizes.sm,
  },
  large: {
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.md,
    fontSize: Typography.sizes.base,
  },
};

export function PremiumBadge({ size = "medium" }: PremiumBadgeProps) {
  const sizeStyle = SIZES[size];

  return (
    <LinearGradient
      colors={[
        Colors.light.premiumGradientStart,
        Colors.light.premiumGradientEnd,
      ]}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 0 }}
      style={[
        styles.badge,
        {
          paddingHorizontal: sizeStyle.paddingHorizontal,
          paddingVertical: sizeStyle.paddingVertical,
        },
      ]}
    >
      <Text style={[styles.text, { fontSize: sizeStyle.fontSize }]}>
        ⭐ PREMIUM
      </Text>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  badge: {
    borderRadius: BorderRadius.full,
    alignSelf: "flex-start",
  },
  text: {
    color: "#FFFFFF",
    fontWeight: Typography.weights.bold,
    letterSpacing: 0.5,
  },
});
