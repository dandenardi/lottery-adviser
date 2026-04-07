/**
 * Paywall Component
 * Modal displaying subscription options and benefits
 */

import React from "react";
import {
  View,
  Text,
  StyleSheet,
  Modal,
  ScrollView,
  TouchableOpacity,
  Alert,
} from "react-native";
import Purchases, { PurchasesPackage, PurchasesOffering } from "react-native-purchases";
import { Button } from "@/components/ui/Button";
import { PremiumBadge } from "./PremiumBadge";
import { Colors } from "@/constants/Colors";
import { Spacing, BorderRadius } from "@/constants/Layout";
import { TextStyles, Typography } from "@/constants/Typography";
import { useOfferings } from "@/hooks/usePremiumStatus";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";

interface PaywallProps {
  visible: boolean;
  onClose: () => void;
  onPurchase: (pkg: PurchasesPackage) => Promise<void>;
  onRestore: () => Promise<void>;
}

const BENEFITS = [
  "✨ Sugestões ilimitadas de números",
  "📊 Acesso a todas as estratégias",
  "🎯 Análises avançadas",
  "🔔 Notificações de resultados",
  "💾 Histórico de sugestões",
  "🚀 Novos recursos em primeira mão",
];

export function Paywall({
  visible,
  onClose,
  onPurchase,
  onRestore,
}: PaywallProps) {
  const [loading, setLoading] = React.useState(false);
  const { data: offerings, isLoading: isLoadingOfferings } = useOfferings();

  const handlePurchase = async (pkg: PurchasesPackage) => {
    try {
      setLoading(true);
      await onPurchase(pkg);
      onClose();
    } catch (error: any) {
      if (!error.userCancelled) {
        Alert.alert("Erro", error.message || "Falha ao processar compra");
      }
    } finally {
      setLoading(false);
    }
  };

  const currentOffering = offerings?.current;
  const packages = currentOffering?.availablePackages || [];

  const handleRestore = async () => {
    try {
      setLoading(true);
      await onRestore();
      Alert.alert("Sucesso", "Compras restauradas com sucesso!");
    } catch (error: any) {
      Alert.alert("Erro", error.message || "Nenhuma compra encontrada");
    } finally {
      setLoading(false);
    }
  };

  const getTranslatedPlanName = (pkg: PurchasesPackage) => {
    const title = pkg.product.title;
    // Common store titles that might come in English during sandbox testing
    if (title.toLowerCase().includes("monthly")) return "Mensal";
    if (title.toLowerCase().includes("annual")) return "Anual";
    if (title.toLowerCase().includes("yearly")) return "Anual";
    if (title.toLowerCase().includes("weekly")) return "Semanal";
    return title;
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
      onRequestClose={onClose}
    >
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={onClose} style={styles.closeButton}>
            <Text style={styles.closeText}>✕</Text>
          </TouchableOpacity>
        </View>

        <ScrollView
          style={styles.content}
          contentContainerStyle={styles.contentContainer}
        >
          {/* Title */}
          <View style={styles.titleContainer}>
            <PremiumBadge size="large" />
            <Text style={styles.title}>Desbloqueie o Poder Premium</Text>
            <Text style={styles.subtitle}>
              Maximize suas chances com recursos exclusivos
            </Text>
          </View>

          {/* Benefits */}
          <View style={styles.benefitsContainer}>
            {BENEFITS.map((benefit, index) => (
              <View key={index} style={styles.benefitItem}>
                <Text style={styles.benefitText}>{benefit}</Text>
              </View>
            ))}
          </View>

          {/* Plans */}
          <View style={styles.plansContainer}>
            {isLoadingOfferings ? (
              <LoadingSpinner text="Carregando planos..." />
            ) : packages.length > 0 ? (
              packages.map((pkg) => (
                <TouchableOpacity
                  key={pkg.identifier}
                  style={[
                    styles.planCard,
                    pkg.packageType === "ANNUAL" && styles.planCardPopular,
                  ]}
                  onPress={() => handlePurchase(pkg)}
                  disabled={loading}
                >
                  {pkg.packageType === "ANNUAL" && (
                    <View style={styles.popularBadge}>
                      <Text style={styles.popularText}>MELHOR VALOR</Text>
                    </View>
                  )}

                  <Text style={styles.planName}>{getTranslatedPlanName(pkg)}</Text>
                  <Text style={styles.planPrice}>{pkg.product.priceString}</Text>
                  <Text style={styles.planPeriod}>
                    {pkg.packageType === "MONTHLY" ? "por mês" : 
                     pkg.packageType === "ANNUAL" ? "por ano" : 
                     pkg.packageType === "WEEKLY" ? "por semana" : ""}
                  </Text>
                </TouchableOpacity>
              ))
            ) : (
              <Text style={styles.noPlansText}>
                Nenhum plano disponível no momento.
              </Text>
            )}
          </View>

          {/* Restore Button */}
          <TouchableOpacity
            onPress={handleRestore}
            disabled={loading}
            style={styles.restoreButton}
          >
            <Text style={styles.restoreText}>Restaurar Compras</Text>
          </TouchableOpacity>

          {/* Terms */}
          <Text style={styles.terms}>
            A assinatura será renovada automaticamente. Cancele a qualquer
            momento nas configurações da sua conta.
          </Text>
        </ScrollView>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.light.background,
  },
  header: {
    flexDirection: "row",
    justifyContent: "flex-end",
    padding: Spacing.md,
  },
  closeButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: Colors.light.card,
    justifyContent: "center",
    alignItems: "center",
  },
  closeText: {
    fontSize: Typography.sizes.xl,
    color: Colors.light.textSecondary,
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: Spacing.lg,
  },
  titleContainer: {
    alignItems: "center",
    marginBottom: Spacing.xl,
  },
  title: {
    ...TextStyles.h2,
    color: Colors.light.text,
    textAlign: "center",
    marginTop: Spacing.md,
  },
  subtitle: {
    ...TextStyles.body,
    color: Colors.light.textSecondary,
    textAlign: "center",
    marginTop: Spacing.sm,
  },
  benefitsContainer: {
    marginBottom: Spacing.xl,
  },
  benefitItem: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: Spacing.sm,
  },
  benefitText: {
    ...TextStyles.body,
    color: Colors.light.text,
  },
  plansContainer: {
    gap: Spacing.md,
    marginBottom: Spacing.lg,
  },
  planCard: {
    backgroundColor: Colors.light.card,
    borderRadius: BorderRadius.lg,
    padding: Spacing.lg,
    borderWidth: 2,
    borderColor: Colors.light.border,
    alignItems: "center",
  },
  planCardPopular: {
    borderColor: Colors.light.primary,
    backgroundColor: Colors.light.primaryLight + "10",
  },
  popularBadge: {
    position: "absolute",
    top: -12,
    backgroundColor: Colors.light.primary,
    paddingHorizontal: Spacing.md,
    paddingVertical: 4,
    borderRadius: BorderRadius.full,
  },
  popularText: {
    color: "#FFFFFF",
    fontSize: Typography.sizes.xs,
    fontWeight: Typography.weights.bold,
  },
  planName: {
    ...TextStyles.h4,
    color: Colors.light.text,
    marginBottom: Spacing.xs,
  },
  planPrice: {
    ...TextStyles.h2,
    color: Colors.light.primary,
    fontWeight: Typography.weights.bold,
  },
  planPeriod: {
    ...TextStyles.bodySmall,
    color: Colors.light.textSecondary,
  },
  planSavings: {
    ...TextStyles.bodySmall,
    color: Colors.light.secondary,
    fontWeight: Typography.weights.semibold,
    marginTop: Spacing.xs,
  },
  restoreButton: {
    padding: Spacing.md,
    alignItems: "center",
  },
  restoreText: {
    ...TextStyles.body,
    color: Colors.light.primary,
    fontWeight: Typography.weights.semibold,
  },
  terms: {
    ...TextStyles.caption,
    color: Colors.light.textTertiary,
    textAlign: "center",
    marginTop: Spacing.lg,
  },
  noPlansText: {
    ...TextStyles.body,
    color: Colors.light.textSecondary,
    textAlign: "center",
    marginVertical: Spacing.xl,
  },
});
