/**
 * Application configuration interface matching the backend Config class
 *
 * @interface Config
 * @property {boolean} DEBUG - Enable/disable debug mode for visual output
 * @property {number} TTS_SPEED - Speech rate for text-to-speech engine (100-500)
 * @property {number} THRESHOLDING - Image processing threshold value (0-255)
 * @property {string} TTS_OCR_TEMPLATE - Template string for OCR text announcements
 * @property {string} TTS_BARCODE_FOUND_TEMPLATE - Template for product announcements
 * @property {string} TTS_BARCODE_NOT_FOUND_TEMPLATE - Message for unknown products
 */
interface Config {
  DEBUG: boolean;
  TTS_SPEED: number;
  THRESHOLDING: number;
  TTS_OCR_TEMPLATE: string;
  TTS_BARCODE_FOUND_TEMPLATE: string;
  TTS_BARCODE_NOT_FOUND_TEMPLATE: string;
}

/**
 * Reactive configuration state object using Svelte 5 runes
 *
 * This object maintains the current application configuration and automatically
 * updates the UI when values change. It's synchronized with the backend server.
 */
export const config: Config = $state({
  DEBUG: false,
  TTS_SPEED: 0,
  THRESHOLDING: 0,
  TTS_OCR_TEMPLATE: "",
  TTS_BARCODE_FOUND_TEMPLATE: "",
  TTS_BARCODE_NOT_FOUND_TEMPLATE: "",
});

import { API_BASE_URL } from "../config";

/**
 * Fetch current configuration settings from the backend API
 *
 * Retrieves all configuration settings from the server and updates
 * the local config state. Only updates properties that exist in the
 * local config interface to prevent unwanted data injection.
 */
export const fetchConfig = async () => {
  const response = await fetch(`${API_BASE_URL}/api/settings`);
  const data = await response.json();

  // Safely update only known configuration properties
  for (const key in data) {
    if (key in config) {
      (config as any)[key] = data[key];
    }
  }
};

/**
 * Send current configuration settings to the backend API
 *
 * Pushes all current configuration values to the server for persistence.
 * The server will validate and apply the settings, updating the backend
 * configuration state.
 *
 * @throws {Error} If the API request fails or returns an error status
 */
export const updateConfig = async () => {
  const response = await fetch(`${API_BASE_URL}/api/settings`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(config),
  });

  if (!response.ok) {
    throw new Error(`Failed to update configuration: ${response.statusText}`);
  }
};
