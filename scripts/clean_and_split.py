"""
Merge all existing splits, clean, re-split 70/15/15 stratified,
and write a manifest CSV.
"""

import os
import shutil
import random
import pandas as pd
from collections import defaultdict

# ---- CHANGE THIS to your project path ----
PROJECT_DIR = r"D:\EGATE\Projects\BunaData"

# Input: original USK-Coffee layout with train/val/test
RAW_DIR    = os.path.join(PROJECT_DIR, "data", "raw", "USK-Coffee")

# Output: new splits
CLEAN_DIR  = os.path.join(PROJECT_DIR, "data", "clean")     # not used yet, but create
SPLIT_DIR  = os.path.join(PROJECT_DIR, "data", "splits")    # new train/val/test
MANIFEST   = os.path.join(PROJECT_DIR, "data", "manifest.csv")

CLASSES    = ['defect', 'longberry', 'peaberry', 'premium']
IMG_EXTS   = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

SPLIT_RATIOS = {'train': 0.70, 'val': 0.15, 'test': 0.15}
RANDOM_SEED  = 42


def gather_all_images(root):
    """Walk the USK-Coffee tree and collect every image path + its label."""
    items = []
    for split in ['train', 'val', 'test']:
        for cls in CLASSES:
            d = os.path.join(root, split, cls)
            if not os.path.isdir(d):
                print(f"  WARNING: missing folder {d}")
                continue
            for f in os.listdir(d):
                if f.lower().endswith(IMG_EXTS):
                    items.append({
                        'original_split': split,
                        'class': cls,
                        'filename': f,
                        'path': os.path.join(d, f),
                    })
    return items


def main():
    random.seed(RANDOM_SEED)

    print("=" * 60)
    print("STEP 1 — Gather all images")
    print("=" * 60)
    items = gather_all_images(RAW_DIR)
    print(f"Total images found: {len(items)}")

    # Group by class
    by_class = defaultdict(list)
    for it in items:
        by_class[it['class']].append(it)

    print("\nImages per class:")
    for cls in CLASSES:
        print(f"  {cls:12s}: {len(by_class[cls])}")

    print("\n" + "=" * 60)
    print("STEP 2 — Stratified split")
    print("=" * 60)

    splits = {'train': [], 'val': [], 'test': []}

    for cls in CLASSES:
        class_items = by_class[cls][:]
        random.shuffle(class_items)
        n = len(class_items)
        n_train = int(n * SPLIT_RATIOS['train'])
        n_val   = int(n * SPLIT_RATIOS['val'])
        # rest to test to avoid off-by-one

        splits['train'].extend(class_items[:n_train])
        splits['val'].extend(class_items[n_train:n_train + n_val])
        splits['test'].extend(class_items[n_train + n_val:])

    for split, items_ in splits.items():
        print(f"  {split:5s}: {len(items_)} images")

    print("\n" + "=" * 60)
    print("STEP 3 — Copy to new split folders")
    print("=" * 60)

    if os.path.isdir(SPLIT_DIR):
        shutil.rmtree(SPLIT_DIR)

    rows = []
    for split, items_ in splits.items():
        for it in items_:
            dst_dir = os.path.join(SPLIT_DIR, split, it['class'])
            os.makedirs(dst_dir, exist_ok=True)
            dst_path = os.path.join(dst_dir, it['filename'])

            # Handle rare filename collisions across original splits
            if os.path.exists(dst_path):
                base, ext = os.path.splitext(it['filename'])
                dst_path = os.path.join(dst_dir, f"{base}__dup{ext}")

            shutil.copy2(it['path'], dst_path)

            rows.append({
                'filename': os.path.basename(dst_path),
                'class': it['class'],
                'split': split,
                'original_split': it['original_split'],
                'source_path': it['path'],
                'dest_path': dst_path,
            })

    df = pd.DataFrame(rows)
    df.to_csv(MANIFEST, index=False)

    print(f"\nCopied {len(df)} images to: {SPLIT_DIR}")
    print(f"Manifest saved to: {MANIFEST}")

    print("\n" + "=" * 60)
    print("STEP 4 — Verify split balance")
    print("=" * 60)
    pivot = df.groupby(['split', 'class']).size().unstack(fill_value=0)
    print(pivot)

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
    print("Your new train/val/test folders are at:")
    print(f"  {SPLIT_DIR}")
    print("\nUse these folders for training on Day 2.")


if __name__ == "__main__":
    main()