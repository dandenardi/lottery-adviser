/**
 * ResultCard Component
 * Displays a lottery result with contest number, date, and numbers
 */

import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Card } from "@/components/ui/Card";
import { NumberBall } from "./NumberBall";
import { Colors } from "@/constants/Colors";
import { Spacing } from "@/constants/Layout";
import { TextStyles, Typography } from "@/constants/Typography";
import type { LotteryResult } from "@/types/api";

interface ResultCardProps {
  result: {
    contest_number: number;
    draw_date: string;
    numbers: number[];
  };
  onPress?: () => void;
  showDate?: boolean;
}

export function ResultCard({
  result,
  onPress,
  showDate = true,
}: ResultCardProps) {
  const formattedDate = new Date(result.draw_date).toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });

  const content = (
    <Card elevated>
      <View style={styles.header}>
        <Text style={styles.contest}>Concurso {result.contest_number}</Text>
        {showDate && <Text style={styles.date}>{formattedDate}</Text>}
      </View>

      <View style={styles.numbersGrid}>
        {result.numbers.map((number, index) => (
          <NumberBall
            key={`${result.contest_number}-${number}-${index}`}
            number={number}
            size="small"
            style={styles.ball}
          />
        ))}
      </View>
    </Card>
  );

  if (onPress) {
    return (
      <TouchableOpacity onPress={onPress} activeOpacity={0.7}>
        {content}
      </TouchableOpacity>
    );
  }

  return content;
}

const styles = StyleSheet.create({
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: Spacing.md,
  },
  contest: {
    ...TextStyles.h4,
    color: Colors.light.text,
  },
  date: {
    ...TextStyles.bodySmall,
    color: Colors.light.textSecondary,
  },
  numbersGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: Spacing.sm,
  },
  ball: {
    marginBottom: Spacing.xs,
  },
});
