/**
 * ErrorMessage Component
 * Display error messages with retry option
 */

import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { Colors } from "@/constants/Colors";
import { Spacing, BorderRadius } from "@/constants/Layout";
import { TextStyles } from "@/constants/Typography";
import { Button } from "./Button";

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  return (
    <View style={styles.container}>
      <View style={styles.errorBox}>
        <Text style={styles.emoji}>⚠️</Text>
        <Text style={styles.message}>{message}</Text>
        {onRetry && (
          <Button
            title="Tentar Novamente"
            onPress={onRetry}
            variant="outline"
            size="small"
            style={styles.button}
          />
        )}
      </View>
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
  errorBox: {
    backgroundColor: Colors.light.card,
    borderRadius: BorderRadius.lg,
    padding: Spacing.lg,
    alignItems: "center",
    maxWidth: 300,
  },
  emoji: {
    fontSize: 48,
    marginBottom: Spacing.md,
  },
  message: {
    ...TextStyles.body,
    color: Colors.light.text,
    textAlign: "center",
    marginBottom: Spacing.md,
  },
  button: {
    marginTop: Spacing.sm,
  },
});
