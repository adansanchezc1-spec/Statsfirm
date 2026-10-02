import os
import shutil
from pathlib import Path

SRC = Path(r"c:\Users\ADAN\OneDrive\Documentos\Statsfirm\AgroStats AndTech\AgroStatsApp")
DST = Path(r"c:\Users\ADAN\OneDrive\Documentos\AgroStatsApp")

print(f"Syncing from {SRC} to {DST}...")

DIRS_TO_SYNC = ["src", "tests", "config", "notebooks", "docs", "app"]
FILES_TO_SYNC = [
    "run_pipeline.py",
    "build_full_notebooks.py",
    "build_master_notebook.py",
    "metadata.json",
    "requirements.txt"
]

# Sync individual files
for fname in FILES_TO_SYNC:
    sf = SRC / fname
    df = DST / fname
    if sf.exists():
        shutil.copy2(sf, df)
        print(f"  Copied {fname}")

# Sync directories
for dname in DIRS_TO_SYNC:
    sd = SRC / dname
    dd = DST / dname
    if not sd.exists():
        continue
    dd.mkdir(parents=True, exist_ok=True)
    for root, dirs, files in os.walk(sd):
        dirs[:] = [d for d in dirs if d not in ["__pycache__", ".pytest_cache", ".git"]]
        rel_root = Path(root).relative_to(sd)
        target_dir = dd / rel_root
        target_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            if f.endswith((".pyc", ".tmp")):
                continue
            src_file = Path(root) / f
            dst_file = target_dir / f
            try:
                shutil.copy2(src_file, dst_file)
            except Exception as e:
                print(f"  Warning: could not copy {src_file.name}: {e}")
    print(f"  Synced directory {dname}")

# Also sync data/processed parquet files
data_proc_src = SRC / "data" / "processed"
data_proc_dst = DST / "data" / "processed"
if data_proc_src.exists():
    data_proc_dst.mkdir(parents=True, exist_ok=True)
    for f in data_proc_src.glob("*.parquet"):
        try:
            shutil.copy2(f, data_proc_dst / f.name)
            print(f"  Copied {f.name}")
        except Exception as e:
            print(f"  Warning: {e}")

print("Sync completed successfully!")
