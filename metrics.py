import psutil
import shutil
import subprocess
import xml.etree.ElementTree as ET
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

def get_gpu_stats() -> Dict[str, Any]:
    """
    Attempts to get GPU statistics via nvidia-smi.
    Returns a dict with 'utilization' (0-100) and 'memory_used' (MB), or None if failed.
    """
    nvidia_smi = shutil.which('nvidia-smi')
    if nvidia_smi:
        try:
            # -x: XML output, -q: Query
            cmd = [nvidia_smi, '-q', '-x']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1)
            if result.returncode == 0:
                root = ET.fromstring(result.stdout)
                gpu = root.find('gpu')
                if gpu:
                    util = gpu.find('utilization')
                    mem = gpu.find('fb_memory_usage')
                    
                    gpu_util = float(util.find('gpu_util').text.split()[0])
                    mem_used = float(mem.find('used').text.split()[0])
                    mem_total = float(mem.find('total').text.split()[0])
                    
                    return {
                        "utilization": gpu_util,
                        "memory_used": mem_used,
                        "memory_total": mem_total,
                        "name": gpu.find('product_name').text
                    }
        except Exception:
            pass
            
    # Mock return for development if no GPU found, or just return empty
    # For the sake of the user seeing the feature working without a GPU, I'll return None 
    # and handle the None in render.py (or mock if requested, but plan said "mock if hardware unavailable" 
    # under Verification, but maybe I should just return None here and let render handle it cleanly)
    return None
