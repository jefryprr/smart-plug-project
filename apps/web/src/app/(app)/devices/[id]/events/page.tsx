"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import { useEvents } from "@/lib/hooks";
import { EventList } from "@/components/EventList";
import { ErrorPanel, Loading } from "@/components/Feedback";

const FILTERS = ["ALL", "CRITICAL", "WARNING", "INFO"] as const;
type Filter = (typeof FILTERS)[number];

export default function EventsPage() {
  const params = useParams();
  const deviceId = typeof params.id === "string" ? params.id : "";
  const events = useEvents(deviceId, 100);
  const [filter, setFilter] = useState<Filter>("ALL");

  if (events.loading && !events.data) return <Loading />;
  if (events.error && !events.data) return <ErrorPanel message={events.error} onRetry={() => void events.reload()} />;

  const all = events.data?.events ?? [];
  const filtered = filter === "ALL" ? all : all.filter((event) => event.severity === filter);

  return (
    <div className="stack">
      <div className="range-picker" role="group" aria-label="Filter severity">
        {FILTERS.map((value) => (
          <button
            key={value}
            type="button"
            className={filter === value ? "range-button active" : "range-button"}
            aria-pressed={filter === value}
            onClick={() => setFilter(value)}
          >
            {value === "ALL" ? "Semua" : value}
          </button>
        ))}
      </div>
      <EventList events={filtered} limit={100} title={`Event (${filtered.length})`} />
    </div>
  );
}
