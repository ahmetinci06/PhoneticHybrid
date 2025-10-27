# Phoneme Feature Verification Guide

Complete testing instructions for the Turkish phoneme generation feature.

---

## ✅ Pre-Flight Checklist

Before testing, ensure:

- [ ] **eSpeak-NG installed:** Run `espeak-ng --version`
- [ ] **Backend dependencies installed:** `pip install phonemizer`
- [ ] **Backend running:** http://localhost:8000
- [ ] **Frontend running:** http://localhost:3000

---

## 🧪 Test 1: Backend Health Check

### Command:
```bash
curl http://localhost:8000/phoneme/health
```

### Expected Response:
```json
{
  "status": "available",
  "backend": "espeak-ng",
  "language": "tr",
  "version": "1.51"
}
```

### ✅ Pass Criteria:
- Status is "available"
- Backend shows "espeak-ng"
- Language is "tr"

### ❌ If Failed:
```bash
# Check if eSpeak-NG is installed
espeak-ng --version

# Windows: Install with chocolatey
choco install espeak-ng

# macOS:
brew install espeak

# Linux:
sudo apt-get install espeak-ng

# Restart backend
cd backend
python main.py
```

---

## 🧪 Test 2: Single Word Phoneme Generation (curl)

### Command:
```bash
curl -X POST http://localhost:8000/phoneme/generate \
  -H "Content-Type: application/json" \
  -d '{"word": "pencere"}'
```

### Expected Response:
```json
{
  "word": "pencere",
  "phonemes": "p e n d͡ʒ e ɾ e",
  "phoneme_count": 7,
  "language": "tr",
  "backend": "espeak-ng"
}
```

### ✅ Pass Criteria:
- Word matches input
- Phonemes is non-empty string
- Phoneme count > 0
- Contains IPA characters (d͡ʒ, ɾ, etc.)

---

## 🧪 Test 3: Multiple Words (Batch)

### Command:
```bash
curl -X POST http://localhost:8000/phoneme/batch \
  -H "Content-Type: application/json" \
  -d '["araba", "bahçe", "çocuk"]'
```

### Expected Response:
```json
[
  {
    "word": "araba",
    "phonemes": "a ɾ a b a",
    "phoneme_count": 5,
    "language": "tr",
    "backend": "espeak-ng"
  },
  {
    "word": "bahçe",
    "phonemes": "b a h t͡ʃ e",
    "phoneme_count": 5,
    "language": "tr",
    "backend": "espeak-ng"
  },
  {
    "word": "çocuk",
    "phonemes": "t͡ʃ o d͡ʒ u k",
    "phoneme_count": 5,
    "language": "tr",
    "backend": "espeak-ng"
  }
]
```

### ✅ Pass Criteria:
- Returns array with 3 items
- Each item has word, phonemes, phoneme_count
- All phoneme strings are non-empty

---

## 🧪 Test 4: Detailed Analysis

### Command:
```bash
curl -X POST http://localhost:8000/phoneme/analyze \
  -H "Content-Type: application/json" \
  -d '{"word": "üniversite"}'
```

### Expected Response:
```json
{
  "word": "üniversite",
  "phonemes": "y n i v e ɾ s i t e",
  "phoneme_list": ["y", "n", "i", "v", "e", "ɾ", "s", "i", "t", "e"],
  "phoneme_count": 10,
  "syllable_estimate": 5,
  "language": "tr"
}
```

### ✅ Pass Criteria:
- phoneme_list is an array
- phoneme_count equals length of phoneme_list
- syllable_estimate is a positive number
- Syllable estimate is reasonable (typically 2-5 for Turkish words)

---

## 🧪 Test 5: Frontend UI Testing

### Steps:

1. **Open Frontend:**
   - Navigate to http://localhost:3000
   - Should see Welcome screen

2. **Switch to Phoneme Mode:**
   - Click "Fonem Önizleyici" button
   - Should navigate to phoneme interface

