import psutil
import platform
import json
from datetime import datetime


def get_full_system_info():
    """Собирает полную информацию о системе, включая ОС, железо и датчики."""
    try:
        sensors = psutil.sensors_temperatures()
        temperature_info = {
            sensor: [entry._asdict() for entry in entries]
            for sensor, entries in sensors.items()
        } if sensors else "Temperature sensors are not supported"
    except AttributeError:
        temperature_info = "Temperature sensors are not supported on this system."

    info = {
        "os_info": {
            "system": platform.system(),
            "version": platform.version(),
            "release": platform.release(),
            "full_version": platform.platform(),
            "architecture": platform.architecture()[0],
        },
        "system_info": {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.architecture(),
            "cpu": {
                "count": psutil.cpu_count(logical=False),
                "logical_count": psutil.cpu_count(logical=True),
                "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else "Not available",
                "load_avg": psutil.getloadavg() if hasattr(psutil, "getloadavg") else "Not supported",
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "used": psutil.virtual_memory().used,
                "percent_used": psutil.virtual_memory().percent,
            },
            "disks": [disk._asdict() for disk in psutil.disk_partitions()],
            "disk_usage": {
                partition.device: psutil.disk_usage(partition.mountpoint)._asdict()
                for partition in psutil.disk_partitions()
            },
            "network": {
                "interfaces": {
                    name: [addr._asdict() for addr in addrs]
                    for name, addrs in psutil.net_if_addrs().items()
                },
                "stats": {
                    iface: stat._asdict() for iface, stat in psutil.net_if_stats().items()
                },
                "io_counters": {
                    iface: io._asdict()
                    for iface, io in psutil.net_io_counters(pernic=True).items()
                },
            },
            "battery": psutil.sensors_battery()._asdict() if psutil.sensors_battery() else "No battery detected",
            "sensors": temperature_info,
        },
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return info


def main():
    data = get_full_system_info()

    output_file = "system_info.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Информация о системе сохранена в файл: {output_file}")


if __name__ == "__main__":
    main()


# sudo apt update
# sudo apt install python3 python3-pip -y
# sudo apt install python3-pip -y
# pip3 install psutil
#
# python3 info.py
# cat system_info.json

