# src/mytool/core.py
def calculate_disk_percentage(used: int, total: int) -> float:
    if total <= 0:
        raise ValueError("Total must be greater than zero")
    return (used / total) * 100