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
import { Button } from "@/components/ui/Button";
import { PremiumBadge } from "./PremiumBadge";
import { Colors } from "@/constants/Colors";
import { Spacing, BorderRadius } from "@/constants/Layout";
import { TextStyles, Typography } from "@/constants/Typography";

interface PaywallProps {
  visible: boolean;
  onClose: () => void;
  onPurchase: (planId: string) => Promise<void>;
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

const PLANS = [
  {
    id: "daily",
    name: "Diário",
    price: "R$ 0,99",
    period: "por dia",
    popular: false,
  },
  {
    id: "monthly",
    name: "Mensal",
    price: "R$ 29,90",
    period: "por mês",
    popular: true,
    savings: "Melhor valor!",
  },
  {
    id: "yearly",
    name: "Anual",
    price: "R$ 299,90",
    period: "por ano",
    popular: false,
    savings: "Economia de 18%",
  },
];

export function Paywall({
  visible,
  onClose,
  onPurchase,
  onRestore,
}: PaywallProps) {
  const [loading, setLoading] = React.useState(false);

  const handlePurchase = async (planId: string) => {
    try {
      setLoading(true);
      await onPurchase(planId);
    } catch (error: any) {
      Alert.alert("Erro", error.message || "Falha ao processar compra");
    } finally {
      setLoading(false);
    }
  };

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
            {PLANS.map((plan) => (
              <TouchableOpacity
                key={plan.id}
                style={[
                  styles.planCard,
                  plan.popular && styles.planCardPopular,
                ]}
                onPress={() => handlePurchase(plan.id)}
                disabled={loading}
              >
                {plan.popular && (
                  <View style={styles.popularBadge}>
                    <Text style={styles.popularText}>MAIS POPULAR</Text>
                  </View>
                )}

                <Text style={styles.planName}>{plan.name}</Text>
                <Text style={styles.planPrice}>{plan.price}</Text>
                <Text style={styles.planPeriod}>{plan.period}</Text>

                {plan.savings && (
                  <Text style={styles.planSavings}>{plan.savings}</Text>
                )}
              </TouchableOpacity>
            ))}
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
});
