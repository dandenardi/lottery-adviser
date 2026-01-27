/**
 * Card Component
 * Container component for content with optional shadow
 */

import React from "react";
import { View, StyleSheet, ViewStyle } from "react-native";
import { Colors } from "@/constants/Colors";
import { BorderRadius, Spacing, Shadows } from "@/constants/Layout";

interface CardProps {
  children: React.ReactNode;
  elevated?: boolean;
  padding?: keyof typeof Spacing;
  style?: ViewStyle;
}

export function Card({
  children,
  elevated = false,
  padding = "md",
  style,
}: CardProps) {
  return (
    <View
      style={[
        styles.card,
        elevated && Shadows.md,
        { padding: Spacing[padding] },
        style,
      ]}
    >
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.light.card,
    borderRadius: BorderRadius.lg,
  },
});
