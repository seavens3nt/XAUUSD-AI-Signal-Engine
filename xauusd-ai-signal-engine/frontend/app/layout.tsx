import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "XAUUSD AI Signal Engine",
  description: "Paper-trading assisted XAUUSD signal dashboard"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
