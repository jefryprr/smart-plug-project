import type { EventItem } from "@smartplug/api-contract";
import { formatDateTime } from "@/lib/format";
import { EmptyState } from "./Feedback";
import { StatusBadge, type StatusTone } from "./StatusBadge";

function severityTone(severity: EventItem["severity"]): StatusTone {
  if (severity === "CRITICAL") return "danger";
  if (severity === "WARNING") return "warn";
  return "info";
}

export function EventList({ events, limit = 8, title = "Event terbaru" }: { events: EventItem[]; limit?: number; title?: string }) {
  return (
    <section className="panel" aria-labelledby="events-title">
      <div className="panel-head">
        <div>
          <h2 id="events-title">{title}</h2>
          <p className="muted">Audit perintah, fault, dan perubahan status. Waktu ditampilkan dalam Asia/Jakarta.</p>
        </div>
      </div>
      {events.length === 0 ? (
        <EmptyState title="Belum ada event" />
      ) : (
        <ol className="event-list">
          {events.slice(0, limit).map((event) => (
            <li key={event.event_id}>
              <div className="event-head">
                <StatusBadge label={event.severity} tone={severityTone(event.severity)} />
                <strong>{event.summary}</strong>
              </div>
              <div className="event-meta muted small">
                <span>{event.type}</span>
                <span>{formatDateTime(event.occurred_at)}</span>
                <span>Sumber: {event.source}</span>
                {event.actor_id ? <span>Aktor: {event.actor_id}</span> : null}
              </div>
              {Object.keys(event.payload).length > 0 ? (
                <details>
                  <summary>Detail payload</summary>
                  <pre>{JSON.stringify(event.payload, null, 2)}</pre>
                </details>
              ) : null}
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
