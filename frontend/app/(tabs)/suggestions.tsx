import React, { useState } from "react";
import { StyleSheet, ScrollView, View, Text, Alert } from "react-native";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { DisclaimerBanner } from "@/components/ui/DisclaimerBanner";
import { Colors } from "@/constants/Colors";
import { Spacing } from "@/constants/Layout";
import { TextStyles } from "@/constants/Typography";
import { api } from "@/services/api";
import { StrategyType } from "@/types/api";
import type { GenerateSuggestionsRequest, Suggestion } from "@/types/api";

export default function SuggestionsScreen() {
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<Suggestion[] | null>(null);
  const [selectedStrategy, setSelectedStrategy] = useState<StrategyType>(
    StrategyType.BALANCED,
  );

  const strategies: Array<{
    id: StrategyType;
    name: string;
    description: string;
  }> = [
    {
      id: StrategyType.BALANCED,
      name: "Balanceado",
      description: "Mix equilibrado de números quentes e frios",
    },
    {
      id: StrategyType.HOT_NUMBERS,
      name: "Números Quentes",
      description: "Foca em números mais sorteados",
    },
    {
      id: StrategyType.COLD_NUMBERS,
      name: "Números Frios",
      description: "Foca em números menos sorteados",
    },
    {
      id: StrategyType.WEIGHTED_RANDOM,
      name: "Aleatório Ponderado",
      description: "Aleatoriedade com peso estatístico",
    },
    {
      id: StrategyType.RECENT_PATTERNS,
      name: "Padrões Recentes",
      description: "Baseado em sorteios recentes",
    },
  ];

  const handleGenerateSuggestions = async () => {
    try {
      setLoading(true);
      const request: GenerateSuggestionsRequest = {
        strategy: selectedStrategy,
        count: 3,
        user_id: "demo_user", // TODO: Replace with actual user ID from auth
      };

      const response = await api.generateSuggestions(request);
      setSuggestions(response.suggestions);
    } catch (error) {
      Alert.alert(
        "Erro",
        error instanceof Error ? error.message : "Erro ao gerar sugestões",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Gambling Policy Disclaimer Banner */}
      <DisclaimerBanner />

      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>🎲 Gerar Sugestões</Text>
        <Text style={styles.subtitle}>
          Escolha uma estratégia e gere suas sugestões
        </Text>
      </View>

      {/* Strategy Selection */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Escolha a Estratégia</Text>
        {strategies.map((strategy) => (
          <Card
            key={strategy.id}
            padding="md"
            style={StyleSheet.flatten([
              styles.strategyCard,
              selectedStrategy === strategy.id && styles.strategyCardSelected,
            ])}
          >
            <Button
              title={strategy.name}
              onPress={() => setSelectedStrategy(strategy.id)}
              variant={selectedStrategy === strategy.id ? "primary" : "outline"}
              fullWidth
            />
            <Text style={styles.strategyDescription}>
              {strategy.description}
            </Text>
          </Card>
        ))}
      </View>

      {/* Generate Button */}
      <Button
        title="Gerar Sugestões"
        onPress={handleGenerateSuggestions}
        loading={loading}
        disabled={loading}
        size="large"
        fullWidth
        style={styles.generateButton}
      />

      {/* Results */}
      {loading && <LoadingSpinner text="Gerando sugestões..." />}

      {suggestions && !loading && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Suas Sugestões</Text>

          {/* Inline disclaimer required by Google Play gambling policy */}
          <View style={styles.inlineDisclaimer}>
            <Text style={styles.inlineDisclaimerText}>
              ⚠️ Sugestões baseadas em análise estatística histórica. Os
              resultados da loteria são aleatórios —{" "}
              <Text style={styles.inlineDisclaimerBold}>
                nenhum método garante premiação.
              </Text>
            </Text>
          </View>
          {suggestions.map((suggestion, index) => (
            <Card
              key={index}
              elevated
              padding="md"
              style={styles.suggestionCard}
            >
              <Text style={styles.suggestionTitle}>Sugestão {index + 1}</Text>
              <View style={styles.numbersContainer}>
                {suggestion.numbers.map((number, numIndex) => (
                  <View key={numIndex} style={styles.numberBall}>
                    <Text style={styles.numberText}>{number}</Text>
                  </View>
                ))}
              </View>
            </Card>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.light.background,
  },
  content: {
    padding: Spacing.lg,
  },
  header: {
    marginBottom: Spacing.xl,
    alignItems: "center",
  },
  title: {
    ...TextStyles.h1,
    color: Colors.light.text,
    marginBottom: Spacing.xs,
  },
  subtitle: {
    ...TextStyles.body,
    color: Colors.light.textSecondary,
    textAlign: "center",
  },
  section: {
    marginBottom: Spacing.xl,
  },
  sectionTitle: {
    ...TextStyles.h3,
    color: Colors.light.text,
    marginBottom: Spacing.md,
  },
  strategyCard: {
    marginBottom: Spacing.md,
  },
  strategyCardSelected: {
    borderWidth: 2,
    borderColor: Colors.light.primary,
  },
  strategyDescription: {
    ...TextStyles.bodySmall,
    color: Colors.light.textSecondary,
    marginTop: Spacing.sm,
    textAlign: "center",
  },
  generateButton: {
    marginBottom: Spacing.xl,
  },
  suggestionCard: {
    marginBottom: Spacing.md,
  },
  suggestionTitle: {
    ...TextStyles.h4,
    color: Colors.light.text,
    marginBottom: Spacing.md,
  },
  numbersContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: Spacing.sm,
  },
  numberBall: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: Colors.light.primary,
    alignItems: "center",
    justifyContent: "center",
  },
  numberText: {
    ...TextStyles.body,
    color: "#FFFFFF",
    fontWeight: "700",
  },
  inlineDisclaimer: {
    backgroundColor: "#FFFBEB",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#FDE68A",
    padding: Spacing.sm,
    marginBottom: Spacing.md,
  },
  inlineDisclaimerText: {
    ...TextStyles.bodySmall,
    color: "#92400E",
    lineHeight: 20,
  },
  inlineDisclaimerBold: {
    fontWeight: "700",
  },
});
