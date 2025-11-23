import random
from typing import List, Dict, Any
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich import box
from config import CONFIG, THEMES

def get_glyph(value: float) -> str:
    """
    Returns the appropriate glyph for a given value (0-100).
    """
    theme_name = CONFIG["theme"]
    theme = THEMES.get(theme_name, THEMES["standard"])
    
    if value < 25:
        return theme["low"]
    elif value < 50:
        return theme["med"]
    elif value < 75:
        return theme["high"]
    else:
        return theme["critical"]

def get_color(value: float) -> str:
    """
    Returns a color string based on intensity.
    """
    if value < 25:
        return "green"
    elif value < 50:
        return "cyan"
    elif value < 75:
        return "yellow"
    else:
        return "red"

def apply_glitch_effect(text_obj: Text, intensity: float) -> Text:
    """
    Randomly modifies the text object based on intensity (0.0 - 1.0).
    Higher intensity means more glitches.
    """
    if not CONFIG["glitch_enabled"] or intensity < 0.1:
        return text_obj
        
    glitch_chars = ["Z", "X", "¥", "§", "¶", "¿", "░", "▒", "▓"]
    
    # Calculate probability of glitch based on intensity
    # If intensity is high (e.g. 0.9), probability is higher
    prob = intensity * 0.3  # Cap max glitch probability at 30% per char
    
    new_text = Text()
    
    for span in text_obj:
        content = span.text
        style = span.style
        
        glitched_content = ""
        for char in content:
            if random.random() < prob:
                # Glitch type 1: Replace character
                glitched_content += random.choice(glitch_chars)
            else:
                glitched_content += char
        
        # Glitch type 2: Style corruption (invert or bold)
        if random.random() < (prob * 0.5):
            style = "reverse bold " + str(style)
            
        new_text.append(glitched_content, style=style)
        
    return new_text

def generate_cpu_visual(cpu_data: List[float]) -> Panel:
    """
    Generates a grid visualization of CPU cores.
    """
    # Calculate average load for glitch intensity
    avg_load = sum(cpu_data) / len(cpu_data) if cpu_data else 0
    glitch_intensity = avg_load / 100.0 if avg_load > CONFIG["glitch_threshold"] else 0.0
    
    grid_content = Text()
    
    # Simple grid layout: try to make it square-ish
    # For now, just a linear flow with wrapping handled by the console or manual newlines
    
    for i, core_usage in enumerate(cpu_data):
        glyph = get_glyph(core_usage)
        color = get_color(core_usage)
        
        # Add some padding/spacing
        grid_content.append(f" {glyph} ", style=color)
        
        # Break line every 4 cores (arbitrary, adaptable)
        if (i + 1) % 4 == 0:
            grid_content.append("\n")
            
    # Apply glitch effect
    final_text = apply_glitch_effect(grid_content, glitch_intensity)
    
    return Panel(final_text, title=f"CPU [ {avg_load:.1f}% ]", border_style="green")

def generate_memory_visual(mem_pressure: float) -> Panel:
    """
    Generates a fluid container visualization for memory.
    mem_pressure is 0.0 to 1.0
    """
    # Visualizing as a vertical bar filling up
    # We'll create a few lines representing levels
    
    height = 10
    fill_level = int(mem_pressure * height)
    
    visual_lines = []
    
    theme = THEMES.get(CONFIG["theme"], THEMES["standard"])
    fill_char = theme["critical"] if mem_pressure > 0.8 else theme["med"]
    empty_char = theme["low"]
    
    for i in range(height):
        # Invert index because we fill from bottom
        current_level = height - 1 - i
        
        if current_level < fill_level:
            # Filled
            line_str = fill_char * 20 # Width of the bar
            color = get_color(mem_pressure * 100)
        else:
            # Empty
            line_str = empty_char * 20
            color = "dim white"
            
        visual_lines.append(Text(line_str, style=color))
    
    # Combine lines
    final_content = Text("\n").join(visual_lines)
    
    # Apply minor glitch if memory is very high
    glitch_intensity = (mem_pressure - 0.8) * 2 if mem_pressure > 0.8 else 0.0
    final_content = apply_glitch_effect(final_content, glitch_intensity)
    
    return Panel(final_content, title=f"MEM [ {mem_pressure*100:.1f}% ]", border_style="blue")

def generate_disk_visual(disk_io: Dict[str, int]) -> Panel:
    """
    Generates a visual for disk activity.
    """
    # Just showing read/write counters for now, maybe rates later if we tracked history
    read_mb = disk_io['read_bytes'] / (1024 * 1024)
    write_mb = disk_io['write_bytes'] / (1024 * 1024)
    
    content = Text()
    content.append(f"R: {read_mb:.1f} MB\n", style="cyan")
    content.append(f"W: {write_mb:.1f} MB", style="magenta")
    
    return Panel(content, title="DISK I/O", border_style="yellow")

def generate_process_table(processes: List[Dict[str, Any]]) -> Panel:
    """
    Generates a table of top processes.
    """
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold magenta")
    table.add_column("PID", style="cyan", width=6)
    table.add_column("NAME", style="white")
    table.add_column("CPU%", style="green", justify="right")
    table.add_column("MEM%", style="yellow", justify="right")
    
    for proc in processes:
        table.add_row(
            str(proc['pid']),
            proc['name'][:15], # Truncate long names
            f"{proc['cpu_percent']:.1f}",
            f"{proc['memory_percent']:.1f}"
        )
        
    return Panel(table, title="TOP PROCS", border_style="magenta")
