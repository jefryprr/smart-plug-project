import React, { useCallback, useEffect, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View
} from "react-native";
import { StatusBar } from "expo-status-bar";
import * as SecureStore from "expo-secure-store";

const TOKEN_KEY = "smartplug.access";
const API_KEY = "smartplug.apiBase";

type Screen =
  | { name: "devices" }
  | { name: "device"; deviceId: string }
  | { name: "settings" };

interface DeviceState {
  commanded_output: "ON" | "OFF";
  observed_output: "ON" | "OFF" | null;
  lockout: boolean;
  fault_code: string | null;
  state_version: number;
  last_transition_at: string;
  clock_valid: boolean;
  meter_valid: boolean;
  temperature_valid: boolean;
  time_valid?: boolean;
  time_source?: "sntp" | "api" | "mqtt" | "manual" | "none";
  last_sync?: string | null;
  last_known_time?: string | null;
  time_age_s?: number | null;
}

interface DeviceSummary {
  device_id: string;
  name: string;
  room: string | null;
  availability: "ONLINE" | "STALE" | "OFFLINE" | "NEVER_SEEN";
  last_seen_at: string | null;
  state: DeviceState;
  firmware_version: string | null;
  data_source: "DEVICE" | "SIMULATOR" | "SYNTHETIC_DEMO" | "UNKNOWN";
  created_at: string;
  role?: "owner" | "admin" | "viewer";
}

interface TelemetrySample {
  sampled_at: string;
  quality: "VALID" | "STALE" | "INVALID";
  voltage_v: number | null;
  current_a: number | null;
  active_power_w: number | null;
  energy_kwh_total: number | null;
  power_factor: number | null;
  frequency_hz: number | null;
}

interface EventItem {
  event_id: string;
  type: string;
  severity: "INFO" | "WARNING" | "CRITICAL";
  occurred_at: string;
  summary: string;
}

interface CommandResult {
  command_id: string;
  status: "PENDING" | "ACCEPTED" | "DELIVERED" | "APPLIED" | "REJECTED" | "EXPIRED" | "TIMEOUT";
  message: string;
}

const STATUS_COLORS: Record<string, string> = {
  ONLINE: "#067647",
  STALE: "#9a5b00",
  OFFLINE: "#b42318",
  NEVER_SEEN: "#5b677a",
  ON: "#067647",
  OFF: "#5b677a"
};

function formatTime(iso: string | null): string {
  if (!iso) return "Belum pernah";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "Waktu tidak valid";
  return date.toLocaleString("id-ID", { dateStyle: "medium", timeStyle: "short" });
}

function formatNumber(value: number | null, digits = 1): string {
  if (value === null || !Number.isFinite(value)) return "—";
  return value.toLocaleString("id-ID", { maximumFractionDigits: digits, minimumFractionDigits: digits });
}

function formatIdr(value: number | null): string {
  if (value === null || !Number.isFinite(value)) return "—";
  return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", maximumFractionDigits: 0 }).format(value);
}

async function apiFetch<T>(
  baseUrl: string,
  path: string,
  token: string | null,
  options: { method?: string; body?: unknown } = {}
): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, {
    method: options.method ?? "GET",
    headers: {
      ...(options.body ? { "content-type": "application/json" } : {}),
      ...(token ? { authorization: `Bearer ${token}` } : {})
    },
    body: options.body ? JSON.stringify(options.body) : undefined
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as { error?: { message?: string; code?: string } } | null;
    throw new Error(body?.error?.message ?? `HTTP ${response.status}`);
  }
  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}

