# BunaLens — Model Card

**Version:** 1.0
**Model type:** EfficientNet-B0 (ImageNet pretrained, fine-tuned)
**Framework:** PyTorch → TensorFlow Lite (mobile deployment)
**Task:** 4-class classification of Ethiopian green coffee beans
**Input:** 224×224 RGB image of a single bean
**Output:** Probability distribution over 4 classes

---

## Intended Use

**Primary use case**
An on-device mobile assistant for coffee quality pre-screening.
Supports — but does not replace — trained Q-graders.

**Intended users**
- Smallholder farmers (self-check before selling)
- Cooperatives (delivery screening)
- Exporters (defect leakage reduction)
- Coffee labs (assistive triage)

**Out-of-scope uses**
- Certification or legal grading
- Predicting SCA cupping scores
- Roasted coffee (trained on green beans only)
- Multi-bean batch images (single bean only)

---

## Performance

**Overall test accuracy:** 95.58%

**Cross-validation:** 95.93% ± 0.39% (5-fold)

**Per-class metrics (test set):**

| Class | Precision | Recall | F1 |
|---|---|---|---|
| Defect | 24 | 0.920 | 0.948 |
| Longberry | — | 1.000 | 0.963 |
| Peaberry | — | 0.960 | 0.965 |
| Premium | — | 0.943 | 0.946 |

**Calibration:** Expected Calibration Error (ECE) = 0.0132
(down from 0.0781 before temperature scaling)

**Inference time:** ~50 ms per bean on mid-range Android; ~200 ms with TTA

**Model size:** 15.6 MB (float32 TFLite)

---

## Training Data

**Dataset:** USK-Coffee (8,000 images)
**Classes:** Defect, Longberry, Peaberry, Premium (2,000 each)
**Split:** 70/15/15 stratified → 5,600 / 1,200 / 1,200
**Source:** Single environment (consistent lighting, background, camera)
**Labels:** Inherited from original dataset

**Preprocessing**
- Resize to 256×256, center-crop to 224×224
- ImageNet normalization (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

**Augmentation (training only)**
- RandomResizedCrop (scale 0.6–1.0), horizontal flip, rotation ±25°
- ColorJitter, RandomAffine, RandomErasing

---

## Evaluation

**Test set:** 1,200 images (held out from training)

**Error analysis**
- Total errors: 53 / 1200 (4.42%)
- Largest error types:
  - defect → longberry (11)
  - premium → longberry (10)
  - defect → premium (8)
- Error rate by true class:
  - Longberry: 0.00% ✅
  - Peaberry: 4.00%
  - Premium: 5.67%
  - Defect: 8.00%

**Confidence calibration**
- Mean confidence on correct predictions: 96.8%
- Mean confidence on incorrect predictions: 75.5%
- Model confidence tracks accuracy — low-confidence predictions are more likely wrong

---

## Limitations

1. **Single-source training data** — performance may degrade on photos from
   different lighting, backgrounds, cameras, or bean origins. External
   validation is a priority for the next version.

2. **Defect recall = 92%** — misses ~8% of defects, mostly those visually
   similar to longberry. This is above the 85% target for assistive use
   but below the 95%+ expected of certified Q-graders.

3. **4-class simplification** — real coffee grading distinguishes ~10 defect
   types with point deductions. Our "defect" class is a coarse bucket.

4. **Single-bean images only** — the model was not trained on batch photos.
   It cannot grade a pile of beans.

5. **Visual features only** — the model cannot assess taste, aroma, moisture,
   density, or flavor. It is a visual proxy for pre-roast quality, not a
   substitute for cupping.

6. **Confident errors** — approximately 49% of errors had confidence > 0.8.
   The OOD system flags low-confidence predictions but cannot catch
   confident mistakes.

---

## Ethical Considerations

- **Not a replacement for human judgment** — designed to assist, not replace,
  Q-graders.
- **Not for labor/price exploitation** — should never be used to justify
  underpaying farmers. It is a quality-visibility tool, not a gatekeeping tool.
- **Transparency** — Grad-CAM heatmaps show exactly what the model looks at,
  enabling user trust and error analysis.
- **Offline operation** — no images leave the user's device; no data collection.

---

## Technical Stack

- **Training:** PyTorch (EfficientNet-B0, ImageNet pretrained)
- **Augmentation:** torchvision transforms
- **Calibration:** Temperature scaling (T = 0.60)
- **OOD detection:** Max softmax + cosine similarity to class means
- **TTA:** 2-view (original + horizontal flip) — gain of +0.16 pts
- **Export:** PyTorch → ONNX → TFLite (float32)
- **Deployment:** Flutter (Android), on-device inference

---

## Files

- `baseline_efficientnet_b0.pt` — PyTorch checkpoint (15.6 MB)
- `coffee_efficientnet_b0_float32.tflite` — deployable model
- `calibration.json`, `ood_config.json`, `tta_config.json` — inference configs
- `confusion_matrix.png`, `gradcam_*.png` — evaluation figures

---

## Contact

For questions about this model, training pipeline, or intended use:
[Your name / project contact]
