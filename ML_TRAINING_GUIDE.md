# 🤖 ML Model Training Guide - Pronunciation Scoring

Complete guide to train and deploy a machine learning model for pronunciation quality scoring (0-100).

---

## 📋 Overview

Replace heuristic scoring with a trained neural network that predicts pronunciation quality from acoustic features.

**Pipeline:**
```
Audio Data → Feature Extraction → Dataset CSV → Model Training → Export → Backend Integration
```

---

## 🚀 Quick Start (5 Steps)

### Step 1: Prepare Training Data

```bash
cd backend
python prepare_training_data.py
```

**Options:**
1. Create mock labels (for testing) - generates random scores
2. Prepare dataset from existing labels - uses real human evaluations

**Output:** `../data/training_data.csv`

### Step 2: Upload to Google Colab

1. Open `ml_colab/pronunciation_scoring_training.ipynb` in Google Colab
2. Enable GPU: Runtime → Change runtime type → GPU
3. Upload `training_data.csv` when prompted

### Step 3: Train Model

Run all cells in the notebook:
- Data loading and exploration
- Model training (100 epochs with early stopping)
- Evaluation on test set
- Model export

**Expected Training Time:** 5-10 minutes on GPU

### Step 4: Download Model Files

Download these 3 files from Colab:
- `pronunciation_scorer.pth` - Model weights
- `model_info.json` - Architecture info
- `scaler_params.json` - Feature normalization

### Step 5: Deploy to Backend

```bash
# Create models directory
mkdir backend/models

# Move downloaded files
mv pronunciation_scorer.pth backend/models/
mv model_info.json backend/models/
mv scaler_params.json backend/models/

# Restart backend
cd backend
python main.py
```

✅ **ML scoring now active!**

---

## 📊 Data Preparation Details

### Expected Data Structure

```
data/
  participant_XXX/
    kelimeler/
      01_araba.wav
      01_araba_result.json          ← Score label
      02_çocuk.wav
      02_çocuk_result.json
      ...
```

### Label Format (`*_result.json`)

```json
{
  "word": "araba",
  "score": 85.5,
  "labeled": true,
  "evaluator": "expert",
  "notes": "Good pronunciation, slight accent"
}
```

**Score Range:** 0-100
- 90-100: Excellent (native-like)
- 80-89: Good (clear, understandable)
- 70-79: Fair (some errors)
- 60-69: Poor (many errors)
- 0-59: Very poor (unintelligible)

### Feature Extraction

**57 features extracted per audio file:**

| Category | Count | Features |
|----------|-------|----------|
| MFCCs | 39 | 13 coefficients × (mean + std + delta) |
| Pitch | 3 | Mean, std, range |
| Formants | 5 | F1, F2, F3 (mean + std) |
| Energy | 3 | RMS (mean, std, max) |
| Spectral | 5 | Centroid, rolloff, bandwidth, flatness, ZCR |
| Temporal | 1 | Tempo |
| Harmonic | 1 | Harmonic ratio |

### Creating Labels

**Option 1: Manual Labeling (Recommended)**

Have human experts evaluate recordings:

```python
# Label single recording
score = evaluate_pronunciation(audio_file)  # 0-100

result = {
    "word": "araba",
    "score": score,
    "labeled": True,
    "evaluator": "expert_name",
    "timestamp": "2025-01-17T12:00:00"
}

with open("01_araba_result.json", "w") as f:
    json.dump(result, f, indent=2)
```

**Option 2: Mock Labels (Testing Only)**

```bash
cd backend
python prepare_training_data.py
# Choose option 1
```

⚠️ **Warning:** Mock labels use random scores and won't produce a useful model!

---

## 🧠 Model Architecture

### Neural Network Design

```python
PronunciationScorer(
  input_dim=57,
  hidden_layers=[128, 64, 32],
  dropout=0.3,
  output_dim=1,
  activation='relu',
  output_activation='sigmoid'
)
```

**Layer Breakdown:**
```
Input (57) 
  → Dense(128) → BatchNorm → ReLU → Dropout(0.3)
  → Dense(64) → BatchNorm → ReLU → Dropout(0.3)
  → Dense(32) → BatchNorm → ReLU → Dropout(0.3)
  → Dense(1) → Sigmoid
Output (0-1, scaled to 0-100)
```

**Total Parameters:** ~12,000

### Training Configuration

```python
BATCH_SIZE = 32
LEARNING_RATE = 0.001
OPTIMIZER = Adam(weight_decay=1e-5)
LOSS = MSELoss
SCHEDULER = ReduceLROnPlateau(patience=5)
EARLY_STOPPING = True(patience=15)
MAX_EPOCHS = 100
```

### Data Split

