/**
 * LoadingSpinner Component
 * Centered loading indicator with optional text
 */

import React from "react";
import { View, ActivityIndicator, Text, StyleSheet } from "react-native";
import { Colors } from "@/constants/Colors";
import { Spacing } from "@/constants/Layout";
import { TextStyles } from "@/constants/Typography";

interface LoadingSpinnerProps {
  text?: string;
  size?: "small" | "large";
  color?: string;
}

export function LoadingSpinner({
  text,
  size = "large",
  color = Colors.light.primary,
}: LoadingSpinnerProps) {
  return (
    <View style={styles.container}>
      <ActivityIndicator size={size} color={color} />
      {text && <Text style={styles.text}>{text}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: Spacing.xl,
  },
  text: {
    ...TextStyles.body,
    color: Colors.light.textSecondary,
    marginTop: Spacing.md,
    textAlign: "center",
  },
});
