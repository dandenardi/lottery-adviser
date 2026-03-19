import React, { useEffect, useState } from "react";
import {
  Modal,
  View,
  Text,
  ScrollView,
  Pressable,
  StyleSheet,
  BackHandler,
  Platform,
} from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Colors } from "@/constants/Colors";
import { Spacing } from "@/constants/Layout";
import { TextStyles } from "@/constants/Typography";

const DISCLAIMER_ACCEPTED_KEY = "@lottery_adviser:disclaimer_accepted_v1";

/**
 * First-run consent modal.
 * Shown once when the user opens the app for the first time.
 * The user must confirm they are 18+ and understand no results are guaranteed.
 * Required for Google Play gambling content policy compliance.
 */
export function GamblingDisclaimerModal() {
  const [visible, setVisible] = useState(false);
  const [accepted, setAccepted] = useState(false);

  useEffect(() => {
    checkFirstRun();
  }, []);

  const checkFirstRun = async () => {
    try {
      const value = await AsyncStorage.getItem(DISCLAIMER_ACCEPTED_KEY);
      if (value === null) {
        setVisible(true);
      }
    } catch {
      // If storage fails, show the modal to be safe
      setVisible(true);
    }
  };

  const handleAccept = async () => {
    try {
      await AsyncStorage.setItem(DISCLAIMER_ACCEPTED_KEY, "true");
    } catch {
      // Proceed even if storage fails
    }
    setVisible(false);
  };

  const handleExit = () => {
    if (Platform.OS === "android") {
      BackHandler.exitApp();
    }
    // On iOS we cannot force-exit; do nothing (the modal stays.)
  };

  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
      statusBarTranslucent
      onRequestClose={() => {
        /* Prevent hardware back closing the modal before acceptance */
      }}
    >
      <View style={styles.overlay}>
        <View style={styles.card}>
          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.headerIcon}>⚠️</Text>
            <Text style={styles.headerTitle}>Aviso Importante</Text>
          </View>

          {/* Body */}
          <ScrollView
            style={styles.body}
            contentContainerStyle={styles.bodyContent}
            showsVerticalScrollIndicator={false}
          >
            <Text style={styles.bodyText}>
              O <Text style={styles.bold}>Lottery Adviser</Text> é uma
              ferramenta de análise estatística para loterias da Caixa Econômica
              Federal. Este aplicativo:
            </Text>

            <View style={styles.bulletContainer}>
              <BulletItem text="NÃO garante prêmios ou resultados favoráveis." />
              <BulletItem text="NÃO realiza apostas em seu nome." />
              <BulletItem text="NÃO está vinculado à Caixa Econômica Federal." />
              <BulletItem text="Fornece sugestões baseadas exclusivamente em análise estatística histórica." />
              <BulletItem text="Resultados de loteria são sorteios aleatórios; nenhum método prevê os números vencedores." />
            </View>

            <Text style={styles.bodyText}>
              Apostar pode causar dependência. Jogue com responsabilidade e
              dentro dos seus limites financeiros.
            </Text>

            <Text style={[styles.bodyText, styles.ageWarning]}>
              🔞 Este aplicativo é destinado exclusivamente a maiores de 18
              anos.
            </Text>
          </ScrollView>

          {/* Checkbox */}
          <Pressable
            style={styles.checkboxRow}
            onPress={() => setAccepted((prev) => !prev)}
            accessibilityRole="checkbox"
            accessibilityState={{ checked: accepted }}
            accessibilityLabel="Confirmo que tenho mais de 18 anos e entendo que este app não garante prêmios"
          >
            <View style={[styles.checkbox, accepted && styles.checkboxChecked]}>
              {accepted && <Text style={styles.checkmark}>✓</Text>}
            </View>
            <Text style={styles.checkboxLabel}>
              Tenho mais de 18 anos e entendo que este app{" "}
              <Text style={styles.bold}>não garante prêmios</Text>.
            </Text>
          </Pressable>

          {/* Actions */}
          <View style={styles.actions}>
            <Pressable
              style={[
                styles.button,
                styles.buttonPrimary,
                !accepted && styles.buttonDisabled,
              ]}
              onPress={handleAccept}
              disabled={!accepted}
              accessibilityRole="button"
              accessibilityLabel="Concordar e continuar"
              accessibilityState={{ disabled: !accepted }}
            >
              <Text style={[styles.buttonText, styles.buttonPrimaryText]}>
                Concordar e Continuar
              </Text>
            </Pressable>

            <Pressable
              style={[styles.button, styles.buttonSecondary]}
              onPress={handleExit}
              accessibilityRole="button"
              accessibilityLabel="Sair do aplicativo"
            >
              <Text style={[styles.buttonText, styles.buttonSecondaryText]}>
                Sair do App
              </Text>
            </Pressable>
          </View>
        </View>
      </View>
    </Modal>
  );
}

