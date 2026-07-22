import psutil


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory():
    memory = psutil.virtual_memory()

    return {
        "used": round(memory.used / (1024**3), 2),
        "total": round(memory.total / (1024**3), 2),
        "percent": memory.percent,
    }


def get_disk():
    disk = psutil.disk_usage("/")

    return {
        "used": round(disk.used / (1024**3), 2),
        "total": round(disk.total / (1024**3), 2),
        "percent": disk.percent,
    }


def get_uptime():
    seconds = int(psutil.boot_time())

    return seconds