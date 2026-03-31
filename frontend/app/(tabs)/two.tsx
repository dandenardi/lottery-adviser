import React from "react";
import {
  StyleSheet,
  ScrollView,
  View,
  Text,
  RefreshControl,
  Dimensions,
} from "react-native";
import { useStatistics } from "@/hooks/useStatistics";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { ErrorMessage } from "@/components/ui/ErrorMessage";
import { StatCard } from "@/components/lottery/StatCard";
import { NumberBall } from "@/components/lottery/NumberBall";
import { Card } from "@/components/ui/Card";
import { Colors } from "@/constants/Colors";
import { Spacing, BorderRadius } from "@/constants/Layout";
import { TextStyles, Typography } from "@/constants/Typography";

const { width } = Dimensions.get("window");

export default function StatisticsScreen() {
  const { data: stats, isLoading, error, refetch } = useStatistics();
  const [refreshing, setRefreshing] = React.useState(false);

  const onRefresh = async () => {
    setRefreshing(true);
    await refetch();
    setRefreshing(false);
  };

  if (isLoading && !refreshing) {
    return <LoadingSpinner text="Analisando dados históricos..." />;
  }

  if (error) {
    return (
      <ErrorMessage
        message={error.message || "Erro ao carregar estatísticas"}
        onRetry={onRefresh}
      />
    );
  }

  if (!stats) return null;

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
        <Text style={styles.title}>📊 Estatísticas Avançadas</Text>
        <Text style={styles.subtitle}>
          Análise baseada em {stats.total_contests} concursos
        </Text>
      </View>

      {/* Overview Stats */}
      <View style={styles.statsRow}>
        <StatCard
          icon="📅"
          title="Período"
          value={
            stats.date_range.start && stats.date_range.end
              ? `${new Date(stats.date_range.start).getFullYear()} - ${new Date(stats.date_range.end).getFullYear()}`
              : "N/A"
          }
          style={styles.statCardHalf}
        />
        <StatCard
          icon="📈"
          title="Soma Média"
          value={Math.round(stats.average_sum)}
          variant="primary"
          style={styles.statCardHalf}
        />
      </View>

      {/* Hot Numbers */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>🔥 Números Mais Sorteados (Quentes)</Text>
        <Card elevated style={styles.numberGridCard}>
          <View style={styles.numberGrid}>
            {stats.most_common_numbers.slice(0, 10).map((item) => (
              <View key={item.number} style={styles.numberItem}>
                <NumberBall number={item.number} type="hot" size="medium" />
                <Text style={styles.frequencyText}>{item.frequency}x</Text>
              </View>
            ))}
          </View>
        </Card>
      </View>

      {/* Cold Numbers */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>❄️ Números Menos Sorteados (Frios)</Text>
        <Card elevated style={styles.numberGridCard}>
          <View style={styles.numberGrid}>
            {stats.least_common_numbers.slice(0, 10).map((item) => (
              <View key={item.number} style={styles.numberItem}>
                <NumberBall number={item.number} type="cold" size="medium" />
                <Text style={styles.frequencyText}>{item.frequency}x</Text>
              </View>
            ))}
          </View>
        </Card>
      </View>

      {/* Distribution */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>⚖️ Equilíbrio Par/Ímpar</Text>
        <Card elevated padding="lg">
          <View style={styles.distributionContainer}>
            <View style={styles.distLabelRow}>
              <Text style={styles.distLabel}>Pares</Text>
              <Text style={styles.distValue}>{stats.even_odd_distribution.even_percentage.toFixed(1)}%</Text>
            </View>
            <View style={styles.progressBarBg}>
              <View 
                style={[
                  styles.progressBarFill, 
                  { width: `${stats.even_odd_distribution.even_percentage}%`, backgroundColor: Colors.light.primary }
                ]} 
              />
            </View>
            <View style={styles.distLabelRow}>
              <Text style={styles.distLabel}>Ímpares</Text>
              <Text style={styles.distValue}>{stats.even_odd_distribution.odd_percentage.toFixed(1)}%</Text>
            </View>
            <View style={styles.progressBarBg}>
              <View 
                style={[
                  styles.progressBarFill, 
                  { width: `${stats.even_odd_distribution.odd_percentage}%`, backgroundColor: Colors.light.secondary }
                ]} 
              />
            </View>
          </View>
        </Card>
      </View>

      {/* Ranges */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📍 Distribuição por Faixas</Text>
        <Card elevated padding="lg">
          {Object.entries(stats.number_range_distribution).map(([range, count]) => (
            <View key={range} style={styles.rangeRow}>
              <Text style={styles.rangeLabel}>{range}</Text>
              <View style={styles.rangeBarContainer}>
                <View style={styles.rangeBarWrapper}>
                  <View 
                    style={[
                      styles.rangeBar, 
                      { 
                        width: `${Math.min((count / stats.total_contests) * 100 * 3, 100)}%`,
                        backgroundColor: Colors.light.primaryLight 
                      }
                    ]} 
                  />
                </View>
                <Text style={styles.rangeText}>{count} vezes</Text>
              </View>
            </View>
          ))}
        </Card>
      </View>

      <View style={{ height: Spacing.xl }} />
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
  statsRow: {
    flexDirection: "row",
    gap: Spacing.md,
    marginBottom: Spacing.xl,
  },
  statCardHalf: {
    flex: 1,
  },
  numberGridCard: {
    paddingVertical: Spacing.lg,
    paddingHorizontal: Spacing.md,
  },
  numberGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "flex-start",
    gap: Spacing.md,
  },
  numberItem: {
    alignItems: "center",
    width: (width - Spacing.lg * 2 - Spacing.md * 4) / 5,
  },
  frequencyText: {
    ...TextStyles.caption,
    marginTop: 4,
    color: Colors.light.textSecondary,
    fontWeight: "bold",
  },
  distributionContainer: {
    gap: Spacing.sm,
  },
  distLabelRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: Spacing.xs,
  },
  distLabel: {
    ...TextStyles.bodySmall,
    fontWeight: "600",
  },
  distValue: {
    ...TextStyles.bodySmall,
    color: Colors.light.textSecondary,
  },
  progressBarBg: {
    height: 8,
    backgroundColor: Colors.light.borderLight,
    borderRadius: 4,
    overflow: "hidden",
  },
  progressBarFill: {
    height: "100%",
    borderRadius: 4,
  },
  rangeRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: Spacing.md,
  },
  rangeLabel: {
    width: 70,
    ...TextStyles.bodySmall,
    color: Colors.light.textSecondary,
  },
  rangeBarContainer: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    gap: Spacing.sm,
  },
  rangeBarWrapper: {
    flex: 1,
    height: 12,
    justifyContent: "center",
  },
  rangeBar: {
    height: 12,
    borderRadius: 6,
  },
  rangeText: {
    ...TextStyles.caption,
    color: Colors.light.textTertiary,
    minWidth: 60,
    textAlign: "right",
  },
});
