import { randomUUID } from "node:crypto";
import type { AppDb } from "../db/index.js";
import type { AppConfig } from "../config.js";
import { rateLimited } from "../errors.js";
import { appendAudit } from "./audit.js";

export interface NotificationResult {
  notification_id: string;
  provider: "mock" | "telegram";
  status: "QUEUED" | "SENT" | "FAILED";
}

export async function sendTestNotification(
  db: AppDb,
  config: AppConfig,
  userId: string,
  deviceId: string,
  now: Date = new Date()
): Promise<NotificationResult> {
  const recent = db.get<{ created_at: string }>(
    `SELECT created_at FROM user_notifications
      WHERE user_id = ? AND device_id = ?
      ORDER BY created_at DESC LIMIT 1`,
    userId,
    deviceId
  );
  if (recent && now.getTime() - new Date(recent.created_at).getTime() < 60_000) {
    throw rateLimited("Notifikasi test dibatasi satu kali per menit per perangkat");
  }

  const notificationId = randomUUID();
  const provider: "mock" | "telegram" = config.telegramBotToken && config.telegramChatId ? "telegram" : "mock";
  db.run(
    `INSERT INTO user_notifications (notification_id, device_id, user_id, provider, status, created_at, sent_at, error)
     VALUES (?, ?, ?, ?, 'QUEUED', ?, NULL, NULL)`,
    notificationId,
    deviceId,
    userId,
    provider,
    now.toISOString()
  );

  if (provider === "mock") {
    db.run(
      `UPDATE user_notifications SET status = 'SENT', sent_at = ? WHERE notification_id = ?`,
      now.toISOString(),
      notificationId
    );
    appendAudit(db, {
      actorId: userId,
      action: "notification.test.mock_sent",
      objectType: "device",
      objectId: deviceId,
      metadata: { notification_id: notificationId, provider },
      now
    });
    return { notification_id: notificationId, provider, status: "SENT" };
  }

  try {
    const response = await fetch(`https://api.telegram.org/bot${config.telegramBotToken}/sendMessage`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        chat_id: config.telegramChatId,
        text: "Smart Plug: notifikasi test. Jika Anda menerima pesan ini, kanal Telegram aktif."
      }),
      signal: AbortSignal.timeout(10_000)
    });
    if (!response.ok) {
      throw new Error(`TELEGRAM_HTTP_${response.status}`);
    }
    db.run(
      `UPDATE user_notifications SET status = 'SENT', sent_at = ? WHERE notification_id = ?`,
      new Date().toISOString(),
      notificationId
    );
    appendAudit(db, {
      actorId: userId,
      action: "notification.test.telegram_sent",
      objectType: "device",
      objectId: deviceId,
      metadata: { notification_id: notificationId, provider },
      now
    });
    return { notification_id: notificationId, provider, status: "SENT" };
  } catch (error) {
    const message = error instanceof Error ? error.message.slice(0, 160) : "TELEGRAM_ERROR";
    db.run(
      `UPDATE user_notifications SET status = 'FAILED', error = ? WHERE notification_id = ?`,
      message,
      notificationId
    );
    appendAudit(db, {
      actorId: userId,
      action: "notification.test.failed",
      objectType: "device",
      objectId: deviceId,
      metadata: { notification_id: notificationId, provider, error: message },
      now
    });
    return { notification_id: notificationId, provider, status: "FAILED" };
  }
}
