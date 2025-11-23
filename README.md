# GlitchTop

> "System monitoring as performance art."

## 1. Project Overview
**GlitchTop** is a system monitor (like `htop` or `btop`) that prioritizes aesthetics over precision. It visualizes system metrics (CPU, RAM, Net) as evolving, abstract Unicode patterns and "Matrix-like" digital rain, rather than bars and graphs.

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

## 3. Implementation Roadmap (For AI Agent)

### Phase 1: Data Harvesting (`metrics.py`)
- Function `get_cpu_matrix()`: Returns a list of values for each CPU core.
- Function `get_memory_pressure()`: Returns float 0.0-1.0.

### Phase 2: The Renderer (`render.py`)
- **The Grid:** Create a `Table` or `Layout` in Rich.
- **The Algorithms:**
  - *CPU View:* A grid of characters that updates 4x per second.
  - *Memory View:* A "fluid" container where characters fill up from the bottom.
- **The Glitch Effect:** Occasionally inject Zzalgo text or invert colors randomly if CPU > 80%.

### Phase 3: Main Loop
- Use `rich.live.Live` to refresh the screen without flickering.
- Handle `KeyboardInterrupt` for graceful exit.

## 4. Customization
- Users can supply their own "Glyph Sets" (e.g., Runes, Braille, Japanese Katakana) via config.
