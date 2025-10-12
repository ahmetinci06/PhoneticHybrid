# eSpeak-NG Windows Installation Guide

## Problem
The phoneme service requires **eSpeak-NG** to be installed on your system to convert Turkish words into IPA phonemes.

**Current Error:**
```
ERROR: espeak not installed on your system
503 Service Unavailable
```

---

## ✅ Solution 1: Direct Download (RECOMMENDED)

### Step 1: Download Installer
1. Go to: https://github.com/espeak-ng/espeak-ng/releases/latest
2. Download: **`espeak-ng-X64.msi`** (for 64-bit Windows)
   - Latest version: 1.51 or higher

### Step 2: Install
1. Run the `.msi` installer
2. Accept the license agreement
3. Click "Next" → "Next" → "Install"
4. Complete installation
5. **Important:** Installer should add eSpeak-NG to PATH automatically

### Step 3: Verify Installation
Open a **NEW** terminal (important!) and run:
```bash
espeak-ng --version
```

**Expected output:**
```
eSpeak NG text-to-speech: 1.51  Data at: C:\Program Files\eSpeak NG
```

### Step 4: Test Turkish Support
```bash
espeak-ng --voices=tr
```

**Expected output:**
```
Pty Language Age/Gender VoiceName          File          Other Languages
 5  tr         --/M       turkish            gmw/tr
```

### Step 5: Restart Backend
```bash
cd backend
python main.py
```

**Expected output:**
```
✓ eSpeak-NG backend initialized for Turkish (tr)
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## ✅ Solution 2: Chocolatey (Requires Admin)

If you have Chocolatey package manager:

```bash
# Run as Administrator
choco install espeak-ng
```

Then verify with `espeak-ng --version`

---

## ✅ Solution 3: WinGet (Windows 10/11)

If you have Windows Package Manager:

```bash
winget install eSpeak-NG.eSpeak-NG
```

Then verify with `espeak-ng --version`

---

## ✅ Solution 4: Scoop

If you have Scoop package manager:

```bash
scoop install espeak-ng
```

Then verify with `espeak-ng --version`

---

## 🔧 Troubleshooting

### Issue 1: "espeak-ng: command not found"

**Cause:** PATH not updated or terminal not restarted

**Solution:**
1. Close ALL terminals
2. Open a NEW terminal
3. Try again: `espeak-ng --version`

If still not working:
1. Search Windows: "Environment Variables"
2. Check System PATH includes: `C:\Program Files\eSpeak NG`
3. If missing, add it manually
4. Restart terminal

### Issue 2: Installation succeeded but backend still fails

**Solution:**
1. Restart the backend server completely
2. Check backend logs for different error
3. Verify phonemizer can find espeak:
   ```python
   python -c "from phonemizer.backend import BACKENDS; print(BACKENDS)"
   ```
   Should include `'espeak'`

### Issue 3: Permission denied during installation

**Solution:**
1. Right-click installer → "Run as Administrator"
2. Try Chocolatey/WinGet with admin rights

### Issue 4: Turkish voices not available

**Solution:**
1. Reinstall eSpeak-NG with default data directory
2. Ensure data directory exists: `C:\Program Files\eSpeak NG\espeak-ng-data`

---

## ✅ Verification Checklist

After installation, verify:

- [ ] `espeak-ng --version` shows version
- [ ] `espeak-ng --voices=tr` shows Turkish voice
- [ ] Backend starts without errors
- [ ] `/phoneme/health` returns `"status": "available"`
- [ ] Frontend shows phonemes (not 503 error)

---

## 🚀 Quick Test After Installation

### Test 1: Command Line
```bash
espeak-ng -v tr "merhaba"
```
Should hear Turkish pronunciation

### Test 2: API Health
```bash
curl http://localhost:8000/phoneme/health
```

**Expected:**
```json
{
  "status": "available",
  "backend": "espeak-ng",
  "language": "tr",
  "version": "1.51"
}
```

### Test 3: Generate Phonemes
```bash
curl -X POST http://localhost:8000/phoneme/generate \
  -H "Content-Type: application/json" \
  -d '{"word": "merhaba"}'
```

**Expected:**
```json
{
  "word": "merhaba",
  "phonemes": "m e ɾ h a b a",
  "phoneme_count": 7,
  "language": "tr",
  "backend": "espeak-ng"
}
```

### Test 4: Frontend UI
1. Open: http://localhost:3000
2. Click "Fonem Önizleyici"
3. Enter: "pencere"
4. Click "Fonem Oluştur"
5. Should see: `p e n d͡ʒ e ɾ e`

---

## 📥 Download Links

- **Main Release:** https://github.com/espeak-ng/espeak-ng/releases/latest
- **Documentation:** https://github.com/espeak-ng/espeak-ng/blob/master/docs/guide.md
- **Windows Installer:** Look for `espeak-ng-X64.msi` (64-bit) or `espeak-ng-X86.msi` (32-bit)

---

## 🔄 Alternative: Work Without eSpeak-NG

If you cannot install eSpeak-NG, the main pronunciation test functionality **still works**. Only the phoneme preview feature will be unavailable.

The backend will show:
```
⚠ eSpeak-NG not available
⚠ Phoneme service will not be available
```

You can:
- ✅ Use the main pronunciation test
- ✅ Record audio
- ✅ Collect data
- ✅ Train ML model
- ❌ Cannot use phoneme preview feature

For phoneme analysis, you can temporarily use:
- https://ipa.typeit.org/ (Online IPA keyboard)
- https://tophonetics.com/ (Online text-to-phoneme converter)

---

## 💡 Tips

1. **Always use NEW terminal** after installation (PATH update)
2. **Run backend from `/backend` directory:** `cd backend && python main.py`
3. **Check logs** for initialization message
4. **Test health endpoint** before using UI
5. **Restart backend** after installing eSpeak-NG

---

## 📞 Still Having Issues?

1. Check backend logs carefully
2. Verify Python version: `python --version` (should be 3.10+)
3. Ensure phonemizer installed: `pip list | grep phonemizer`
4. Try uninstalling and reinstalling eSpeak-NG
5. Check Windows Event Viewer for installation errors

---

**Status:** eSpeak-NG is optional but required for phoneme features
**Priority:** Medium (main app works without it)
**Install Time:** ~5 minutes