export default function App() {
  const [baseUrl, setBaseUrl] = useState("http://10.0.2.2:4000");
  const [email, setEmail] = useState("demo@example.com");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState<string | null>(null);
  const [screen, setScreen] = useState<Screen>({ name: "devices" });
  const [devices, setDevices] = useState<DeviceSummary[]>([]);
  const [selected, setSelected] = useState<DeviceSummary | null>(null);
  const [telemetry, setTelemetry] = useState<TelemetrySample | null>(null);
  const [events, setEvents] = useState<EventItem[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [command, setCommand] = useState<CommandResult | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      const storedApi = await SecureStore.getItemAsync(API_KEY).catch(() => null);
      const storedToken = await SecureStore.getItemAsync(TOKEN_KEY).catch(() => null);
      if (storedApi) setBaseUrl(storedApi);
      if (storedToken) setToken(storedToken);
    })();
  }, []);

  const loadDevices = useCallback(async () => {
    if (!token) return;
    try {
      const body = await apiFetch<{ devices: DeviceSummary[] }>(baseUrl, "/api/v1/devices", token);
      setDevices(body.devices);
      setError(null);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Gagal memuat perangkat");
    }
  }, [baseUrl, token]);

  const loadSelected = useCallback(
    async (deviceId: string) => {
      if (!token) return;
      try {
        const [detail, telemetryBody, eventsBody] = await Promise.all([
          apiFetch<DeviceSummary>(baseUrl, `/api/v1/devices/${deviceId}`, token),
          apiFetch<{ samples: TelemetrySample[] }>(baseUrl, `/api/v1/devices/${deviceId}/telemetry?limit=1`, token),
          apiFetch<{ events: EventItem[] }>(baseUrl, `/api/v1/devices/${deviceId}/events?limit=8`, token)
        ]);
        setSelected(detail);
        setTelemetry(telemetryBody.samples[0] ?? null);
        setEvents(eventsBody.events);
        setError(null);
      } catch (caught) {
        setError(caught instanceof Error ? caught.message : "Gagal memuat perangkat");
      }
    },
    [baseUrl, token]
  );

  useEffect(() => {
    if (!token) return;
    void loadDevices();
    const timer = setInterval(() => {
      void loadDevices();
      if (screen.name === "device") {
        void loadSelected(screen.deviceId);
      }
    }, 5000);
    return () => clearInterval(timer);
  }, [loadDevices, loadSelected, screen, token]);

  const login = async (): Promise<void> => {
    setBusy(true);
    setError(null);
    setNotice(null);
    try {
      const response = await apiFetch<{ access_token: string }>(baseUrl, "/api/v1/auth/login", null, {
        method: "POST",
        body: { email, password }
      });
      await SecureStore.setItemAsync(TOKEN_KEY, response.access_token);
      await SecureStore.setItemAsync(API_KEY, baseUrl);
      setToken(response.access_token);
      setScreen({ name: "devices" });
      setNotice("Login berhasil. Token disimpan di SecureStore perangkat.");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Login gagal");
    } finally {
      setBusy(false);
    }
  };

  const logout = async (): Promise<void> => {
    await SecureStore.deleteItemAsync(TOKEN_KEY).catch(() => undefined);
    setToken(null);
    setSelected(null);
    setDevices([]);
    setCommand(null);
    setScreen({ name: "devices" });
  };

  const sendCommand = async (requested: "ON" | "OFF"): Promise<void> => {
    if (!token || !selected) return;
    if (requested === "ON" && (selected.state.lockout || selected.availability === "OFFLINE" || !selected.state.meter_valid)) {
      setError("ON diblokir: lockout/offline/sensor tidak valid.");
      return;
    }
    setBusy(true);
    setError(null);
    setCommand(null);
    try {
      const created = await apiFetch<CommandResult>(baseUrl, `/api/v1/devices/${selected.device_id}/commands`, token, {
        method: "POST",
        body: { requested_output: requested, idempotency_key: `android-${Date.now()}`, ttl_seconds: 30 }
      });
      setCommand(created);
      let latest = created;
      const deadline = Date.now() + 35_000;
      while (!["APPLIED", "REJECTED", "EXPIRED", "TIMEOUT"].includes(latest.status) && Date.now() < deadline) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        latest = await apiFetch<CommandResult>(
          baseUrl,
          `/api/v1/devices/${selected.device_id}/commands/${created.command_id}`,
          token
        );
        setCommand(latest);
      }
      if (!["APPLIED", "REJECTED", "EXPIRED", "TIMEOUT"].includes(latest.status)) {
        setError("Tidak ada ACK final. Status fisik tidak dapat dipastikan.");
      }
      await loadSelected(selected.device_id);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Perintah gagal");
    } finally {
      setBusy(false);
    }
  };

  if (!token) {
    return (
      <SafeAreaView style={styles.safe}>
        <StatusBar style="auto" />
        <ScrollView contentContainerStyle={styles.loginContainer}>
          <Text style={styles.logo}>Smart Plug</Text>
          <Text style={styles.title}>Masuk ke aplikasi</Text>
          <Text style={styles.muted}>
            Aplikasi ini memakai kontrak API yang sama dengan web. Token disimpan di SecureStore; jangan gunakan
            kredensial demo di perangkat produksi.
          </Text>
          <Text style={styles.label}>API base URL</Text>
          <TextInput style={styles.input} value={baseUrl} onChangeText={setBaseUrl} autoCapitalize="none" />
          <Text style={styles.hint}>Emulator Android: http://10.0.2.2:4000. Perangkat fisik: IP LAN komputer.</Text>
          <Text style={styles.label}>Email</Text>
          <TextInput style={styles.input} value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address" />
          <Text style={styles.label}>Password</Text>
          <TextInput style={styles.input} value={password} onChangeText={setPassword} secureTextEntry />
          {error ? <Text style={styles.error}>{error}</Text> : null}
          {notice ? <Text style={styles.success}>{notice}</Text> : null}
          <Pressable style={[styles.button, styles.primary]} onPress={() => void login()} disabled={busy}>
            <Text style={styles.buttonText}>{busy ? "Memeriksa…" : "Masuk"}</Text>
          </Pressable>
          <Text style={styles.hint}>Demo: demo@example.com / demo1234 (hanya seed lokal).</Text>
        </ScrollView>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safe}>
      <StatusBar style="auto" />
      <View style={styles.header}>
        <Pressable onPress={() => setScreen({ name: "devices" })}>
          <Text style={styles.headerTitle}>Smart Plug</Text>
        </Pressable>
        <View style={styles.headerActions}>
          <Pressable onPress={() => setScreen({ name: "settings" })}>
            <Text style={styles.headerLink}>Pengaturan</Text>
          </Pressable>
          <Pressable onPress={() => void logout()}>
            <Text style={styles.headerLink}>Keluar</Text>
          </Pressable>
        </View>
      </View>

      <ScrollView contentContainerStyle={styles.container}>
        {error ? <Text style={styles.error}>{error}</Text> : null}
        {notice ? <Text style={styles.success}>{notice}</Text> : null}

        {screen.name === "devices" ? (
          <View>
            <Text style={styles.title}>Perangkat</Text>
            <Text style={styles.muted}>
              Status koneksi bukan bukti status fisik. Data demo sintetik selalu diberi label. Waktu tidak valid
              menonaktifkan schedule; kontrol manual tetap boleh.
            </Text>
            <Pressable style={[styles.button, styles.secondary]} onPress={() => void loadDevices()}>
              <Text style={styles.buttonTextDark}>Muat ulang</Text>
            </Pressable>
            {devices.map((device) => (
              <Pressable
                key={device.device_id}
                style={styles.card}
                onPress={() => {
                  setScreen({ name: "device", deviceId: device.device_id });
                  void loadSelected(device.device_id);
                }}
              >
                <View style={styles.rowBetween}>
                  <Text style={styles.cardTitle}>{device.name}</Text>
                  <Text style={[styles.badge, { color: STATUS_COLORS[device.availability] ?? "#5b677a" }]}>
                    {device.availability}
                  </Text>
                </View>
                <Text style={styles.muted}>{device.room ?? "Tanpa ruangan"}</Text>
                <Text style={styles.mono}>{device.device_id}</Text>
                <View style={styles.rowBetween}>
                  <Text style={styles.cardValue}>{device.state.commanded_output}</Text>
                  <Text style={styles.muted}>{formatTime(device.last_seen_at)}</Text>
                </View>
                {device.data_source === "SYNTHETIC_DEMO" ? (
                  <Text style={styles.demoChip}>Data demo sintetik</Text>
                ) : null}
                {device.state.lockout ? <Text style={styles.error}>LOCKOUT / FAULT</Text> : null}
              </Pressable>
            ))}
            {devices.length === 0 ? <Text style={styles.muted}>Belum ada perangkat.</Text> : null}
          </View>
        ) : null}

        {screen.name === "device" && selected ? (
          <View>
            <Text style={styles.title}>{selected.name}</Text>
            <Text style={styles.muted}>{selected.room ?? "Tanpa ruangan"} · {selected.device_id}</Text>
            {selected.data_source === "SYNTHETIC_DEMO" ? (
              <Text style={styles.demoChip}>Data demo sintetik — bukan pengukuran nyata</Text>
            ) : null}
            <View style={styles.rowBetween}>
              <Text style={[styles.badge, { color: STATUS_COLORS[selected.availability] ?? "#5b677a" }]}>
                {selected.availability}
              </Text>
              <Text style={[styles.badge, { color: STATUS_COLORS[selected.state.commanded_output] ?? "#5b677a" }]}>
                {selected.state.commanded_output} (commanded)
              </Text>
            </View>
            {!(selected.state.time_valid ?? selected.state.clock_valid) ? (
              <Text style={styles.error}>
                Waktu belum valid — schedule dinonaktifkan. Kontrol manual tetap boleh.
              </Text>
            ) : (
              <Text style={styles.muted}>
                Waktu valid · sumber {selected.state.time_source ?? "sntp"} · sync{" "}
                {formatTime(selected.state.last_sync ?? null)}
              </Text>
            )}
            <Text style={styles.muted}>
              Feedback fisik: {selected.state.observed_output ?? "tidak tersedia"}
            </Text>
            {selected.state.lockout ? (
              <Text style={styles.error}>Lockout aktif{selected.state.fault_code ? `: ${selected.state.fault_code}` : ""}</Text>
            ) : null}
            <View style={styles.buttonRow}>
              <Pressable
                style={[styles.button, styles.primary, (busy || selected.state.commanded_output === "ON") && styles.disabled]}
                disabled={busy || selected.state.commanded_output === "ON"}
                onPress={() => void sendCommand("ON")}
              >
                <Text style={styles.buttonText}>Nyalakan</Text>
              </Pressable>
              <Pressable
                style={[styles.button, styles.secondary, (busy || selected.state.commanded_output === "OFF") && styles.disabled]}
                disabled={busy || selected.state.commanded_output === "OFF"}
                onPress={() => void sendCommand("OFF")}
              >
                <Text style={styles.buttonTextDark}>Matikan</Text>
              </Pressable>
            </View>
            {command ? <Text style={styles.statusLine}>{command.status} — {command.message}</Text> : null}

            <Text style={styles.sectionTitle}>Pembacaan listrik</Text>
            {telemetry ? (
              <View style={styles.grid}>
                <Reading label="Tegangan" value={`${formatNumber(telemetry.voltage_v)} V`} />
                <Reading label="Arus" value={`${formatNumber(telemetry.current_a, 3)} A`} />
                <Reading label="Daya" value={`${formatNumber(telemetry.active_power_w)} W`} />
                <Reading label="PF" value={formatNumber(telemetry.power_factor, 2)} />
                <Reading label="Frekuensi" value={telemetry.frequency_hz === null ? "—" : `${formatNumber(telemetry.frequency_hz)} Hz`} />
                <Reading label="Energi" value={telemetry.energy_kwh_total === null ? "—" : `${formatNumber(telemetry.energy_kwh_total, 3)} kWh`} />
              </View>
            ) : (
              <Text style={styles.muted}>Belum ada telemetry. Nilai tidak ditampilkan sebagai nol.</Text>
            )}
            <Text style={styles.hint}>Sampel: {telemetry ? formatTime(telemetry.sampled_at) : "—"}. Estimasi biaya bukan tagihan PLN.</Text>

            <Text style={styles.sectionTitle}>Event terbaru</Text>
            {events.length === 0 ? <Text style={styles.muted}>Belum ada event.</Text> : null}
            {events.map((event) => (
              <View key={event.event_id} style={styles.eventRow}>
                <Text style={[styles.badge, { color: event.severity === "CRITICAL" ? "#b42318" : event.severity === "WARNING" ? "#9a5b00" : "#175cd3" }]}>
                  {event.severity}
                </Text>
                <Text style={styles.eventText}>{event.summary}</Text>
                <Text style={styles.hint}>{formatTime(event.occurred_at)}</Text>
              </View>
            ))}
          </View>
        ) : null}

        {screen.name === "settings" ? (
          <View>
            <Text style={styles.title}>Pengaturan</Text>
            <Text style={styles.label}>API base URL</Text>
            <TextInput style={styles.input} value={baseUrl} onChangeText={setBaseUrl} autoCapitalize="none" />
            <Text style={styles.hint}>Ubah ke IP LAN komputer saat memakai perangkat fisik.</Text>
            <Pressable
              style={[styles.button, styles.primary]}
              onPress={() => {
                void SecureStore.setItemAsync(API_KEY, baseUrl).then(() => setNotice("API base URL disimpan."));
              }}
            >
              <Text style={styles.buttonText}>Simpan URL</Text>
            </Pressable>
            <Text style={styles.sectionTitle}>Notifikasi</Text>
            <Text style={styles.muted}>
              Notifikasi push Android belum diaktifkan; memerlukan FCM/Expo credentials. Tombol test memakai endpoint
              backend.
            </Text>
            <Pressable
              style={[styles.button, styles.secondary]}
              onPress={() => {
                if (!selected) {
                  setNotice("Pilih perangkat terlebih dahulu untuk test notifikasi.");
                  return;
                }
                void apiFetch(baseUrl, `/api/v1/devices/${selected.device_id}/notifications/test`, token, { method: "POST" })
                  .then(() => setNotice("Notifikasi test dikirim ke provider backend."))
                  .catch((caught: unknown) => setError(caught instanceof Error ? caught.message : "Test gagal"));
              }}
            >
              <Text style={styles.buttonTextDark}>Test notifikasi perangkat terpilih</Text>
            </Pressable>
            <Text style={styles.sectionTitle}>Keamanan</Text>
            <Text style={styles.muted}>
              Token disimpan di SecureStore. Aplikasi tidak menampilkan status fisik OFF tanpa feedback. Jangan memakai
              kredensial demo di produksi. Revoke-all-session belum tersedia.
            </Text>
            <Pressable style={[styles.button, styles.danger]} onPress={() => void logout()}>
              <Text style={styles.buttonText}>Keluar</Text>
            </Pressable>
          </View>
        ) : null}
      </ScrollView>
    </SafeAreaView>
  );
}

