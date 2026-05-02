# ISS Tracker Setup Guide

Display the real-time position and altitude of the International Space Station.

## Overview

The ISS Tracker plugin fetches the current latitude, longitude, and velocity of the ISS every few minutes using the public wheretheiss.at API. No API key is required.

- API reference: https://wheretheiss.at/w/developer

### Prerequisites

No API key or account required.

## Quick Setup

1. **Enable** — Go to **Integrations** in your FiestaBoard settings and enable **ISS Tracker**.
2. **Configure** — Fill in the plugin settings (see Configuration Reference below).
3. **Template** — Add a page using the `iss_tracker` plugin variables:
   ```
   {{{ iss_tracker.status }}}
   ```
4. **View** — Navigate to your board page to see the live display.

## Template Variables

| Variable | Description | Example |
|---|---|---|
| `iss_tracker.latitude` | Current latitude in decimal degrees | `51.50` |
| `iss_tracker.longitude` | Current longitude in decimal degrees | `-0.13` |
| `iss_tracker.altitude_km` | Altitude above Earth in km | `408.3` |
| `iss_tracker.velocity_kph` | Speed in km/h | `27600` |
| `iss_tracker.visibility` | daylight or eclipsed | `daylight` |

## Configuration Reference

| Setting | Name | Description | Default |
|---|---|---|---|
| `enabled` | Enabled |  | `False` |
| `refresh_seconds` | Refresh Interval (seconds) | How often to fetch ISS position. | `60` |

## Troubleshooting

- **No data shown** — verify the device can reach `api.wheretheiss.at`.
- **Stale position** — lower the refresh interval (minimum 30 s).

