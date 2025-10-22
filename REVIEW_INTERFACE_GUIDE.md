# 📋 Manual Review Interface - Usage Guide

Complete guide for using the manual pronunciation review interface to create labeled training data.

---

## 🎯 Purpose

The Review Interface allows human evaluators to:
- Listen to participant recordings
- Assign quality scores (0-100)
- Add detailed notes and observations
- View participant information and survey data
- Track labeling progress

**This creates the labeled dataset needed to train the ML model.**

---

## 🚀 Quick Start

### 1. Start Backend

```bash
cd backend
python main.py
```

**Expected:** Backend running on `http://localhost:8000`

### 2. Start Frontend

```bash
cd frontend
npm run dev
```

**Expected:** Frontend running on `http://localhost:3000`

### 3. Access Review Interface

1. Open `http://localhost:3000` in browser
2. Click **"📋 Manuel İnceleme"** button
3. Review interface opens

---

## 📊 Interface Overview

### Main Dashboard

**Top Section - Global Statistics:**
- Total Participants
- Total Recordings
- Labeled/Unlabeled counts
- Progress bar showing labeling completion

**Left Panel - Participants List:**
- All participants with IDs
- Recording counts
- Labeling status
- Survey completion status

**Right Panel - Participant Details:**
- Survey information (age, gender, Turkish level, etc.)
- List of all recordings
- Audio playback
- Labeling interface

---

## 🎵 Labeling Workflow

### Step 1: Select Participant

In the participants table:
- Click **"View"** button on any participant
- Participant details load on the right

### Step 2: Review Survey Data

Check participant background:
- Age and gender
- Native language
- Turkish proficiency level
- Accent information

**Use this context when evaluating pronunciation quality.**

### Step 3: Listen to Recording

For each recording:
1. Click **▶️ Play** button to listen
2. Listen carefully (can replay multiple times)
3. Note pronunciation quality

### Step 4: Open Labeling Dialog

Click **"Label"** or **"Edit"** button on a recording

### Step 5: Assign Score

**Score Guidelines (0-100):**

| Range | Quality | Description |
|-------|---------|-------------|
| 90-100 | Excellent | Native-like pronunciation, no errors |
| 80-89 | Good | Clear and understandable, minor errors |
| 70-79 | Fair | Understandable with some effort, noticeable errors |
| 60-69 | Poor | Difficult to understand, many errors |
| 0-59 | Very Poor | Unintelligible, severe pronunciation issues |

**Scoring Factors:**
- ✓ Phoneme accuracy (correct sounds)
- ✓ Pitch and intonation
- ✓ Vowel formants (a, e, i, o, u sounds)
- ✓ Consonant clarity
- ✓ Rhythm and stress
- ✓ Overall intelligibility

### Step 6: Select Quality Rating

Choose overall quality:
- **Excellent** - Native-like pronunciation
- **Good** - Clear, understandable
- **Fair** - Some errors
- **Poor** - Many errors

### Step 7: Enter Your Name

Enter evaluator name (for tracking who labeled what)

### Step 8: Add Notes (Optional)

Add specific observations:
- "Good vowel sounds, but 'ş' pronunciation needs work"
- "Native English speaker accent detected"
- "Strong 'r' rolling, excellent!"
- "Pitch too flat, lacks natural intonation"

### Step 9: Save Label

Click **"Save Label"** button

**Result:**
- Label saved to `data/participant_XXX/kelimeler/*_result.json`
- Recording marked as "Labeled" with green chip
- Progress statistics updated

---

## 📁 Label File Format

When you save a label, it creates a JSON file:

**File:** `01_araba_result.json`

```json
{
  "word": "araba",
  "score": 85.5,
  "labeled": true,
  "evaluator": "Dr. Smith",
  "notes": "Good pronunciation overall. Slight accent on 'r' sound.",
  "pronunciation_quality": "good",
  "specific_issues": [],
  "timestamp": "2025-01-17T15:30:00.000Z"
}
```

---

## 🎯 Best Practices

### Consistency