- **Train:** 70% - Model learns from this
- **Validation:** 15% - Hyperparameter tuning
- **Test:** 15% - Final evaluation (never seen during training)

---

## 📈 Training Process

### 1. Data Loading

```python
df = pd.read_csv('training_data.csv')
X = df[feature_columns]  # 57 features
y = df['score'] / 100.0  # Normalize to [0, 1]
```

### 2. Feature Normalization

```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save for inference
scaler_params = {
    'mean': scaler.mean_,
    'scale': scaler.scale_,
    'feature_names': feature_columns
}
```

### 3. Training Loop

```python
for epoch in range(MAX_EPOCHS):
    # Training
    model.train()
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        output = model(batch_X)
        loss = criterion(output, batch_y)
        loss.backward()
        optimizer.step()
    
    # Validation
    model.eval()
    val_loss = evaluate(model, X_val, y_val)
    
    # Early stopping
    if val_loss < best_val_loss:
        save_checkpoint(model)
    elif patience_exceeded:
        break
```

### 4. Evaluation Metrics

- **MSE (Mean Squared Error)** - Training objective
- **MAE (Mean Absolute Error)** - Average prediction error
- **RMSE (Root Mean Squared Error)** - Error in original scale

**Target Performance:**
- MAE < 5 points (on 0-100 scale)
- RMSE < 7 points
- R² > 0.85

---

## 🔧 Backend Integration

### Model Loading

The backend automatically loads the ML model on startup:

```python
# backend/ml_scorer.py
scorer = MLPronunciationScorer(model_dir="models")

if scorer.is_available():
    print("✓ ML model loaded")
else:
    print("⚠ Using heuristic scoring")
```

### Inference Pipeline

```python
# 1. Extract features
features = extract_acoustic_features(audio_path)

# 2. ML Prediction
score = ml_scorer.predict_score(features)  # 0-100

# 3. Return result
{
    "word": "araba",
    "overall": 85.3,
    "grade": "B (İyi)",
    "scoring_method": "ml_model"  # vs "heuristic"
}
```

### Fallback Behavior

```
Try ML Model
    ↓
If unavailable → Heuristic Scoring
    ↓
Always return valid score
```

---

## 🧪 Testing

### Test ML Model

```bash
cd backend
python -c "
from ml_scorer import get_ml_scorer
scorer = get_ml_scorer()
print('ML Model Available:', scorer.is_available())
"
```

### Test Full Pipeline

```bash
cd backend
python test_analysis.py ../data/participant_XXX/kelimeler/01_araba.wav araba
```

**Expected Output:**
```
✅ Audio Analysis Complete
   Word: araba
   Overall Score: 85.3
   Grade: B (İyi)
   Scoring Method: ml_model  ← Should be "ml_model"
```

### Compare ML vs Heuristic

```python
from inference import analyze_pronunciation

# With ML
result_ml = analyze_pronunciation(audio, word, phonemes, use_ml=True)

# Without ML (heuristic)
result_heuristic = analyze_pronunciation(audio, word, phonemes, use_ml=False)

print(f"ML Score: {result_ml['overall']}")
print(f"Heuristic Score: {result_heuristic['overall']}")
```

---

## 📁 File Structure

```
PhoneticHybrid/
├── backend/
│   ├── prepare_training_data.py       ← Step 1: Data prep
│   ├── ml_scorer.py                   ← ML scorer class
│   ├── inference.py                   ← Updated with ML
│   └── models/                        ← Model files
│       ├── pronunciation_scorer.pth   ← Weights
│       ├── model_info.json           ← Architecture
│       └── scaler_params.json        ← Normalization
├── ml_colab/
│   └── pronunciation_scoring_training.ipynb  ← Step 2-4: Training
├── data/
│   ├── participant_XXX/
│   └── training_data.csv             ← Prepared dataset
└── ML_TRAINING_GUIDE.md              ← This file
```

---

## 🐛 Troubleshooting

### Issue 1: "No labeled data found"

**Problem:** No `*_result.json` files exist

**Solution:**
```bash
# Create mock labels for testing
python prepare_training_data.py
# Choose option 1

# OR manually label your data
# See "Creating Labels" section above
```

### Issue 2: "Model not loaded"

**Problem:** Model files not in `backend/models/`

**Solution:**
```bash
# Check files exist
ls backend/models/
# Should show: pronunciation_scorer.pth, model_info.json, scaler_params.json

# If missing, re-download from Colab or retrain
```

### Issue 3: "Feature dimension mismatch"

**Problem:** Different features in training vs inference

**Solution:**
```bash
# Ensure same feature extraction code
# Check scaler_params.json has correct feature_names
# Retrain model if feature extraction was modified
```

### Issue 4: "High prediction error (MAE > 10)"

**Problem:** Not enough training data or poor labels

