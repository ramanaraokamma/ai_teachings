import type { Metadata } from "next";
import "./globals.css";
import "./lesson-book.css";
import "./topic-studio.css";
import "./grade6-learning.css";
import "./curriculum-v3.css";

export const metadata: Metadata = {
  title: { default: "AI Academy", template: "%s | AI Academy" },
  description: "AI Academy for students starting in Grade 6: lessons, practice and protected teacher guidance.",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en"><body>{children}</body></html>
  );
}
