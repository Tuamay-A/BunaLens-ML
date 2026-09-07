"""
Show a grid of sample images 10 per class, side by side.
"""
import os
import random
import matplotlib.pyplot as plt
from PIL import Image

# RAW_DIR = r"D:\EGATE\BunaLens_v2\data\raw\USK-Coffee"
RAW_DIR = r"D:\EGATE\Projects\BunaData\data\raw\USK-Coffee"
CLASSES = ['defect', 'longberry', 'peaberry', 'premium']
IMG_EXTS = ('.jpg', '.jpeg', '.png')

def gather_by_class(root):
    by_class = {c: [] for c in CLASSES}
    for split in ['train', 'val', 'test']:
        for cls in CLASSES:
            d = os.path.join(root, split, cls)
            if not os.path.isdir(d):
                continue
            for f in os.listdir(d):
                if f.lower().endswith(IMG_EXTS):
                    by_class[cls].append(os.path.join(d, f))
    return by_class

def main():
    by_class = gather_by_class(RAW_DIR)
    fig, axes = plt.subplots(4, 10, figsize=(20, 8))
    for row, cls in enumerate(CLASSES):
        files = random.sample(by_class[cls], min(10, len(by_class[cls])))
        for col, f in enumerate(files):
            axes[row, col].imshow(Image.open(f))
            axes[row, col].axis('off')
            if col == 0:
                axes[row, col].set_title(cls, fontsize=12, loc='left')
    plt.tight_layout()
    out = r"D:\EGATE\Projects\BunaData\figures\sample_grid.png"
    plt.savefig(out, dpi=120, bbox_inches='tight')
    plt.show()
    print(f"Saved: {out}")

if __name__ == "__main__":
    main()