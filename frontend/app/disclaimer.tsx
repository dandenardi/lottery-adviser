import React from "react";
import {
  ScrollView,
  View,
  Text,
  Pressable,
  StyleSheet,
  Linking,
} from "react-native";
import { Stack } from "expo-router";
import { Colors } from "@/constants/Colors";
import { Spacing } from "@/constants/Layout";
import { TextStyles } from "@/constants/Typography";

const RESPONSIBLE_GAMBLING_LINKS = [
  {
    label: "CVV – Centro de Valorização da Vida",
    sublabel: "Apoio emocional 24h: ligue 188",
    url: "https://www.cvv.org.br",
  },
  {
    label: "Jogadores Anônimos Brasil",
    sublabel: "Ajuda para dependência em jogos",
    url: "https://www.jogadoresanonimos.com.br",
  },
  {
    label: "Loteria Caixa – Site Oficial",
    sublabel: "Resultados e apostas oficiais",
    url: "https://loterias.caixa.gov.br",
  },
];

export default function DisclaimerScreen() {
  return (
    <>
      <Stack.Screen
        options={{ title: "Aviso Legal", headerBackTitle: "Voltar" }}
      />
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.content}
      >
        {/* Title */}
        <View style={styles.header}>
          <Text style={styles.icon}>⚠️</Text>
          <Text style={styles.title}>Aviso Legal e Jogo Responsável</Text>
        </View>

        {/* Section 1 – About the app */}
        <Section title="Sobre este aplicativo">
          <Paragraph>
            O <Bold>Lottery Adviser</Bold> é uma ferramenta de análise
            estatística para loterias administradas pela Caixa Econômica Federal
            (Mega-Sena, Lotofácil, Quina etc.). O aplicativo processa dados
            históricos de sorteios e gera sugestões de números com base em
            padrões estatísticos.
          </Paragraph>
          <Paragraph>
            Este aplicativo{" "}
            <Bold>não é afiliado, endossado ou patrocinado</Bold> pela Caixa
            Econômica Federal nem por qualquer órgão governamental.
          </Paragraph>
        </Section>

        {/* Section 2 – No guarantees */}
        <Section title="Ausência de Garantias">
          <AlertBox>
            <Bold>
              Nenhuma sugestão gerada por este aplicativo garante premiação.
            </Bold>
          </AlertBox>
          <Paragraph>
            Os resultados das loterias são determinados por sorteios
            completamente aleatórios. Análises estatísticas e padrões históricos{" "}
            <Bold>não têm capacidade preditiva</Bold> sobre sorteios futuros.
            Cada sorteio é um evento independente.
          </Paragraph>
          <Paragraph>
            Não existe nenhum método, algoritmo ou sistema capaz de prever com
            certeza os números sorteados em loterias. Qualquer promessa nesse
            sentido é falsa.
          </Paragraph>
        </Section>

        {/* Section 3 – Entertainment only */}
        <Section title="Uso Exclusivamente Informativo">
          <Paragraph>
            Este aplicativo destina-se exclusivamente ao uso{" "}
            <Bold>informativo e de entretenimento</Bold>. Não é um serviço de
            apostas. As sugestões geradas são apenas pontos de partida para que
            o usuário tome suas próprias decisões.
          </Paragraph>
        </Section>

        {/* Section 4 – Responsible gambling */}
        <Section title="Jogo Responsável">
          <Paragraph>
            Apostar pode ser uma atividade de lazer, mas pode causar
            dependência. Observe os seguintes princípios:
          </Paragraph>
          <BulletList
            items={[
              "Defina um orçamento fixo e nunca aposte mais do que pode perder.",
              "Não tente recuperar perdas aumentando apostas.",
              "Não utilize dinheiro destinado a despesas essenciais (aluguel, alimentação, saúde).",
              "Se sentir que o jogo está afetando sua vida ou de pessoas próximas, procure ajuda.",
            ]}
          />
        </Section>

        {/* Section 5 – Age restriction */}
        <Section title="Restrição de Idade">
          <AlertBox color="#FEE2E2" textColor="#991B1B">
            🔞 Este aplicativo é destinado{" "}
            <Bold>exclusivamente a maiores de 18 anos</Bold>. O uso por menores
            de idade é expressamente proibido.
          </AlertBox>
        </Section>

        {/* Section 6 – External links */}
        <Section title="Ajuda e Suporte">
          {RESPONSIBLE_GAMBLING_LINKS.map((link) => (
            <Pressable
              key={link.url}
              style={styles.linkCard}
              onPress={() => Linking.openURL(link.url)}
              accessibilityRole="link"
              accessibilityLabel={link.label}
            >
              <View style={styles.linkContent}>
                <Text style={styles.linkLabel}>{link.label}</Text>
                <Text style={styles.linkSublabel}>{link.sublabel}</Text>
              </View>
              <Text style={styles.linkArrow}>›</Text>
            </Pressable>
          ))}
        </Section>

        {/* Footer */}
        <Text style={styles.footer}>
          Versão das diretrizes: Fevereiro de 2026 · Conforme Google Play
          Developer Policy
        </Text>
      </ScrollView>
    </>
  );
}

