from pathlib import Path
import shutil

src = Path("config.json")
backup = Path("backup/config.json")

backup.parent.mkdir(parents=True, exist_ok=True)

if src.exists():
    shutil.copy(src, backup)
else:
    print("Source missing")