**Solution:**
- Collect more labeled data (aim for 500+ samples)
- Check label quality - are they consistent?
- Verify labels are on 0-100 scale
- Check data distribution (avoid all scores near 80)

### Issue 5: "Overfitting (train MAE << val MAE)"

**Problem:** Model memorizing training data

**Solution:**
```python
# Increase dropout
model = PronunciationScorer(dropout=0.5)  # was 0.3

# Reduce model complexity
model = PronunciationScorer(hidden_dims=[64, 32])  # was [128, 64, 32]

# Collect more diverse data
```

---

## 📊 Performance Benchmarks

### Minimum Data Requirements

| Samples | Expected MAE | Quality |
|---------|-------------|---------|
| < 100 | > 15 | Poor (insufficient) |
| 100-300 | 10-15 | Fair (basic model) |
| 300-500 | 7-10 | Good (usable) |
| 500-1000 | 5-7 | Very Good |
| > 1000 | < 5 | Excellent |

### Expected Training Time

| Dataset Size | GPU Time | CPU Time |
|-------------|----------|----------|
| 100 samples | 1 min | 5 min |
| 500 samples | 3 min | 15 min |
| 1000 samples | 5 min | 25 min |
| 5000 samples | 15 min | 90 min |

---

## 🔄 Retraining Workflow

### When to Retrain

✅ **Retrain when:**
- Collected more labeled data
- Model performance degrades
- Changed feature extraction
- Want to improve accuracy

### How to Retrain

```bash
# 1. Add new labeled data to data/
# (New participants or relabeled existing)

# 2. Regenerate dataset
python prepare_training_data.py

# 3. Upload new CSV to Colab
# 4. Run training notebook
# 5. Download and deploy new model

# 6. Test improvement
python test_analysis.py sample.wav word
```

### Version Control

```bash
# Backup old model
mv backend/models backend/models_v1_backup

# Deploy new model
mkdir backend/models
mv pronunciation_scorer.pth backend/models/
```

---

## 📚 Advanced Topics

### Uncertainty Estimation

```python
# Get prediction with confidence
from ml_scorer import get_ml_scorer

scorer = get_ml_scorer()
result = scorer.predict_with_confidence(features, num_samples=10)

print(f"Score: {result['score']:.1f}")
print(f"Uncertainty: ±{result['std']:.1f}")
print(f"95% CI: [{result['confidence_interval'][0]:.1f}, {result['confidence_interval'][1]:.1f}]")
```

### Custom Features

Add new features to improve accuracy:

```python
# In prepare_training_data.py
def extract_features_from_audio(audio_path):
    # ... existing features ...
    
    # Add custom feature
    custom_feature = compute_custom_metric(y, sr)
    features['custom_metric'] = custom_feature
    
    return features
```

**Important:** Retrain model after adding features!

### Multi-Task Learning

Train model to predict multiple targets:

```python
# Labels with multiple scores
{
    "word": "araba",
    "overall_score": 85,
    "fluency_score": 90,
    "accuracy_score": 80,
    "clarity_score": 85
}
```

### Active Learning

Prioritize labeling samples where model is uncertain:

```python
# Find uncertain predictions
for sample in unlabeled_data:
    prediction = scorer.predict_with_confidence(sample)
    if prediction['std'] > threshold:
        add_to_labeling_queue(sample)
```

---

## ✅ Checklist

### Data Preparation
- [ ] Audio files exist in `data/participant_*/kelimeler/*.wav`
- [ ] Label files created (`*_result.json`)
- [ ] Labels are on 0-100 scale
- [ ] At least 100 labeled samples (300+ recommended)
- [ ] `training_data.csv` generated successfully

### Training
- [ ] Uploaded CSV to Colab
- [ ] GPU enabled in Colab
- [ ] Training completed without errors
- [ ] Test MAE < 10 (preferably < 5)
- [ ] Downloaded 3 model files

### Deployment
- [ ] Model files in `backend/models/`
- [ ] Backend starts without errors
- [ ] ML model loads successfully
- [ ] Test prediction works
- [ ] Response includes `"scoring_method": "ml_model"`

### Validation
- [ ] Tested with sample audio
- [ ] Scores are reasonable (0-100)
- [ ] Compare ML vs heuristic scores
- [ ] Performance acceptable for production

---

## 📞 Support

**Common Questions:**

Q: How many samples do I need?
A: Minimum 300, ideal 500+. More data = better model.

Q: How long to train?
A: 5-10 minutes on GPU with early stopping.

Q: Can I use CPU?
A: Yes, but slower. GPU recommended.

Q: What if ML model fails?
A: System automatically falls back to heuristic scoring.

Q: How to improve accuracy?
A: Collect more data, improve label quality, tune hyperparameters.

---

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Last Updated:** 2025-01-17