3. **Test Input:**
   - Enter word: "telefon"
   - Click "Fonem Oluştur"
   - Should see loading indicator

4. **Verify Output:**
   - Phoneme display box should appear
   - Should show: "t e l e f o n" (or similar IPA)
   - Should show chips with:
     - Kelime: telefon
     - Fonem Sayısı: [number]
     - Backend: espeak-ng
     - Dil: TR

5. **Test Detailed Analysis:**
   - Click "Detaylı Analiz" button
   - Should show:
     - Individual phoneme chips
     - Total phoneme count
     - Syllable estimate
     - IPA display in dark box

### ✅ Pass Criteria:
- No console errors
- Phonemes display correctly
- UI is responsive
- All chips render properly
- Analysis section shows when clicked

### Screenshot Verification:
- [ ] Gradient header visible
- [ ] Input field works
- [ ] Buttons are clickable
- [ ] Phoneme display is monospace font
- [ ] Chips have correct colors

---

## 🧪 Test 6: Error Handling

### Test 6.1: Empty Word

```bash
curl -X POST http://localhost:8000/phoneme/generate \
  -H "Content-Type: application/json" \
  -d '{"word": ""}'
```

**Expected:** Status 400, error message "Word cannot be empty"

### Test 6.2: Backend Not Running

1. Stop backend server
2. Try generating phonemes in frontend
3. **Expected:** Error message "Bir hata oluştu. Backend çalışıyor mu kontrol edin."

### Test 6.3: Invalid JSON

```bash
curl -X POST http://localhost:8000/phoneme/generate \
  -H "Content-Type: application/json" \
  -d 'invalid json'
```

**Expected:** Status 422, validation error

---

## 🧪 Test 7: API Documentation

### Command:
```bash
open http://localhost:8000/docs
```

### Verify:
- [ ] Swagger UI loads
- [ ] `/phoneme/generate` endpoint visible
- [ ] `/phoneme/analyze` endpoint visible
- [ ] `/phoneme/batch` endpoint visible
- [ ] `/phoneme/health` endpoint visible
- [ ] Can test endpoints directly in Swagger UI

### Try Interactive Test:
1. Click `/phoneme/generate`
2. Click "Try it out"
3. Enter: `{"word": "merhaba"}`
4. Click "Execute"
5. Should see 200 response with phonemes

---

## 🧪 Test 8: Python Integration

### Test Script:
```python
import requests

# Test connection
response = requests.get('http://localhost:8000/phoneme/health')
print(f"✓ Health Check: {response.json()['status']}")

# Test single word
response = requests.post(
    'http://localhost:8000/phoneme/generate',
    json={'word': 'kitap'}
)
data = response.json()
print(f"✓ Word: {data['word']}")
print(f"✓ Phonemes: {data['phonemes']}")
print(f"✓ Count: {data['phoneme_count']}")

# Test batch
response = requests.post(
    'http://localhost:8000/phoneme/batch',
    json=['masa', 'sandalye', 'pencere']
)
batch_data = response.json()
print(f"✓ Batch processed: {len(batch_data)} words")

for item in batch_data:
    print(f"  - {item['word']}: {item['phonemes']}")

print("\n✅ All Python tests passed!")
```

### Run:
```bash
python test_phoneme_api.py
```

### ✅ Expected Output:
```
✓ Health Check: available
✓ Word: kitap
✓ Phonemes: k i t a p
✓ Count: 5
✓ Batch processed: 3 words
  - masa: m a s a
  - sandalye: s a n d a l j e
  - pencere: p e n d͡ʒ e ɾ e

✅ All Python tests passed!
```

---

## 🧪 Test 9: Performance Testing

### Single Word Latency:
```bash
time curl -X POST http://localhost:8000/phoneme/generate \
  -H "Content-Type: application/json" \
  -d '{"word": "bilgisayar"}'
```

**Expected:** < 200ms

### Batch Performance:
```bash
time curl -X POST http://localhost:8000/phoneme/batch \
  -H "Content-Type: application/json" \
  -d '["word1", "word2", "word3", "word4", "word5"]'
```

