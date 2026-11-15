"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";

const LINKS = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/devices", label: "Perangkat" },
  { href: "/settings/tariffs", label: "Tarif" },
  { href: "/settings/notifications", label: "Notifikasi" }
];

export function AppNav() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuth();

  return (
    <header className="app-nav">
      <div className="app-nav-inner">
        <Link href="/dashboard" className="brand" aria-label="Smart Plug dashboard">
          <span className="brand-mark" aria-hidden="true" />
          <span>Smart Plug</span>
        </Link>
        <nav aria-label="Navigasi utama">
          {LINKS.map((link) => {
            const active = pathname === link.href || pathname.startsWith(`${link.href}/`);
            return (
              <Link key={link.href} href={link.href} className={active ? "nav-link active" : "nav-link"}>
                {link.label}
              </Link>
            );
          })}
        </nav>
        <div className="nav-user">
          <span title={user?.email}>{user?.display_name ?? "Pengguna"}</span>
          <button
            type="button"
            className="button button-small button-secondary"
            onClick={() => {
              void logout().then(() => router.replace("/login"));
            }}
          >
            Keluar
          </button>
        </div>
      </div>
    </header>
  );
}