✓ **Use the same criteria for all recordings**  
✓ **Take breaks to avoid evaluator fatigue**  
✓ **Compare similar scores periodically**  
✓ **Document your scoring rationale in notes**

### Quality Standards

**For Scores 90-100 (Excellent):**
- Indistinguishable from native speaker
- Perfect phoneme articulation
- Natural rhythm and stress
- Appropriate pitch variation

**For Scores 80-89 (Good):**
- Minor accent acceptable
- 1-2 phoneme errors tolerable
- Generally clear and fluent
- Easy to understand

**For Scores 70-79 (Fair):**
- Noticeable non-native accent
- 3-5 phoneme errors
- Some hesitation acceptable
- Understandable with attention

**For Scores 60-69 (Poor):**
- Strong foreign accent
- Multiple pronunciation errors
- Difficult to understand
- Requires repetition

**For Scores 0-59 (Very Poor):**
- Severe pronunciation issues
- Unintelligible
- Wrong phonemes
- Cannot understand intended word

### Common Scoring Mistakes

❌ **Too lenient** - Giving high scores to avoid being harsh  
❌ **Too strict** - Expecting perfection from non-natives  
❌ **Inconsistent** - Changing criteria mid-session  
❌ **Bias** - Favoring certain accents/backgrounds  

✅ **Correct approach:**
- Be objective and consistent
- Focus on intelligibility
- Consider learner level
- Use the full 0-100 range

---

## 📈 Progress Tracking

### Global Stats

View overall progress:
- **Total recordings** - All audio files collected
- **Labeled** - How many have scores
- **Unlabeled** - How many still need review
- **Progress %** - Completion percentage

**Goal:** Label all recordings before ML training

### Per-Participant Stats

Each participant shows:
- Total recordings count
- Labeled/unlabeled breakdown
- Survey completion status

**Strategy:** Focus on participants with most unlabeled recordings

---

## 🔄 Editing Labels

### Re-labeling

If you want to change a score:
1. Click **"Edit"** on labeled recording
2. Previous score loads automatically
3. Modify score/notes
4. Click **"Save Label"** to overwrite

### Deleting Labels

Currently not supported in UI, but can delete manually:
```bash
# Delete label file
rm data/participant_XXX/kelimeler/01_araba_result.json
```

---

## 🎧 Audio Playback Tips

### Listening Best Practices

✓ **Use good headphones** - Better sound quality  
✓ **Quiet environment** - Minimize background noise  
✓ **Listen 2-3 times** - Confirm your evaluation  
✓ **Focus on specific phonemes** - Break down the word  

### Audio Controls

- Click ▶️ to play
- Click ⏸️ to pause (while playing)
- Click again to restart

**Keyboard shortcut:** Just click the play button multiple times to replay

---

## 📝 Example Labeling Session

### Scenario: Evaluating "pencere" (window)

**Participant:** Non-native speaker, English background, intermediate Turkish

**Audio plays:** "pen-je-re" (slight accent, 'ç' pronounced as 'j')

**Evaluation:**

1. **Score:** 75/100
   - Good attempt, understandable
   - Clear vowels (e, e, e)
   - 'ç' → 'j' error (common for English speakers)
   - Otherwise clear pronunciation

2. **Quality:** Fair

3. **Notes:** "Clear vowels and good stress. 'ç' sound pronounced as 'j' (common English speaker error). Otherwise intelligible."

4. **Save** ✅

**Result:** Useful training data for ML model

---

## 🎓 Training the ML Model

After labeling recordings:

### Minimum Requirements

- **300+ labeled samples** - Minimum for basic model
- **500+ labeled samples** - Recommended for good accuracy
- **1000+ labeled samples** - Excellent model performance

### Prepare Dataset

```bash
cd backend
python prepare_training_data.py
# Choose option 2 (existing labels)
```

**Output:** `data/training_data.csv`

### Train Model

1. Upload CSV to Google Colab
2. Train model (5-10 minutes)
3. Download model files
4. Deploy to backend

**See:** `ML_TRAINING_GUIDE.md` for complete instructions

