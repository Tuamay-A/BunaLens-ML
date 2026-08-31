# Training Baseline Model

## Dataset
- Total: 8,000 images (4 classes, 2,000 each)
- Train pool: 6,800 (used for 5-fold CV)
- Held-out test: 1,200 (touched once)

## Model
- Architecture: EfficientNet-B0 (ImageNet pretrained)
- Parameters: 4,012,672
- Classifier head: Dropout(0.3) → Linear(1280→4)

## Training recipe
- Loss: weighted cross-entropy + label smoothing 0.1
- Class weights: defect=1.5, peaberry=1.2, longberry=1.0, premium=0.8
- Optimizer: AdamW (lr=3e-4, weight decay=1e-3)
- Scheduler: CosineAnnealingLR
- Epochs: 8, batch size 32

## Results

### Single split (baseline)
- Test accuracy: 95.42%
- Val-test gap: 0.50 pts
- Defect recall: 92.0%
- Macro F1: 0.954

### 5-fold cross-validation
- Test accuracy: **95.93% ± 0.39%**
- Val accuracy: 95.78% ± 0.61%
- Per-fold test: [96.17, 96.25, 96.25, 95.25, 95.75]

## Deliverables saved
- baseline_efficientnet_b0.pt (15.6 MB)
- baseline_test_metrics.json
- cv_results.json
- confusion_matrix.png
- training_curves.png