"use client";

import { useParams } from "next/navigation";
import { useDiagnostics } from "@/lib/hooks";
import { DeviceHealth } from "@/components/DeviceHealth";
import { ErrorPanel, Loading } from "@/components/Feedback";

export default function DiagnosticsPage() {
  const params = useParams();
  const deviceId = typeof params.id === "string" ? params.id : "";
  const diagnostics = useDiagnostics(deviceId);

  if (diagnostics.loading && !diagnostics.data) return <Loading />;
  if (diagnostics.error && !diagnostics.data) return <ErrorPanel message={diagnostics.error} onRetry={() => void diagnostics.reload()} />;

  return (
    <div className="stack">
      <DeviceHealth diagnostics={diagnostics.data} />
      <section className="panel">
        <h2>Payload diagnostik</h2>
        <p className="muted">
          Data mentah dari perangkat/backend. Jangan menambahkan token, password Wi-Fi, atau secret ke payload ini.
        </p>
        <details>
          <summary>Tampilkan JSON</summary>
          <pre>{JSON.stringify(diagnostics.data, null, 2)}</pre>
        </details>
      </section>
    </div>
  );
}
