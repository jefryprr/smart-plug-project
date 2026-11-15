const ACCESS_KEY = "smartplug.access";
const REFRESH_KEY = "smartplug.refresh";

export interface TokenPair {
  access: string | null;
  refresh: string | null;
}

export function getTokens(): TokenPair {
  if (typeof window === "undefined") {
    return { access: null, refresh: null };
  }
  return {
    access: window.sessionStorage.getItem(ACCESS_KEY),
    refresh: window.sessionStorage.getItem(REFRESH_KEY)
  };
}

export function setTokens(access: string, refresh: string): void {
  if (typeof window === "undefined") return;
  window.sessionStorage.setItem(ACCESS_KEY, access);
  window.sessionStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens(): void {
  if (typeof window === "undefined") return;
  window.sessionStorage.removeItem(ACCESS_KEY);
  window.sessionStorage.removeItem(REFRESH_KEY);
}
