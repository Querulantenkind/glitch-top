# GlitchTop

> "System monitoring as performance art."

## 1. Project Overview
**GlitchTop** is a system monitor (like `htop` or `btop`) that prioritizes aesthetics over precision. It visualizes system metrics (CPU, RAM, Disk, Net) as evolving, abstract Unicode patterns and "Matrix-like" digital rain, rather than bars and graphs.

## 2. Technical Architecture

### Tech Stack
- **Language:** Python.
- **UI Library:** `Rich` (for advanced terminal formatting) and `Live` display.
- **System Data:** `psutil`.

### Visualization Logic
- **Mapping:** Map 0-100% usage to index in a character array.
  - Low load: `·`
  - Medium load: `+`
  - High load: `#`
  - Critical: `█` (Red)
- **Entropy:** Use `random` tailored by system load to determine "glitch" frequency. High CPU load = more visual corruption/noise in the display.

## 3. Features
- **CPU Grid:** Visualizes per-core usage with glyphs.
- **Memory Fluid:** A "fluid" container filling with usage.
- **Disk I/O:** Monitors read/write bytes.
- **Process List:** Top processes by CPU usage in a glitchy table.
- **Network Stats:** Real-time upload/download tracking.


## 4. Customization
- Users can supply their own "Glyph Sets" (e.g., Runes, Braille, Japanese Katakana) via config.