function Reading({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.reading}>
      <Text style={styles.readingLabel}>{label}</Text>
      <Text style={styles.readingValue}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#f3f6fb" },
  loginContainer: { padding: 24, paddingTop: 60 },
  container: { padding: 18, paddingBottom: 60 },
  header: {
    paddingHorizontal: 18,
    paddingVertical: 14,
    backgroundColor: "#ffffff",
    borderBottomWidth: 1,
    borderBottomColor: "#d7dfeb",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between"
  },
  headerTitle: { fontSize: 20, fontWeight: "800", color: "#14213d" },
  headerActions: { flexDirection: "row", gap: 16 },
  headerLink: { color: "#0f6b5c", fontWeight: "700" },
  logo: { fontSize: 28, fontWeight: "900", color: "#0f6b5c", marginBottom: 12 },
  title: { fontSize: 26, fontWeight: "800", color: "#14213d", marginBottom: 6 },
  sectionTitle: { fontSize: 18, fontWeight: "800", color: "#14213d", marginTop: 22, marginBottom: 8 },
  muted: { color: "#5b677a", fontSize: 14, lineHeight: 20 },
  hint: { color: "#5b677a", fontSize: 12, marginTop: 4 },
  label: { fontWeight: "700", color: "#14213d", marginTop: 14, marginBottom: 6 },
  input: {
    backgroundColor: "#ffffff",
    borderWidth: 1,
    borderColor: "#d7dfeb",
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 15,
    color: "#14213d"
  },
  button: { borderRadius: 10, paddingVertical: 12, paddingHorizontal: 16, alignItems: "center", marginTop: 14 },
  primary: { backgroundColor: "#0f6b5c" },
  secondary: { backgroundColor: "#eef2f8", borderWidth: 1, borderColor: "#d7dfeb" },
  danger: { backgroundColor: "#b42318" },
  disabled: { opacity: 0.45 },
  buttonText: { color: "#ffffff", fontWeight: "800", fontSize: 15 },
  buttonTextDark: { color: "#14213d", fontWeight: "800", fontSize: 15 },
  buttonRow: { flexDirection: "row", gap: 10 },
  error: { color: "#b42318", fontWeight: "700", marginTop: 10 },
  success: { color: "#067647", fontWeight: "700", marginTop: 10 },
  card: {
    backgroundColor: "#ffffff",
    borderWidth: 1,
    borderColor: "#d7dfeb",
    borderRadius: 14,
    padding: 14,
    marginTop: 12
  },
  cardTitle: { fontSize: 17, fontWeight: "800", color: "#14213d" },
  cardValue: { fontSize: 20, fontWeight: "900", color: "#14213d", marginTop: 4 },
  rowBetween: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginTop: 6 },
  badge: { fontSize: 12, fontWeight: "800", textTransform: "uppercase" },
  mono: { fontFamily: "monospace", color: "#5b677a", fontSize: 12, marginTop: 2 },
  demoChip: { color: "#9a5b00", fontWeight: "800", fontSize: 12, marginTop: 8 },
  statusLine: { color: "#14213d", fontWeight: "700", marginTop: 10 },
  grid: { flexDirection: "row", flexWrap: "wrap", gap: 10 },
  reading: { width: "47%", backgroundColor: "#ffffff", borderWidth: 1, borderColor: "#d7dfeb", borderRadius: 12, padding: 12, marginTop: 8 },
  readingLabel: { color: "#5b677a", fontSize: 11, textTransform: "uppercase", fontWeight: "700" },
  readingValue: { color: "#14213d", fontSize: 19, fontWeight: "800", marginTop: 2 },
  eventRow: { backgroundColor: "#ffffff", borderWidth: 1, borderColor: "#d7dfeb", borderRadius: 10, padding: 10, marginTop: 8 },
  eventText: { color: "#14213d", marginTop: 4 }
});
