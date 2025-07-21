import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Makers Tech - AI-Powered Shopping Assistant",
  description: "Experience the future of online shopping with our AI assistant Makerito. Get personalized product recommendations, instant answers, and discover the perfect tech gadgets tailored just for you.",
  keywords: "AI shopping, personalized recommendations, tech gadgets, e-commerce, artificial intelligence, Makerito, online shopping assistant",
  authors: [{ name: "Makers Tech" }],
  robots: "index, follow",
  openGraph: {
    title: "Makers Tech - AI-Powered Shopping Assistant",
    description: "Experience the future of online shopping with our AI assistant Makerito. Get personalized product recommendations and discover perfect tech gadgets.",
    type: "website",
    locale: "en_US",
  },
};

export const viewport = {
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans antialiased`}>
        {children}
      </body>
    </html>
  );
}
