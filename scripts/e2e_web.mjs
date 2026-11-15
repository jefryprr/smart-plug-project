import { existsSync } from "node:fs";
import { execSync, spawn } from "node:child_process";

if (!existsSync("apps/web/.next")) {
  console.log("Building Next.js for E2E...");
  execSync("npm run build -w @smartplug/web", { stdio: "inherit" });
}

const isWindows = process.platform === "win32";
const child = isWindows
  ? spawn(process.env.ComSpec || "cmd.exe", ["/c", "npm run start -w @smartplug/web"], {
      stdio: "inherit",
      env: process.env
    })
  : spawn("npm", ["run", "start", "-w", "@smartplug/web"], {
      stdio: "inherit",
      env: process.env
    });

const shutdown = () => child.kill();
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
child.on("exit", (code) => process.exit(code ?? 0));
