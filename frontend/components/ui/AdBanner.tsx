import React from "react";
import { StyleSheet, View, Text, Platform } from "react-native";
import { Colors } from "@/constants/Colors";
import { Spacing } from "@/constants/Layout";
import { TextStyles } from "@/constants/Typography";
import { useIsPremium } from "@/hooks/usePremiumStatus";

/**
 * AdBanner Component
 * 
 * Displays a placeholder banner ad for free users.
 * In a real production app, this would use react-native-google-mobile-ads.
 */
export function AdBanner() {
  const isPremium = useIsPremium();

  // Don't show ads for premium users
  if (isPremium) {
    return null;
  }

  return (
    <View style={styles.container}>
      <View style={styles.adBox}>
        <Text style={styles.adLabel}>ANÚNCIO</Text>
        <Text style={styles.adPlaceholderText}>
          {Platform.OS === "web" 
            ? "Espaço para publicidade (Google AdSense)" 
            : "Espaço para AdMob (Banner)"}
        </Text>
      </View>
      <Text style={styles.removeAdsText}>
        Remova anúncios com o Plano Premium ⭐
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: Spacing.md,
    alignItems: "center",
  },
  adBox: {
    width: "100%",
    height: 60,
    backgroundColor: "#F3F4F6",
    borderWidth: 1,
    borderColor: "#D1D5DB",
    borderRadius: 4,
    justifyContent: "center",
    alignItems: "center",
  },
  adLabel: {
    position: "absolute",
    top: 2,
    left: 4,
    fontSize: 10,
    color: "#9CA3AF",
    fontWeight: "700",
  },
  adPlaceholderText: {
    ...TextStyles.bodySmall,
    color: "#6B7280",
  },
  removeAdsText: {
    ...TextStyles.bodySmall,
    fontSize: 10,
    color: Colors.light.textSecondary,
    marginTop: 4,
    fontStyle: "italic",
  },
});
