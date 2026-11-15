import { mkdirSync } from "node:fs";
import { expect, type Page } from "@playwright/test";

export const SCREENSHOT_DIR = "docs/ui-ux/screenshots";

export function prepareScreenshots(): void {
  mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

export async function login(page: Page): Promise<void> {
  await page.goto("/login");
  await page.getByLabel("Email").fill("demo@example.com");
  await page.getByLabel("Password").fill("demo1234");
  await page.getByRole("button", { name: "Masuk" }).click();
  await page.waitForURL("**/dashboard");
  await expect(page.getByRole("heading", { name: /Halo,/ })).toBeVisible();
}

export async function openDemoDevice(page: Page): Promise<void> {
  await page.getByRole("link", { name: /Smart Plug Demo/ }).click();
  await page.waitForURL("**/devices/dev-sim-001/overview");
  await expect(page.getByRole("heading", { name: "Kontrol daya" })).toBeVisible();
}

export async function screenshot(page: Page, name: string): Promise<void> {
  prepareScreenshots();
  await page.screenshot({ path: `${SCREENSHOT_DIR}/${name}.png`, fullPage: true });
}
