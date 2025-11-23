import time
import sys
import collections
from rich.live import Live
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import metrics
import render
from config import CONFIG, THEMES

# State for history and theme cycling
class AppState:
    def __init__(self):
        self.net_history = collections.deque(maxlen=40)
        self.last_net_bytes = 0
        self.last_theme_switch = time.time()
        self.themes = list(THEMES.keys())
        self.current_theme_idx = 0

def make_layout() -> Layout:
    """
    Define the layout grid.
    """
    layout = Layout(name="root")
    
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="entropy_stream", size=6), # New Entropy Stream area
        Layout(name="footer", size=3)
    )
    
    layout["main"].split_row(
        Layout(name="left_col", ratio=2),
        Layout(name="right_col", ratio=1)
    )
    
    layout["left_col"].split(
        Layout(name="cpu", ratio=2),
        Layout(name="processes", ratio=3)
    )
    
    layout["right_col"].split(
        Layout(name="memory", ratio=2),
        Layout(name="disk", ratio=1),
        Layout(name="sensors", ratio=1), # Replaces GPU or adds to it? Let's split this further
        Layout(name="gpu", ratio=1)
    )
    
    return layout

def update_layout(layout: Layout, state: AppState) -> None:
    """
    Fetch metrics and update the layout renderables.
    """
    # Theme Cycling Logic
    if CONFIG["theme_cycle_enabled"]:
        now = time.time()
        if now - state.last_theme_switch > CONFIG["theme_cycle_interval"]:
            state.current_theme_idx = (state.current_theme_idx + 1) % len(state.themes)
            CONFIG["theme"] = state.themes[state.current_theme_idx]
            state.last_theme_switch = now
    
    # Get Data
    cpu_data = metrics.get_cpu_matrix()
    mem_pressure = metrics.get_memory_pressure()
    net_stats = metrics.get_network_stats()
    disk_io = metrics.get_disk_io()
    top_procs = metrics.get_top_processes()
    gpu_stats = metrics.get_gpu_stats()
    temps = metrics.get_temperatures()
    battery = metrics.get_battery_status()
    
    # Calculate System Intensity (0-1)
    # Average of CPU load and Memory Pressure
    avg_cpu = sum(cpu_data) / len(cpu_data) if cpu_data else 0
    intensity = (avg_cpu / 100.0 + mem_pressure) / 2.0
    
    # Update Network History (Sparkline)
    total_net = net_stats['bytes_sent'] + net_stats['bytes_recv']
    if state.last_net_bytes > 0:
        diff = total_net - state.last_net_bytes
        state.net_history.append(diff)
    else:
        state.net_history.append(0)
    state.last_net_bytes = total_net
    
    # Generate Visuals
    cpu_panel = render.generate_cpu_visual(cpu_data)
    mem_panel = render.generate_memory_visual(mem_pressure)
    disk_panel = render.generate_disk_visual(disk_io)
    proc_panel = render.generate_process_table(top_procs)
    gpu_panel = render.generate_gpu_visual(gpu_stats)
    
    # Combine Sensor Visuals
    temp_panel = render.generate_temp_visual(temps)
    # If battery exists, we might want to show it. 
    # For now, let's swap GPU/Sensors if GPU is empty or just alternate?
    # Better: Combine Temp and Battery into one panel or split the Sensor layout
    # Simple approach: render both into one text object
    sensor_content = Text()
    if temps:
        # Extract temp content from the panel function (refactor or just reuse logic?)
        # Reuse logic for cleaner code, let's just use temp_panel for now
        # But wait, we want battery too.
        # Let's create a combined visual manually here or add a new helper in render.
        # Actually, let's use the 'sensors' layout slot for temps, and maybe squeeze battery in footer or header?
        # Or, let's check if battery exists.
        pass

    # Header
    theme_name = CONFIG["theme"].upper()
    header_text = f"GLITCH_TOP // {theme_name}_MODE // V3.0"
    header_content = Text(header_text, justify="center", style="bold magenta")
    layout["header"].update(Panel(header_content, style="magenta"))
    
    # Body
    layout["cpu"].update(cpu_panel)
    layout["memory"].update(mem_panel)
    layout["disk"].update(disk_panel)
    layout["processes"].update(proc_panel)
    layout["gpu"].update(gpu_panel)
    
    # Sensors Slot: Show Temps. If Battery exists, show it instead of Disk maybe?
    # Or just put Temp in Sensors slot.
    layout["sensors"].update(temp_panel)
    
    # Entropy Stream
    # Get width from console? Hard to pass here without refactoring.
    # We'll guess a reasonable width or rely on Panel to clip.
    entropy_panel = render.generate_entropy_stream(width=100, height=4, intensity=intensity)
    layout["entropy_stream"].update(entropy_panel)

    # Footer (Network Stats + Sparkline + Battery Info if present)
    sent_mb = net_stats['bytes_sent'] / (1024 * 1024)
    recv_mb = net_stats['bytes_recv'] / (1024 * 1024)
    
    sparkline = render.generate_net_sparkline(list(state.net_history))
    
    footer_content = Text()
    footer_content.append(f"NET_IO :: UP: {sent_mb:.2f} MB | DOWN: {recv_mb:.2f} MB  ", style="cyan")
    if battery:
        footer_content.append(f"| BATT: {battery['percent']}% {'⚡' if battery['plugged'] else ''} ", style="yellow")
    footer_content.append(sparkline)
    
    layout["footer"].update(Panel(footer_content, style="cyan", title="NETWORK_FLOW"))

def main():
    console = Console()
    layout = make_layout()
    state = AppState()
    
    try:
        with Live(layout, refresh_per_second=4, screen=True) as live:
            while True:
                update_layout(layout, state)
                time.sleep(0.25)
    except KeyboardInterrupt:
        console.print("[bold red]SYSTEM HALTED BY USER[/bold red]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]CRITICAL ERROR: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