**Expected:** < 500ms for 5 words

---

## 🧪 Test 10: Integration with Existing System

### Verify No Conflicts:

1. **Test Main Flow Still Works:**
   ```bash
   # From homepage
   # Click "Telaffuz Testi" (not Phoneme Preview)
   # Should proceed to consent form normally
   ```

2. **Test Mode Switching:**
   ```bash
   # Start on Welcome screen
   # Click "Fonem Önizleyici"
   # Click "← Ana Sayfaya Dön"
   # Should return to Welcome screen
   # Click "Başlamak İçin Tıklayın"
   # Should start normal test flow
   ```

3. **Test API Coexistence:**
   ```bash
   # Register participant still works
   curl -X POST http://localhost:8000/register \
     -H "Content-Type: application/json" \
     -d '{"name": "Test", "age": 25, "gender": "Erkek", "consent": true}'
   
   # Phoneme API still works
   curl -X POST http://localhost:8000/phoneme/generate \
     -H "Content-Type: application/json" \
     -d '{"word": "test"}'
   ```

### ✅ Pass Criteria:
- Both APIs work independently
- No CORS errors
- No route conflicts
- Frontend navigation smooth

---

## 📊 Verification Checklist

### Backend:
- [ ] `/phoneme/health` returns 200
- [ ] `/phoneme/generate` works for single word
- [ ] `/phoneme/analyze` returns detailed data
- [ ] `/phoneme/batch` processes multiple words
- [ ] Error handling works (empty word, invalid JSON)
- [ ] API docs show phoneme endpoints
- [ ] No console errors or warnings

### Frontend:
- [ ] Phoneme Preview component renders
- [ ] Input field accepts Turkish characters
- [ ] "Fonem Oluştur" button works
- [ ] Phoneme display shows IPA characters
- [ ] "Detaylı Analiz" button works
- [ ] Analysis section shows all data
- [ ] Mode switching works (Test ↔ Phoneme)
- [ ] No React errors in console
- [ ] UI is responsive on mobile

### Integration:
- [ ] Phoneme API doesn't break existing endpoints
- [ ] Main test flow still works
- [ ] CORS configured correctly
- [ ] Documentation updated

### Performance:
- [ ] Single word < 200ms
- [ ] Batch processing reasonable
- [ ] No memory leaks
- [ ] Frontend smooth animations

---

## 🎉 Success Criteria

All tests pass when:

✅ Backend health check returns "available"  
✅ Phonemes generated for Turkish words  
✅ IPA characters display correctly  
✅ Frontend UI renders without errors  
✅ Batch processing works  
✅ Analysis shows syllable estimates  
✅ Error handling graceful  
✅ Performance within acceptable limits  
✅ Existing features unaffected  

---

## 🐛 Common Issues & Solutions

### Issue: "Backend not available"
**Solution:** Install eSpeak-NG and restart backend

### Issue: "CORS error in browser"
**Solution:** Ensure backend allows localhost:3000

### Issue: "Phonemes look wrong"
**Solution:** Verify Turkish language: `espeak-ng --voices=tr`

### Issue: "Frontend doesn't connect"
**Solution:** Check backend is running on port 8000

### Issue: "Module not found: phonemizer"
**Solution:** `pip install phonemizer`

---

## 📸 Visual Verification

Expected UI appearance:

1. **Header:** Purple gradient with "Fonem Önizleyici" title
2. **Input:** White text field with icon
3. **Phoneme Display:** Large monospace text in bordered box
4. **Chips:** Colorful chips for metadata
5. **Analysis:** Grid layout with phoneme chips

---

## 🚀 Next Steps After Verification

Once all tests pass:

1. ✅ Feature is production-ready
2. 📝 Document any edge cases found
3. 🎯 Consider adding to ML training pipeline
4. 📊 Monitor usage and performance
5. 🔄 Plan future enhancements

---

**Verification Status:** Ready to test!
