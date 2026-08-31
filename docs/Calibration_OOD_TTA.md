# Day 3 — Calibration + OOD + TTA

## Phase 1 — Temperature Scaling
- Temperature fitted: 0.60 (stable, not at boundary)
- ECE before: 0.0781
- ECE after: 0.0132
- Improvement: 6× better calibration
- Accuracy unchanged: 0.9492

## Phase 2 — OOD Detection
- Method: max softmax probability + cosine similarity to nearest class mean
- Thresholds:
  - Max prob ≥ 0.7678
  - Cosine ≥ 0.4705
- Validation acceptance: 92.9%
- Real beans flagged (test): 4/20 (20%)
- Synthetic OOD flagged: 5/5 (100%)

## Phase 3 — Test-Time Augmentation
- Views: original, h-flip, 90°, 180°
- Non-TTA test accuracy: 0.9542
- TTA test accuracy: ____
- Improvement: +____ points

## Deliverables
- calibration.json
- ood_config.json
- reliability_diagram.png
- confusion_matrix_tta.png