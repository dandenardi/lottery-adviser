/**
 * Badge Component
 * Small label for displaying numbers or short text
 */

import React from "react";
import { View, Text, StyleSheet, ViewStyle } from "react-native";
import { Colors } from "@/constants/Colors";
import { BorderRadius, Spacing } from "@/constants/Layout";
import { Typography } from "@/constants/Typography";

type BadgeVariant = "primary" | "secondary" | "success" | "error" | "neutral";

interface BadgeProps {
  label: string | number;
  variant?: BadgeVariant;
  style?: ViewStyle;
}

export function Badge({ label, variant = "neutral", style }: BadgeProps) {
  return (
    <View style={[styles.badge, styles[variant], style]}>
      <Text style={[styles.text, styles[`${variant}Text`]]}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: {
    paddingHorizontal: Spacing.sm,
    paddingVertical: 4,
    borderRadius: BorderRadius.sm,
    alignSelf: "flex-start",
  },
  text: {
    fontSize: Typography.sizes.xs,
    fontWeight: Typography.weights.semibold,
  },

  // Variants
  primary: {
    backgroundColor: Colors.light.primary,
  },
  primaryText: {
    color: "#FFFFFF",
  },

  secondary: {
    backgroundColor: Colors.light.secondary,
  },
  secondaryText: {
    color: "#FFFFFF",
  },

  success: {
    backgroundColor: Colors.light.success,
  },
  successText: {
    color: "#FFFFFF",
  },

  error: {
    backgroundColor: Colors.light.error,
  },
  errorText: {
    color: "#FFFFFF",
  },

  neutral: {
    backgroundColor: Colors.light.card,
    borderWidth: 1,
    borderColor: Colors.light.border,
  },
  neutralText: {
    color: Colors.light.text,
  },
});
