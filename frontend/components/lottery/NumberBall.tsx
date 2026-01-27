/**
 * NumberBall Component
 * Displays a lottery number in a circular ball with color coding
 */

import React from "react";
import { View, Text, StyleSheet, ViewStyle } from "react-native";
import { Colors } from "@/constants/Colors";
import { Typography } from "@/constants/Typography";

type NumberType = "hot" | "cold" | "neutral";
type BallSize = "small" | "medium" | "large";

interface NumberBallProps {
  number: number;
  type?: NumberType;
  size?: BallSize;
  style?: ViewStyle;
}

const BALL_SIZES = {
  small: 32,
  medium: 44,
  large: 56,
};

const FONT_SIZES = {
  small: Typography.sizes.sm,
  medium: Typography.sizes.lg,
  large: Typography.sizes["2xl"],
};

export function NumberBall({
  number,
  type = "neutral",
  size = "medium",
  style,
}: NumberBallProps) {
  const ballSize = BALL_SIZES[size];
  const fontSize = FONT_SIZES[size];

  const backgroundColor =
    type === "hot"
      ? Colors.light.numberHot
      : type === "cold"
        ? Colors.light.numberCold
        : Colors.light.numberNeutral;

  return (
    <View
      style={[
        styles.ball,
        {
          width: ballSize,
          height: ballSize,
          borderRadius: ballSize / 2,
          backgroundColor,
        },
        style,
      ]}
    >
      <Text style={[styles.number, { fontSize }]}>{number}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  ball: {
    justifyContent: "center",
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 3,
  },
  number: {
    color: "#FFFFFF",
    fontWeight: Typography.weights.bold,
  },
});
