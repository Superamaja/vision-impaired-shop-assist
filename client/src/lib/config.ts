/**
 * API Configuration for the Vision-Impaired Shopping Assistant Client
 *
 * This module provides dynamic API base URL configuration that adapts to the
 * current hostname. This allows the client to work in different environments
 * (localhost, LAN, hotspot) without requiring manual configuration changes.
 *
 * The API server runs on port 5001 by default and provides endpoints for:
 * - Configuration management (/api/settings)
 * - Barcode database operations (/api/barcodes)
 */

/**
 * Dynamic API base URL that adapts to the current hostname
 *
 * Constructs the API URL using the current window location hostname,
 * allowing the client to connect to the backend server regardless of
 * the network configuration (localhost, LAN IP, etc.)
 */
export const API_BASE_URL = `http://${window.location.hostname}:5001`;
