import { Paywall } from "@/components/premium/Paywall";
import { useSubscription } from "@/context/SubscriptionContext";
import { useRouter } from "expo-router";

export default function ModalScreen() {
  const { purchasePackage, restorePurchases } = useSubscription();
  const router = useRouter();

  return (
    <Paywall
      visible={true}
      onClose={() => router.back()}
      onPurchase={purchasePackage}
      onRestore={restorePurchases}
    />
  );
}

