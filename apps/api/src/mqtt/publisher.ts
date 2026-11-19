import type { CommandMessage, TimeMessage } from "@smartplug/mqtt-contract";

export interface CommandPublisher {
  publishCommand(message: CommandMessage): Promise<void>;
  publishTime(message: TimeMessage): Promise<void>;
  isConnected(): boolean;
}

export class NullCommandPublisher implements CommandPublisher {
  async publishCommand(): Promise<void> {
    throw new Error("MQTT_PUBLISHER_NOT_CONFIGURED");
  }

  async publishTime(): Promise<void> {
    throw new Error("MQTT_PUBLISHER_NOT_CONFIGURED");
  }

  isConnected(): boolean {
    return false;
  }
}

/**
 * Allows the HTTP app to be built before the MQTT bridge is connected.
 * Routes hold this stable object; the real bridge is attached afterwards.
 */
export class DeferredPublisher implements CommandPublisher {
  private inner: CommandPublisher | null = null;

  setInner(publisher: CommandPublisher): void {
    this.inner = publisher;
  }

  async publishCommand(message: Parameters<CommandPublisher["publishCommand"]>[0]): Promise<void> {
    if (!this.inner) {
      throw new Error("MQTT_PUBLISHER_NOT_READY");
    }
    await this.inner.publishCommand(message);
  }

  async publishTime(message: Parameters<CommandPublisher["publishTime"]>[0]): Promise<void> {
    if (!this.inner) {
      throw new Error("MQTT_PUBLISHER_NOT_READY");
    }
    await this.inner.publishTime(message);
  }

  isConnected(): boolean {
    return this.inner?.isConnected() ?? false;
  }
}
