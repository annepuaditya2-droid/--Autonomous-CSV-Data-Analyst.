import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
const inter = Inter({ subsets: ["latin"] });
export const metadata: Metadata = {
  title: "StatBot Pro",
  description: "Enterprise AI Data Analyst",
};
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      {/* 2. Apply the font to the entire body of the app */}
      <body className={inter.className}>{children}</body>
    </html>
  );
}