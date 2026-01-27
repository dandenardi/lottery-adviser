# Lottery Adviser - Mobile App

Aplicativo mobile React Native/Expo para análise e sugestões de números da Lotofácil.

## 🚀 Quick Start

### Pré-requisitos

- Node.js 18+
- npm ou yarn
- Expo CLI
- Android Studio (para Android) ou Xcode (para iOS)

### Instalação

```bash
# Instalar dependências
npm install

# Copiar arquivo de ambiente
cp .env.example .env

# Editar .env com suas configurações
# API_BASE_URL=http://localhost:5000
```

### Executar o App

```bash
# Desenvolvimento com Expo Go
npm start

# Android
npm run android

# iOS (apenas macOS)
npm run ios

# Web
npm run web
```

## 📁 Estrutura do Projeto

```
frontend/
├── app/                    # Expo Router screens
│   ├── (tabs)/            # Tab navigation
│   │   ├── index.tsx      # Home screen
│   │   ├── statistics.tsx # Statistics screen
│   │   ├── suggestions.tsx # Suggestions screen
│   │   ├── history.tsx    # History screen
│   │   └── profile.tsx    # Profile/Settings
│   ├── _layout.tsx        # Root layout
│   └── +not-found.tsx     # 404 screen
├── components/            # Reusable components
│   ├── ui/               # UI primitives
│   ├── lottery/          # Lottery-specific components
│   └── premium/          # Premium/paywall components
├── services/             # API and business logic
│   ├── api.ts           # API client
│   ├── revenuecat.ts    # RevenueCat integration
│   └── storage.ts       # AsyncStorage utilities
├── hooks/                # Custom React hooks
├── constants/            # App constants
├── types/                # TypeScript types
└── utils/                # Utility functions
```

## 🎨 Design System

### Cores

- **Primary (Verde)**: `#10B981` - Representa sorte
- **Secondary (Dourado)**: `#F59E0B` - Representa prêmio
- **Background**: `#FFFFFF` (light) / `#111827` (dark)

### Navegação

- Tab navigation com 5 tabs principais
- File-based routing com Expo Router

## 💰 Monetização

### Modelo Freemium

- **Free**: 3 sugestões por dia
- **Premium**: Sugestões ilimitadas
  - R$ 0,99/dia
  - R$ 29,90/mês (melhor valor)
  - R$ 299,90/ano (economia de 18%)

### RevenueCat Setup

1. Criar conta em [RevenueCat](https://www.revenuecat.com/)
2. Criar projeto "Lottery Adviser"
3. Configurar produtos (daily, monthly, yearly)
4. Criar entitlement "premium"
5. Adicionar API key no `.env`

## 🔧 Tecnologias

- **Framework**: React Native + Expo
- **Routing**: Expo Router (file-based)
- **State Management**: React Query
- **HTTP Client**: Axios
- **Payments**: RevenueCat
- **Storage**: AsyncStorage
- **Animations**: React Native Reanimated

## 📝 Próximos Passos

- [ ] Implementar telas principais
- [ ] Criar componentes de UI
- [ ] Integrar com backend API
- [ ] Configurar RevenueCat
- [ ] Adicionar testes
- [ ] Preparar para publicação

## 🔗 Links Úteis

- [Expo Documentation](https://docs.expo.dev/)
- [React Native Documentation](https://reactnative.dev/)
- [RevenueCat Documentation](https://www.revenuecat.com/docs)
- [Backend API](../backend/README.md)

## 📄 Licença

Proprietary - Todos os direitos reservados
