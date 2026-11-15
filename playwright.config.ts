import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 45_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [
    ["list"],
    ["html", { outputFolder: "reports/playwright-report", open: "never" }]
  ],
  use: {
    baseURL: "http://127.0.0.1:3000",
    viewport: { width: 1440, height: 960 },
    trace: "retain-on-failure",
    screenshot: "only-on-failure"
  },
  webServer: [
    {
      command: "node scripts/e2e_api.mjs",
      url: "http://127.0.0.1:4000/health/live",
      timeout: 60_000,
      reuseExistingServer: false
    },
    {
      command: "npm run start -w @smartplug/web",
      url: "http://127.0.0.1:3000/login",
      timeout: 120_000,
      reuseExistingServer: false
    }
  ],
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] }
    }
  ]
});
