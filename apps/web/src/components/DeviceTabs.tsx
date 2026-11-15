"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const TABS = [
  { segment: "overview", label: "Ringkasan" },
  { segment: "analytics", label: "Analitik" },
  { segment: "schedules", label: "Jadwal" },
  { segment: "automation", label: "Otomasi" },
  { segment: "events", label: "Event" },
  { segment: "diagnostics", label: "Diagnostik" },
  { segment: "settings", label: "Pengaturan" }
];

export function DeviceTabs({ deviceId }: { deviceId: string }) {
  const pathname = usePathname();
  return (
    <nav className="device-tabs" aria-label="Navigasi perangkat">
      {TABS.map((tab) => {
        const href = `/devices/${deviceId}/${tab.segment}`;
        const active = pathname === href;
        return (
          <Link key={tab.segment} href={href} className={active ? "device-tab active" : "device-tab"}>
            {tab.label}
          </Link>
        );
      })}
    </nav>
  );
}
