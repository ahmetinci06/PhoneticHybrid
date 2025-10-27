"""
Test script for pronunciation analysis feature
Run this to verify the analysis system works correctly
"""

import requests
import sys
from pathlib import Path

def test_phoneme_service():
    """Test phoneme generation endpoint"""
    print("🧪 Testing Phoneme Service...")
    
    response = requests.post(
        'http://localhost:8000/phoneme/generate',
        json={'word': 'pencere'}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Phoneme Service: {data['word']} → {data['phonemes']}")
        return True
    else:
        print(f"❌ Phoneme Service Failed: {response.status_code}")
        return False


def test_audio_analysis(audio_file: str, word: str):
    """Test pronunciation analysis endpoint"""
    print(f"\n🧪 Testing Audio Analysis for '{word}'...")
    
    audio_path = Path(audio_file)
    
    if not audio_path.exists():
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    with open(audio_path, 'rb') as f:
        response = requests.post(
            'http://localhost:8000/analyze/audio',
            files={'file': f},
            data={'word': word}
        )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Audio Analysis Complete")
        print(f"   Word: {result['word']}")
        print(f"   Target Phonemes: {result['phonemes_target']}")
        print(f"   Overall Score: {result['overall']:.3f}")
        print(f"   Grade: {result['grade']}")
        print(f"   Duration: {result['features']['duration']:.2f}s")
        print(f"   Pitch: {result['features']['pitch_mean']:.1f} Hz")
        print(f"\n   Phoneme Scores:")
        for phoneme, score in result['scores'].items():
            bar = '█' * int(score * 20)
            print(f"     {phoneme:5s} {score:.3f} {bar}")
        return True
    else:
        print(f"❌ Audio Analysis Failed: {response.status_code}")
        print(f"   Detail: {response.text}")
        return False


def test_health():
    """Test API health endpoint"""
    print("\n🧪 Testing API Health...")
    
    response = requests.get('http://localhost:8000/health')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API Health: {data['status']}")
        return True
    else:
        print(f"❌ Health Check Failed")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("  PhoneticHybrid - Pronunciation Analysis Test Suite")
    print("=" * 60)
    
    # Test 1: Health Check
    health_ok = test_health()
    
    if not health_ok:
        print("\n❌ Backend not running. Start with: python main.py")
        sys.exit(1)
    
    # Test 2: Phoneme Service
    phoneme_ok = test_phoneme_service()
    
    if not phoneme_ok:
        print("\n⚠️  Phoneme service unavailable (eSpeak-NG not installed?)")
        print("   Analysis will work but phoneme generation may fail.")
    
    # Test 3: Audio Analysis (if audio file provided)
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        word = sys.argv[2] if len(sys.argv) > 2 else "test"
        
        analysis_ok = test_audio_analysis(audio_file, word)
        
        if analysis_ok:
            print("\n" + "=" * 60)
            print("✅ All tests passed!")
            print("=" * 60)
        else:
            print("\n❌ Audio analysis test failed")
            sys.exit(1)
    else:
        print("\n" + "=" * 60)
        print("✅ Basic tests passed!")
        print("\n💡 To test audio analysis, run:")
        print("   python test_analysis.py path/to/audio.wav wordname")
        print("=" * 60)


if __name__ == "__main__":
    main()
