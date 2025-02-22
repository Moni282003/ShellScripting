import psutil
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.progress import BarColumn, Progress

console = Console()

def get_system_info():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    cpu = psutil.cpu_percent(interval=1)
    uptime = time.time() - psutil.boot_time()

    return {
        "Total RAM": f"{mem.total / (1024**3):.2f} GB",
        "Used RAM": f"{mem.used / (1024**3):.2f} GB",
        "Available RAM": f"{mem.available / (1024**3):.2f} GB",
        "RAM Usage": f"{mem.percent}%",
        "Total Swap": f"{swap.total / (1024**3):.2f} GB",
        "Used Swap": f"{swap.used / (1024**3):.2f} GB",
        "Swap Usage": f"{swap.percent}%",
        "CPU Usage": f"{cpu}%",
        "System Uptime": f"{uptime // 3600:.0f}h {uptime % 3600 // 60:.0f}m {uptime % 60:.0f}s",
    }

def render_system_table():
    table = Table(title="🖥️ System Resource Monitor", show_header=True, header_style="bold magenta")

    table.add_column("Metric", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", justify="right", style="green", no_wrap=True)
    
    sys_info = get_system_info()

    for key, value in sys_info.items():
        table.add_row(key, value)

    return table

def render_progress_bar(label, percent, color):
    progress = Progress(
        f"[bold {color}]{label}:[/bold {color}]",
        BarColumn(bar_width=None, style=color),
        f"[{color}]{percent}%[/]",
    )
    progress.add_task("", total=100, completed=float(percent))
    return progress

with Live(console=console, refresh_per_second=1) as live:
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent

        table = render_system_table()
        
        console.clear()
        console.print(table)
        
        console.print(render_progress_bar("🟢 RAM Usage", mem_usage, "green"))
        console.print(render_progress_bar("🔴 CPU Usage", cpu_usage, "red"))

        time.sleep(1)
