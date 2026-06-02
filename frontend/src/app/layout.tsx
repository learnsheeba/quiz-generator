import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Quiz Generator",
  description: "Topic-based quiz generator"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
