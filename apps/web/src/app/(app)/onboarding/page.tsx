import Link from "next/link";

export default function OnboardingPage() {
  return (
    <div className="stack">
      <header className="page-head">
        <div>
          <p className="eyebrow">Onboarding</p>
          <h1>Mulai dengan perangkat</h1>
          <p className="muted">Klaim perangkat, lalu buka ringkasan untuk kontrol dan diagnostik.</p>
        </div>
      </header>
      <section className="panel">
        <h2>Langkah</h2>
        <ol className="check-list">
          <li>Nyalakan perangkat pada kondisi aman (tanpa beban mains untuk prototipe lab).</li>
          <li>Gunakan BLE + fallback SoftAP untuk provisioning Wi-Fi (firmware).</li>
          <li>Masukkan kode pairing sekali pakai di halaman klaim.</li>
          <li>Periksa status, sensor, dan lockout sebelum menghubungkan beban apa pun.</li>
        </ol>
        <Link href="/onboarding/pair-device" className="button button-primary">
          Buka halaman klaim
        </Link>
      </section>
    </div>
  );
}
