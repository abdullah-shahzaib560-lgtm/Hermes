import type { Metadata } from "next";
import { Nunito_Sans, Baloo_2 } from "next/font/google";
import "./globals.css";

const nunito = Nunito_Sans({
  variable: "--font-nunito",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
});

const baloo = Baloo_2({
  variable: "--font-jayagiri-fallback",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  title: {
    default: "Hermes — The Data Engine for Python",
    template: "%s · Hermes",
  },
  description:
    "Hermes is a foundational intelligence data platform for acquiring, validating, normalizing, storing, and serving intelligence datasets.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${nunito.variable} ${baloo.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-cream text-ink">{children}</body>
    </html>
  );
}
