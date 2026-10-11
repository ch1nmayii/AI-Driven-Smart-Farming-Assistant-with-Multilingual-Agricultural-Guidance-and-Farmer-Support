import type { Metadata, Viewport } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Kisan AI - Smart Multilingual Farming Assistant',
  description: 'AI-driven agricultural voice guidance and farmer support platform',
  manifest: '/manifest.json',
  icons: {
    icon: '/icon-192.png',
  },
};

export const viewport: Viewport = {
  themeColor: '#16a34a',
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-b from-emerald-950 via-slate-950 to-emerald-950 text-emerald-50 antialiased selection:bg-emerald-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
