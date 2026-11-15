"use client";

import type { ReactNode } from "react";
import { AuthGate } from "@/components/AuthGate";
import { AppNav } from "@/components/AppNav";

export default function AppLayout({ children }: { children: ReactNode }) {
  return (
    <AuthGate>
      <AppNav />
      <main id="main-content" className="page">
        {children}
      </main>
    </AuthGate>
  );
}
