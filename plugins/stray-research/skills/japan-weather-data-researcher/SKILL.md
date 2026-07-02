---
name: "japan-weather-data-researcher"
description: "Use when the user wants current, recent historical, station-based, location-based, or prefecture forecast weather data for Japan using jma-data-mcp. Trigger on JMA, 気象庁, AMeDAS, アメダス, 現在の天気, 直近の気象, 天気予報, station code, or weather time series. Do not use for climate normals, long-term climate research, disaster policy background, non-Japan weather, or legal/safety instructions."
---

# Japan Weather Data Researcher

Use `jma-data-mcp` to retrieve Japan Meteorological Agency observation, station, recent-history, time-series, and forecast data, with exact time windows and freshness labels.

## Do Not Use For

- Long-term climate normals or historical climate research beyond the MCP's recent-history window.
- Disaster policy, evacuation guidance, or emergency instructions.
- Non-Japan weather data.
- Official statistics tables that belong in `japan-gov-estat-data-analyst`.
- Generic current-events research where live JMA observations are not needed.

## Workflow

1. Scope the weather question.
   - Resolve location, station code, coordinates, prefecture, weather variable, time window, and whether the user needs current values, forecast, nearby stations, or a time series.
   - Convert relative dates to exact dates and times with timezone labels.
2. Confirm `jma-data-mcp` availability.
   - Use the configured MCP tools when available.
   - If unavailable, stop with setup guidance: configure `jma-data-mcp`.
3. Select the right tool family by question type.

   | Question type | Tool family |
   |---|---|
   | Which station covers this place? | Station lookup/search |
   | What is the weather right now? | Current weather (latest AMeDAS observations) |
   | What is the forecast? | Forecast by prefecture |
   | What happened over recent hours or days? | Historical or time-series tools, only within the MCP's recent availability window |
4. Validate freshness and coverage.
   - Record station, observation timestamp, forecast issue time when available, units, and missing fields.
   - If nearest-station lookup is used, state distance or selection basis when available.
5. Report the result.
   - Keep observations separate from forecasts.
   - Explain unavailable variables or stale/missing data without filling gaps from memory.

## Output Expectations

| Metric | Value | Unit | Station/area | Timestamp | Caveat |
|---|---:|---|---|---|---|

Also include `使用したMCPツール`, `時刻の扱い`, `観測/予報の区別`, and `不足データ`.

## Guardrails

- Do not present weather data as safety-critical emergency guidance.
- Do not silently substitute a distant station for a requested location.
- Do not claim long historical coverage; this MCP is for current, short recent-history, time-series, and forecast workflows.
- Do not mix observation times and forecast target times without labeling them.
