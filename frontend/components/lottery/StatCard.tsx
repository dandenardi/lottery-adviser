/**
 * StatCard Component
 * Displays a statistic with icon, title, value, and description
 */

import React from "react";
import { View, Text, StyleSheet, ViewStyle } from "react-native";
import { Card } from "@/components/ui/Card";
import { Colors } from "@/constants/Colors";
import { Spacing } from "@/constants/Layout";
import { TextStyles, Typography } from "@/constants/Typography";

interface StatCardProps {
  icon: string; // Emoji or icon
  title: string;
  value: string | number;
  description?: string;
  variant?: "default" | "primary" | "secondary";
  style?: ViewStyle;
}

export function StatCard({
  icon,
  title,
  value,
  description,
  variant = "default",
  style,
}: StatCardProps) {
  const valueColor =
    variant === "primary"
      ? Colors.light.primary
      : variant === "secondary"
        ? Colors.light.secondary
        : Colors.light.text;

  return (
    <Card elevated style={style}>
      <View style={styles.container}>
        <Text style={styles.icon}>{icon}</Text>

        <View style={styles.content}>
          <Text style={styles.title}>{title}</Text>
          <Text style={[styles.value, { color: valueColor }]}>{value}</Text>
          {description && <Text style={styles.description}>{description}</Text>}
        </View>
      </View>
    </Card>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
  },
  icon: {
    fontSize: 32,
    marginRight: Spacing.md,
  },
  content: {
    flex: 1,
  },
  title: {
    ...TextStyles.bodySmall,
    color: Colors.light.textSecondary,
    marginBottom: 4,
  },
  value: {
    ...TextStyles.h3,
    fontWeight: Typography.weights.bold,
  },
  description: {
    ...TextStyles.caption,
    color: Colors.light.textTertiary,
    marginTop: 4,
  },
});
