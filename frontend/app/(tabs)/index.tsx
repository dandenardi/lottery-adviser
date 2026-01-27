import React from "react";
import {
  StyleSheet,
  ScrollView,
  View,
  Text,
  RefreshControl,
} from "react-native";
import { router } from "expo-router";
import { useLatestResult } from "@/hooks/useLatestResult";
import { useStatistics } from "@/hooks/useStatistics";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { ErrorMessage } from "@/components/ui/ErrorMessage";
import { Button } from "@/components/ui/Button";
import { ResultCard } from "@/components/lottery/ResultCard";
import { StatCard } from "@/components/lottery/StatCard";
import { Colors } from "@/constants/Colors";
import { Spacing } from "@/constants/Layout";
import { TextStyles } from "@/constants/Typography";

export default function HomeScreen() {
  const {
    data: latestResult,
    isLoading: isLoadingResult,
    error: resultError,
    refetch: refetchResult,
  } = useLatestResult();

  const {
    data: statistics,
    isLoading: isLoadingStats,
    error: statsError,
    refetch: refetchStats,
  } = useStatistics();

  const [refreshing, setRefreshing] = React.useState(false);

  const onRefresh = async () => {
    setRefreshing(true);
    await Promise.all([refetchResult(), refetchStats()]);
    setRefreshing(false);
  };

  // Loading state
  if (isLoadingResult && isLoadingStats) {
    return <LoadingSpinner text="Carregando dados..." />;
  }

  // Error state
  if (resultError || statsError) {
    return (
      <ErrorMessage
        message={
          resultError?.message ||
          statsError?.message ||
          "Erro ao carregar dados"
        }
        onRetry={onRefresh}
      />
    );
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={onRefresh}
          tintColor={Colors.light.primary}
        />
      }
    >
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>🍀 Lottery Adviser</Text>
        <Text style={styles.subtitle}>
          Seu assistente inteligente de loteria
        </Text>
      </View>

      {/* Latest Result */}
      {latestResult && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Último Resultado</Text>
          <ResultCard
            result={{
              contest_number: latestResult.contest,
              draw_date: latestResult.date,
              numbers: latestResult.numbers,
            }}
          />
        </View>
      )}

      {/* Quick Stats */}
      {statistics && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Estatísticas Rápidas</Text>

          <View style={styles.statsGrid}>
            <StatCard
              icon="📊"
              title="Total de Concursos"
              value={statistics.total_contests}
              variant="primary"
              style={styles.statCard}
            />

            <StatCard
              icon="🔥"
              title="Número Mais Sorteado"
              value={statistics.most_common_numbers[0]?.number || "-"}
              description={`${statistics.most_common_numbers[0]?.frequency || 0} vezes`}
              variant="secondary"
              style={styles.statCard}
            />

            <StatCard
              icon="📈"
              title="Soma Média"
              value={Math.round(statistics.average_sum)}
              description="dos números sorteados"
              style={styles.statCard}
            />

            <StatCard
              icon="⚖️"
              title="Distribuição Par/Ímpar"
              value={`${statistics.even_odd_distribution.even_percentage.toFixed(0)}% / ${statistics.even_odd_distribution.odd_percentage.toFixed(0)}%`}
              description="pares / ímpares"
              style={styles.statCard}
            />
          </View>
        </View>
      )}

      {/* CTA for Suggestions */}
      <View style={styles.ctaSection}>
        <Text style={styles.ctaTitle}>Pronto para jogar?</Text>
        <Text style={styles.ctaSubtitle}>
          Gere sugestões inteligentes baseadas em estatísticas
        </Text>
        <Button
          title="Gerar Sugestões"
          onPress={() => router.push("/(tabs)/suggestions")}
          size="large"
          fullWidth
          style={styles.ctaButton}
        />
      </View>
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
  },
  section: {
    marginBottom: Spacing.xl,
  },
  sectionTitle: {
    ...TextStyles.h3,
    color: Colors.light.text,
    marginBottom: Spacing.md,
  },
  statsGrid: {
    gap: Spacing.md,
  },
  statCard: {
    marginBottom: 0,
  },
  ctaSection: {
    alignItems: "center",
    marginTop: Spacing.lg,
    marginBottom: Spacing.xl,
  },
  ctaTitle: {
    ...TextStyles.h2,
    color: Colors.light.text,
    marginBottom: Spacing.sm,
  },
  ctaSubtitle: {
    ...TextStyles.body,
    color: Colors.light.textSecondary,
    textAlign: "center",
    marginBottom: Spacing.lg,
  },
  ctaButton: {
    minWidth: 200,
  },
});
