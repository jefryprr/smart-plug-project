import type { DeviceSummary } from "@smartplug/api-contract";
import Link from "next/link";
import { ageLabel } from "@/lib/format";
import { StatusBadge, availabilityBadge, outputBadge } from "./StatusBadge";

export function DeviceSummaryCard({ device }: { device: DeviceSummary }) {
  const availability = availabilityBadge(device.availability);
  const output = outputBadge(device.state.commanded_output);
  const fault = device.state.fault_code;

  return (
    <Link className="device-card" href={`/devices/${device.device_id}/overview`}>
      <div className="device-card-head">
        <div>
          <h3>{device.name}</h3>
          <p className="muted">{device.room ?? "Tanpa ruangan"}</p>
        </div>
        <StatusBadge label={availability.label} tone={availability.tone} />
      </div>
      <div className="device-card-body">
        <div>
          <span className="label">Output</span>
          <StatusBadge label={output.label} tone={output.tone} />
        </div>
        <div>
          <span className="label">Terakhir terlihat</span>
          <strong>{ageLabel(device.last_seen_at)}</strong>
        </div>
        <div>
          <span className="label">Firmware</span>
          <strong>{device.firmware_version ?? "Tidak diketahui"}</strong>
        </div>
      </div>
      {fault ? (
        <p className="inline-alert" role="alert">
          Fault: {fault} — ON diblokir sampai lockout direset secara otoritatif.
        </p>
      ) : null}
      {device.data_source === "SYNTHETIC_DEMO" ? (
        <p className="demo-chip">Data demo sintetik</p>
      ) : null}
    </Link>
  );
}
