import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { login, openDemoDevice, screenshot } from "./helpers";

test.describe("authentication and dashboard", () => {
  test("login page and dashboard render real states", async ({ page }) => {
    await page.goto("/login");
    await expect(page.getByRole("heading", { name: "Masuk ke dashboard" })).toBeVisible();
    await expect(page.getByText("Batas klaim")).toBeVisible();
    await screenshot(page, "01-login");

    await login(page);
    await expect(page.getByText("Smart Plug Demo")).toBeVisible();
    await expect(page.getByText("Data demo sintetik").first()).toBeVisible();
    await screenshot(page, "02-dashboard");

    await openDemoDevice(page);
    await expect(page.getByText("Pembacaan listrik")).toBeVisible();
    await expect(page.getByText("Tidak tersedia", { exact: true }).first()).toBeVisible();
    await screenshot(page, "03-device-overview");
  });

  test("device tabs show analytics, schedules, events, diagnostics, and settings", async ({ page }) => {
    await login(page);
    await openDemoDevice(page);

    await page.getByRole("link", { name: "Analitik" }).click();
    await expect(page.getByRole("heading", { name: /Energi/ })).toBeVisible();
    await screenshot(page, "04-analytics");

    await page.getByRole("link", { name: "Jadwal" }).click();
    await expect(page.getByRole("heading", { name: "Jadwal mingguan" })).toBeVisible();
    await screenshot(page, "05-schedules");

    await page.getByRole("link", { name: "Otomasi" }).click();
    await expect(page.getByRole("heading", { name: "Aturan dan otomasi" })).toBeVisible();
    await screenshot(page, "06-automation");

    await page.getByRole("link", { name: "Event" }).click();
    await expect(page.getByRole("heading", { name: /Event/ })).toBeVisible();
    await screenshot(page, "07-events");

    await page.getByRole("link", { name: "Diagnostik" }).click();
    await expect(page.getByRole("heading", { name: "Kesehatan perangkat" })).toBeVisible();
    await screenshot(page, "08-diagnostics");

    await page.getByRole("link", { name: "Pengaturan" }).click();
    await expect(page.getByRole("heading", { name: "Identitas perangkat" })).toBeVisible();
    await screenshot(page, "09-device-settings");
  });

  test("ON/OFF command reaches the simulator and returns APPLIED", async ({ page }) => {
    await login(page);
    await openDemoDevice(page);
    await expect(page.getByRole("button", { name: "Nyalakan" })).toBeEnabled({ timeout: 15_000 });
    await page.getByRole("button", { name: "Nyalakan" }).click();
    await expect(page.locator(".command-status")).toContainText("APPLIED", { timeout: 20_000 });
    await expect(page.getByText("ON (commanded)").first()).toBeVisible();
    await expect(page.getByText("Tidak tersedia").first()).toBeVisible();
    await screenshot(page, "10-command-applied");

    await page.getByRole("button", { name: "Matikan" }).click();
    await expect(page.locator(".command-status")).toContainText("APPLIED", { timeout: 20_000 });
    await expect(page.getByRole("button", { name: "Nyalakan" })).toBeEnabled({ timeout: 15_000 });
  });

  test("no serious or critical axe violations on login and dashboard", async ({ page }) => {
    await page.goto("/login");
    const loginResults = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
    const loginBlocking = loginResults.violations.filter(
      (violation) => violation.impact === "serious" || violation.impact === "critical"
    );
    expect(loginBlocking, JSON.stringify(loginBlocking, null, 2)).toEqual([]);

    await login(page);
    const dashboardResults = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
    const dashboardBlocking = dashboardResults.violations.filter(
      (violation) => violation.impact === "serious" || violation.impact === "critical"
    );
    expect(dashboardBlocking, JSON.stringify(dashboardBlocking, null, 2)).toEqual([]);
  });
});

test.describe("mobile dashboard", () => {
  test.use({ viewport: { width: 390, height: 844 } });

  test("mobile layout remains usable", async ({ page }) => {
    await login(page);
    await expect(page.getByRole("heading", { name: /Halo,/ })).toBeVisible();
    await screenshot(page, "11-mobile-dashboard");
    await openDemoDevice(page);
    await expect(page.getByRole("heading", { name: "Kontrol daya" })).toBeVisible();
    await screenshot(page, "12-mobile-device");
  });
});
