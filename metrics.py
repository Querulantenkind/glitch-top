import psutil
from typing import List, Tuple, Dict, Any

def get_cpu_matrix() -> List[float]:
    """
    Returns a list of CPU usage percentages for each core.
    """
    # percpu=True gives usage for each core
    return psutil.cpu_percent(interval=0, percpu=True)

def get_memory_pressure() -> float:
    """
    Returns memory usage as a float between 0.0 and 1.0.
    """
    mem = psutil.virtual_memory()
    return mem.percent / 100.0

def get_network_stats() -> Dict[str, int]:
    """
    Returns basic network statistics: bytes_sent, bytes_recv.
    """
    net = psutil.net_io_counters()
    return {
        "bytes_sent": net.bytes_sent,
        "bytes_recv": net.bytes_recv
    }

def get_disk_io() -> Dict[str, int]:
    """
    Returns basic disk statistics: read_bytes, write_bytes.
    """
    disk = psutil.disk_io_counters()
    if disk:
        return {
            "read_bytes": disk.read_bytes,
            "write_bytes": disk.write_bytes
        }
    return {"read_bytes": 0, "write_bytes": 0}

def get_top_processes(n: int = 5) -> List[Dict[str, Any]]:
    """
    Returns the top n processes sorted by CPU usage.
    """
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            p.info['cpu_percent'] = p.info['cpu_percent'] or 0.0 # handle None
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    # Sort by CPU usage descending
    procs.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return procs[:n]