function BulletItem({ text }: { text: string }) {
  return (
    <View style={styles.bulletItem}>
      <Text style={styles.bulletDot}>•</Text>
      <Text style={styles.bulletText}>{text}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.7)",
    justifyContent: "center",
    alignItems: "center",
    padding: Spacing.lg,
  },
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 16,
    width: "100%",
    maxHeight: "85%",
    overflow: "hidden",
  },
  header: {
    backgroundColor: Colors.light.warning,
    paddingVertical: Spacing.md,
    paddingHorizontal: Spacing.lg,
    flexDirection: "row",
    alignItems: "center",
    gap: Spacing.sm,
  },
  headerIcon: {
    fontSize: 22,
  },
  headerTitle: {
    ...TextStyles.h3,
    color: "#FFFFFF",
    fontWeight: "700",
  },
  body: {
    maxHeight: 320,
  },
  bodyContent: {
    padding: Spacing.lg,
    gap: Spacing.md,
  },
  bodyText: {
    ...TextStyles.body,
    color: Colors.light.text,
    lineHeight: 22,
    marginBottom: Spacing.sm,
  },
  bold: {
    fontWeight: "700",
  },
  ageWarning: {
    backgroundColor: "#FEF3C7",
    borderRadius: 8,
    padding: Spacing.sm,
    fontWeight: "700",
  },
  bulletContainer: {
    gap: Spacing.xs,
    marginBottom: Spacing.sm,
  },
  bulletItem: {
    flexDirection: "row",
    gap: Spacing.sm,
    alignItems: "flex-start",
  },
  bulletDot: {
    ...TextStyles.body,
    color: Colors.light.primary,
    fontWeight: "700",
    lineHeight: 22,
  },
  bulletText: {
    ...TextStyles.body,
    color: Colors.light.text,
    flex: 1,
    lineHeight: 22,
  },
  checkboxRow: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: Spacing.sm,
    padding: Spacing.md,
    borderTopWidth: 1,
    borderTopColor: Colors.light.border,
    backgroundColor: Colors.light.backgroundSecondary,
  },
  checkbox: {
    width: 22,
    height: 22,
    borderWidth: 2,
    borderColor: Colors.light.border,
    borderRadius: 4,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 1,
    flexShrink: 0,
  },
  checkboxChecked: {
    backgroundColor: Colors.light.primary,
    borderColor: Colors.light.primary,
  },
  checkmark: {
    color: "#FFFFFF",
    fontSize: 14,
    fontWeight: "700",
  },
  checkboxLabel: {
    ...TextStyles.body,
    color: Colors.light.text,
    flex: 1,
    lineHeight: 22,
  },
  actions: {
    padding: Spacing.md,
    gap: Spacing.sm,
  },
  button: {
    borderRadius: 10,
    paddingVertical: Spacing.md,
    alignItems: "center",
    justifyContent: "center",
  },
  buttonPrimary: {
    backgroundColor: Colors.light.primary,
  },
  buttonDisabled: {
    backgroundColor: Colors.light.border,
  },
  buttonSecondary: {
    backgroundColor: "transparent",
    borderWidth: 1,
    borderColor: Colors.light.border,
  },
  buttonText: {
    ...TextStyles.body,
    fontWeight: "700",
  },
  buttonPrimaryText: {
    color: "#FFFFFF",
  },
  buttonSecondaryText: {
    color: Colors.light.textSecondary,
  },
});
