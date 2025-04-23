import './styles/globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Providers } from '../providers';
import { Toaster } from '../components/ui/toaster';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Loomi - AI-Powered E-Commerce',
  description: 'Next generation shopping experience powered by AI',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ede9fe' },
    { media: '(prefers-color-scheme: dark)', color: '#4c1d95' },
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          {children}
          <Toaster />
        </Providers>
      </body>
    </html>
  );
}