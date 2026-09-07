"""
Audit the raw USK-Coffee dataset.
- Count images per class
- Detect corrupt files
- Report image dimensions
- Find exact duplicates (by hash)
"""

import os
import hashlib
from collections import defaultdict
from PIL import Image
from tqdm import tqdm

RAW_DIR = r"D:\EGATE\Projects\BunaData\data\raw"
IMG_EXTS = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

def find_images(root):
    """Walk the folder and return a list of image paths."""
    paths = []
    for dirpath, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith(IMG_EXTS):
                paths.append(os.path.join(dirpath, f))
    return paths

def md5_of_file(path):
    """Compute MD5 hash of file contents."""
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    print(f"Scanning: {RAW_DIR}")
    all_images = find_images(RAW_DIR)
    print(f"Total image files found: {len(all_images)}\n")

    # --- 1. Count per split/class ---
    print("=" * 60)
    print("1. COUNT PER SPLIT / CLASS")
    print("=" * 60)
    counts = defaultdict(int)
    for p in all_images:
        rel = os.path.relpath(p, RAW_DIR)
        parts = rel.split(os.sep)
        if len(parts) >= 3:
            split, cls = parts[0], parts[1]
            counts[(split, cls)] += 1
    for (split, cls), n in sorted(counts.items()):
        print(f"  {split:8s} / {cls:12s}: {n}")

    # --- 2. Detect corrupt files ---
    print("\n" + "=" * 60)
    print("2. CORRUPT FILE CHECK")
    print("=" * 60)
    corrupt = []
    dims = defaultdict(int)
    for p in tqdm(all_images, desc="Verifying images"):
        try:
            with Image.open(p) as im:
                im.verify()
            with Image.open(p) as im:
                dims[im.size] += 1
        except Exception as e:
            corrupt.append((p, str(e)))

    print(f"Corrupt images: {len(corrupt)}")
    for p, err in corrupt[:10]:
        print(f"  {p}\n    → {err}")

    # --- 3. Dimensions ---
    print("\n" + "=" * 60)
    print("3. IMAGE DIMENSIONS")
    print("=" * 60)
    for size, n in sorted(dims.items(), key=lambda x: -x[1])[:10]:
        print(f"  {size}: {n} images")

    # --- 4. Duplicates by MD5 ---
    print("\n" + "=" * 60)
    print("4. DUPLICATE FILES (by MD5)")
    print("=" * 60)
    hashes = defaultdict(list)
    for p in tqdm(all_images, desc="Hashing files"):
        hashes[md5_of_file(p)].append(p)

    dupes = {h: ps for h, ps in hashes.items() if len(ps) > 1}
    total_dup_files = sum(len(ps) - 1 for ps in dupes.values())
    print(f"Duplicate hash groups: {len(dupes)}")
    print(f"Redundant files (can be removed): {total_dup_files}")

    if dupes:
        print("\n  First 5 duplicate groups:")
        for h, ps in list(dupes.items())[:5]:
            print(f"  Hash {h[:8]}...")
            for p in ps:
                print(f"    {os.path.relpath(p, RAW_DIR)}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total images scanned:    {len(all_images)}")
    print(f"Corrupt:                 {len(corrupt)}")
    print(f"Exact duplicate groups:  {len(dupes)}")
    print(f"Redundant duplicate files: {total_dup_files}")
    print(f"Unique images (approx):  {len(all_images) - total_dup_files}")

if __name__ == "__main__":
    main()