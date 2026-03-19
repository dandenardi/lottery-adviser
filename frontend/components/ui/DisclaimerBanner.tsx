import React from "react";
import { View, Text, Pressable, StyleSheet } from "react-native";
import { router } from "expo-router";
import { Colors } from "@/constants/Colors";
import { Spacing } from "@/constants/Layout";
import { TextStyles } from "@/constants/Typography";

/**
 * Persistent disclaimer banner shown at the top of every screen.
 * Required for Google Play gambling/lottery content policy compliance.
 */
export function DisclaimerBanner() {
  return (
    <View style={styles.container}>
      <Text style={styles.icon}>⚠️</Text>
      <Text style={styles.text} numberOfLines={2}>
        Apenas para fins informativos. Não garantimos nenhum prêmio.{" "}
      </Text>
      <Pressable
        onPress={() => router.push("/disclaimer" as any)}
        accessibilityRole="link"
        accessibilityLabel="Ver aviso completo"
      >
        <Text style={styles.link}>Saiba mais</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#FFFBEB", // amber-50
    borderBottomWidth: 1,
    borderBottomColor: "#FDE68A", // amber-200
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    gap: Spacing.xs,
  },
  icon: {
    fontSize: 14,
  },
  text: {
    ...TextStyles.bodySmall,
    color: "#92400E", // amber-800
    flex: 1,
    flexWrap: "wrap",
  },
  link: {
    ...TextStyles.bodySmall,
    color: Colors.light.primary,
    fontWeight: "700",
    textDecorationLine: "underline",
  },
});
