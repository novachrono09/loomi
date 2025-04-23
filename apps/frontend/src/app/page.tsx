import { Hero } from '../components/hero';
import { ProductGrid } from '../components/product-grid';
import { AIChatWidget } from '../components/AIChatWidget';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center">
      <Hero />
      <ProductGrid />
      <AIChatWidget />
    </main>
  );
}