---

## 🐛 Troubleshooting

### Issue: "No participants shown"

**Cause:** No participant data collected yet

**Solution:**
- Use main test flow to collect recordings
- Or check `data/` directory exists and has `participant_*` folders

### Issue: "Audio doesn't play"

**Cause:** Backend not serving audio files correctly

**Solution:**
```bash
# Check backend is running
curl http://localhost:8000/health

# Test audio endpoint
curl http://localhost:8000/audio/participant_XXX/01_araba.wav
```

### Issue: "Can't save label"

**Cause:** Backend API not responding

**Solution:**
- Check browser console for errors
- Verify backend is running
- Check CORS configuration
- Ensure evaluator name is filled

### Issue: "Progress not updating"

**Cause:** Need to refresh data

**Solution:**
- Click different participant then back
- Refresh browser page
- Check if label file was actually created

---

## 🔐 Security Considerations

### Data Privacy

✅ **Participant IDs are anonymized** (UUID format)  
✅ **No personal information in labels**  
✅ **Audio stored locally only**  
✅ **KVKK compliant data handling**

### Access Control

Currently no authentication:
- ⚠️ Anyone with access can label
- Consider adding login for production
- Track evaluator names for accountability

---

## 📊 Statistics & Reporting

### Export Labeling Summary

Get overview of labeling status:

```bash
# API endpoint
curl http://localhost:8000/review/stats
```

**Response:**
```json
{
  "total_participants": 25,
  "total_recordings": 250,
  "labeled_recordings": 180,
  "unlabeled_recordings": 70,
  "labeling_progress": 72.0
}
```

### Per-Evaluator Stats

Not currently tracked, but can be added:
- Count labels by evaluator name
- Track average scores per evaluator
- Identify inter-rater reliability

---

## 🎯 Labeling Goals

### Phase 1: Initial Training (300 labels)

**Goal:** Get model working  
**Time:** ~3-4 hours (1 evaluator)  
**Result:** Basic ML model (MAE ~10)

### Phase 2: Quality Improvement (500 labels)

**Goal:** Improve accuracy  
**Time:** ~6-7 hours  
**Result:** Good ML model (MAE ~7)

### Phase 3: Production Ready (1000+ labels)

**Goal:** High accuracy  
**Time:** ~12-15 hours  
**Result:** Excellent ML model (MAE <5)

**Strategy:**
- Multiple evaluators working in parallel
- Focus on diverse speakers
- Include various pronunciation levels

---

## ✅ Quality Control Checklist

Before training ML model:

- [ ] All recordings have labels
- [ ] Scores use full 0-100 range (not all around 80)
- [ ] Notes added for unusual cases
- [ ] Evaluator names filled in
- [ ] No duplicate labels (check for errors)
- [ ] Scores are consistent with quality ratings
- [ ] Survey data reviewed for context

---

## 📚 API Reference

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/review/participants` | List all participants |
| GET | `/review/participants/{id}` | Get participant details |
| POST | `/review/label/{id}/{file}` | Save label |
| GET | `/review/label/{id}/{file}` | Get existing label |
| DELETE | `/review/label/{id}/{file}` | Delete label |
| GET | `/review/stats` | Get global statistics |
| GET | `/audio/{id}/{file}` | Stream audio file |

---

## 💡 Tips & Tricks

### Efficient Labeling

✓ **Label in batches** - Do 20-30 at a time  
✓ **Take breaks** - Every 30 minutes  
✓ **Use keyboard** - Minimize mouse use  
✓ **Create standards** - Document your criteria  
✓ **Review periodically** - Check consistency  

### Quality Over Quantity

**Better to have:**
- 300 high-quality, consistent labels
- Than 1000 rushed, inconsistent labels

**Model learns from patterns:**
- Consistent scoring = better learning
- Clear criteria = more accurate predictions

---

**Status:** ✅ Production Ready  
**Interface:** Fully functional  
**API:** Complete  
**Documentation:** Comprehensive  

**Start labeling to create your ML training dataset!** 🎯
