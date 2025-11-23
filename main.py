import time
import sys
from rich.live import Live
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import metrics
import render

def make_layout() -> Layout:
    """
    Define the layout grid.
    """
    layout = Layout(name="root")
    
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
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
        Layout(name="disk", ratio=1)
    )
    
    return layout

def update_layout(layout: Layout) -> None:
    """
    Fetch metrics and update the layout renderables.
    """
    # Get Data
    cpu_data = metrics.get_cpu_matrix()
    mem_pressure = metrics.get_memory_pressure()
    net_stats = metrics.get_network_stats()
    disk_io = metrics.get_disk_io()
    top_procs = metrics.get_top_processes()
    
    # Generate Visuals
    cpu_panel = render.generate_cpu_visual(cpu_data)
    mem_panel = render.generate_memory_visual(mem_pressure)
    disk_panel = render.generate_disk_visual(disk_io)
    proc_panel = render.generate_process_table(top_procs)
    
    # Header
    header_content = Text("GLITCH_TOP // SYSTEM_MONITOR_V1.1", justify="center", style="bold magenta")
    layout["header"].update(Panel(header_content, style="magenta"))
    
    # Body
    layout["cpu"].update(cpu_panel)
    layout["memory"].update(mem_panel)
    layout["disk"].update(disk_panel)
    layout["processes"].update(proc_panel)
    
    # Footer (Network Stats)
    sent_mb = net_stats['bytes_sent'] / (1024 * 1024)
    recv_mb = net_stats['bytes_recv'] / (1024 * 1024)
    footer_text = f"NET_IO :: UP: {sent_mb:.2f} MB | DOWN: {recv_mb:.2f} MB"
    layout["footer"].update(Panel(Text(footer_text, justify="right"), style="cyan"))

def main():
    console = Console()
    layout = make_layout()
    
    try:
        with Live(layout, refresh_per_second=4, screen=True) as live:
            while True:
                update_layout(layout)
                time.sleep(0.25)
    except KeyboardInterrupt:
        console.print("[bold red]SYSTEM HALTED BY USER[/bold red]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]CRITICAL ERROR: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