// ─── Local helpers ────────────────────────────────────────────────────────────

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      {children}
    </View>
  );
}

function Paragraph({ children }: { children: React.ReactNode }) {
  return <Text style={styles.paragraph}>{children}</Text>;
}

function Bold({ children }: { children: React.ReactNode }) {
  return <Text style={styles.bold}>{children}</Text>;
}

function AlertBox({
  children,
  color = "#FEF3C7",
  textColor = "#92400E",
}: {
  children: React.ReactNode;
  color?: string;
  textColor?: string;
}) {
  return (
    <View style={[styles.alertBox, { backgroundColor: color }]}>
      <Text style={[styles.alertText, { color: textColor }]}>{children}</Text>
    </View>
  );
}

function BulletList({ items }: { items: string[] }) {
  return (
    <View style={styles.bulletList}>
      {items.map((item, i) => (
        <View key={i} style={styles.bulletItem}>
          <Text style={styles.bulletDot}>•</Text>
          <Text style={styles.bulletText}>{item}</Text>
        </View>
      ))}
    </View>
  );
}

// ─── Styles ───────────────────────────────────────────────────────────────────

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.light.background,
  },
  content: {
    padding: Spacing.lg,
    paddingBottom: Spacing["2xl"],
  },
  header: {
    alignItems: "center",
    marginBottom: Spacing.xl,
    gap: Spacing.sm,
  },
  icon: {
    fontSize: 40,
  },
  title: {
    ...TextStyles.h3,
    color: Colors.light.text,
    textAlign: "center",
  },
  section: {
    marginBottom: Spacing.xl,
  },
  sectionTitle: {
    ...TextStyles.h4,
    color: Colors.light.text,
    marginBottom: Spacing.sm,
    borderLeftWidth: 3,
    borderLeftColor: Colors.light.primary,
    paddingLeft: Spacing.sm,
  },
  paragraph: {
    ...TextStyles.body,
    color: Colors.light.text,
    lineHeight: 24,
    marginBottom: Spacing.sm,
  },
  bold: {
    fontWeight: "700",
  },
  alertBox: {
    borderRadius: 8,
    padding: Spacing.md,
    marginBottom: Spacing.sm,
  },
  alertText: {
    ...TextStyles.body,
    lineHeight: 22,
  },
  bulletList: {
    gap: Spacing.sm,
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
    lineHeight: 24,
  },
  bulletText: {
    ...TextStyles.body,
    color: Colors.light.text,
    flex: 1,
    lineHeight: 24,
  },
  linkCard: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: Colors.light.backgroundSecondary,
    borderRadius: 10,
    padding: Spacing.md,
    marginBottom: Spacing.sm,
    borderWidth: 1,
    borderColor: Colors.light.border,
  },
  linkContent: {
    flex: 1,
    gap: 2,
  },
  linkLabel: {
    ...TextStyles.body,
    color: Colors.light.primary,
    fontWeight: "600",
  },
  linkSublabel: {
    ...TextStyles.bodySmall,
    color: Colors.light.textSecondary,
  },
  linkArrow: {
    fontSize: 22,
    color: Colors.light.textTertiary,
    marginLeft: Spacing.sm,
  },
  footer: {
    ...TextStyles.caption,
    color: Colors.light.textTertiary,
    textAlign: "center",
    marginTop: Spacing.md,
  },
});
