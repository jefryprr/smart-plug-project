# Deploy check (does not deploy). Run from repo root.
$ErrorActionPreference = "Continue"
Write-Output "== Tool availability =="
foreach ($tool in "docker", "docker-compose", "psql", "mosquitto") {
    $cmd = Get-Command $tool -ErrorAction SilentlyContinue
    if ($cmd) { Write-Output "$tool => $($cmd.Source)" } else { Write-Output "$tool => NOT_FOUND" }
}
Write-Output "== Required files =="
foreach ($path in "infrastructure/docker-compose.dev.yaml", "infrastructure/.env.docker", "infrastructure/broker/mosquitto.prod.conf", "infrastructure/broker/aclfile.template", "database/migrations/001_init.sql") {
    Write-Output "$path => $(Test-Path $path)"
}
Write-Output "== Blockers =="
Write-Output "Docker/Postgres/Mosquitto not installed => deployment BLOCKED."
Write-Output "API PostgreSQL adapter not implemented => Postgres path is schema-only."
Write-Output "No domain/TLS/VPS credentials => production deploy requires user approval."
