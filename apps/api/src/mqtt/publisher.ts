import type { CommandMessage } from "@smartplug/mqtt-contract";

export interface CommandPublisher {
  publishCommand(message: CommandMessage): Promise<void>;
  isConnected(): boolean;
}

export class NullCommandPublisher implements CommandPublisher {
  async publishCommand(): Promise<void> {
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

  isConnected(): boolean {
    return this.inner?.isConnected() ?? false;
  }
}
