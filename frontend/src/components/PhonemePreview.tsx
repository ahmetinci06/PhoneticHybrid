import { useState } from 'react'
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Alert,
  Divider,
  Chip,
  Card,
  CardContent,
} from '@mui/material'
import MicIcon from '@mui/icons-material/Mic'
import TextFieldsIcon from '@mui/icons-material/TextFields'
import TranslateIcon from '@mui/icons-material/Translate'

interface PhonemeResponse {
  word: string
  phonemes: string
  phoneme_count: number
  language: string
  backend: string
}

interface PhonemeAnalysis {
  word: string
  phonemes: string
  phoneme_list: string[]
  phoneme_count: number
  syllable_estimate: number | null
  language: string
}

export default function PhonemePreview() {
  const [word, setWord] = useState('')
  const [phonemeData, setPhonemeData] = useState<PhonemeResponse | null>(null)
  const [analysis, setAnalysis] = useState<PhonemeAnalysis | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showAnalysis, setShowAnalysis] = useState(false)

  const handleGeneratePhonemes = async () => {
    if (!word.trim()) {
      setError('Lütfen bir kelime giriniz')
      return
    }

    setLoading(true)
    setError('')
    setPhonemeData(null)
    setAnalysis(null)

    try {
      const response = await fetch('http://localhost:8000/phoneme/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          word: word.trim(),
          include_stress: true,
          separator: ' ',
        }),
      })

      if (!response.ok) {
        if (response.status === 503) {
          setError('eSpeak-NG yüklü değil. Fonem servisi kullanılamıyor. Lütfen eSpeak-NG kurun.')
        } else {
          throw new Error('Fonem oluşturma başarısız')
        }
        return
      }

      const data: PhonemeResponse = await response.json()
      setPhonemeData(data)
    } catch (err) {
      if (!error) {
        setError('Bir hata oluştu. Backend çalışıyor mu kontrol edin.')
      }
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleAnalyze = async () => {
    if (!word.trim()) {
      setError('Lütfen bir kelime giriniz')
      return
    }

    setLoading(true)
    setError('')
    setShowAnalysis(true)

    try {
      const response = await fetch('http://localhost:8000/phoneme/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          word: word.trim(),
          include_stress: true,
          separator: ' ',
        }),
      })

      if (!response.ok) {
        if (response.status === 503) {
          setError('eSpeak-NG yüklü değil. Fonem servisi kullanılamıyor. Lütfen eSpeak-NG kurun.')
        } else {
          throw new Error('Fonem analizi başarısız')
        }
        return
      }

      const data: PhonemeAnalysis = await response.json()
      setAnalysis(data)
    } catch (err) {
      if (!error) {
        setError('Analiz yapılamadı. Lütfen tekrar deneyin.')
      }
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleGeneratePhonemes()
    }
  }

  return (
    <Box
      sx={{
        maxWidth: 800,
        mx: 'auto',
        py: 4,
        px: 2,
      }}
    >
      <Paper
        elevation={3}
        sx={{
          p: 4,
          borderRadius: 3,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          mb: 3,
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <TranslateIcon sx={{ fontSize: 40, mr: 2 }} />
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Fonem Önizleyici
          </Typography>
        </Box>
        <Typography variant="body1" sx={{ opacity: 0.9 }}>
          Türkçe kelimelerin IPA (Uluslararası Fonetik Alfabe) fonem dizilerini
          görüntüleyin
        </Typography>
      </Paper>

      <Paper elevation={2} sx={{ p: 4, borderRadius: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
          <TextField
            fullWidth
            label="Türkçe Kelime"
            value={word}
            onChange={(e) => setWord(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Örn: pencere, çocuk, müzik"
            variant="outlined"
            disabled={loading}
            InputProps={{
              startAdornment: <TextFieldsIcon sx={{ mr: 1, color: 'action.active' }} />,
            }}
          />
        </Box>

        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
          <Button
            variant="contained"
            size="large"
            onClick={handleGeneratePhonemes}
            disabled={loading || !word.trim()}
            sx={{ flex: 1, py: 1.5 }}
            startIcon={loading ? <CircularProgress size={20} /> : <MicIcon />}
          >
            {loading ? 'Oluşturuluyor...' : 'Fonem Oluştur'}
          </Button>

          <Button
            variant="outlined"
            size="large"
            onClick={handleAnalyze}
            disabled={loading || !word.trim()}
            sx={{ flex: 1, py: 1.5 }}
          >
            Detaylı Analiz
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mt: 3 }}>
            {error}
          </Alert>
        )}
      </Paper>

      {phonemeData && (
        <Card sx={{ mb: 3, borderRadius: 3 }}>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              Fonem Dizisi
            </Typography>

            <Box
              sx={{
                bgcolor: 'grey.100',
                p: 3,
                borderRadius: 2,
                border: '2px solid',
                borderColor: 'primary.main',
                mb: 3,
              }}
            >
              <Typography
                variant="h4"
                className="ipa-text"
                sx={{
                  textAlign: 'center',
                  color: 'primary.main',
                  fontWeight: 600,
                  letterSpacing: 3,
                  fontSize: '2rem',
                }}
              >
                {phonemeData.phonemes}
              </Typography>
            </Box>

            <Divider sx={{ my: 2 }} />

            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mt: 2 }}>
              <Chip
                label={`Kelime: ${phonemeData.word}`}
                color="primary"
                variant="outlined"
              />
              <Chip
                label={`Fonem Sayısı: ${phonemeData.phoneme_count}`}
                color="secondary"
                variant="outlined"
              />
              <Chip
                label={`Backend: ${phonemeData.backend}`}
                color="default"
                variant="outlined"
              />
              <Chip
                label={`Dil: ${phonemeData.language.toUpperCase()}`}
                color="success"
                variant="outlined"
              />
            </Box>
          </CardContent>
        </Card>
      )}

      {showAnalysis && analysis && (
        <Card sx={{ borderRadius: 3 }}>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              Detaylı Fonem Analizi
            </Typography>

            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                Fonem Listesi:
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 1 }}>
                {analysis.phoneme_list.map((phoneme, index) => (
                  <Chip
                    key={index}
                    label={<span className="ipa-text">{phoneme}</span>}
                    sx={{
                      fontSize: '1.2rem',
                      bgcolor: 'secondary.light',
                      color: 'white',
                      padding: '8px',
                      '& .MuiChip-label': {
                        fontSize: '1.2rem',
                      },
                    }}
                  />
                ))}
              </Box>
            </Box>

            <Divider sx={{ my: 2 }} />

            <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
              <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                <Typography variant="caption" color="text.secondary">
                  Toplam Fonem
                </Typography>
                <Typography variant="h5" sx={{ fontWeight: 600 }}>
                  {analysis.phoneme_count}
                </Typography>
              </Paper>

              <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                <Typography variant="caption" color="text.secondary">
                  Tahmini Hece Sayısı
                </Typography>
                <Typography variant="h5" sx={{ fontWeight: 600 }}>
                  {analysis.syllable_estimate || 'N/A'}
                </Typography>
              </Paper>
            </Box>

            <Box sx={{ mt: 3 }}>
              <Typography variant="caption" color="text.secondary" gutterBottom>
                IPA Gösterimi:
              </Typography>
              <Typography
                variant="h5"
                className="ipa-text"
                sx={{
                  bgcolor: 'grey.900',
                  color: 'white',
                  p: 2,
                  borderRadius: 1,
                  mt: 1,
                  letterSpacing: 2,
                  fontSize: '1.5rem',
                }}
              >
                {analysis.phonemes}
              </Typography>
            </Box>
          </CardContent>
        </Card>
      )}

      <Box sx={{ mt: 4, textAlign: 'center' }}>
        <Typography variant="caption" color="text.secondary">
          eSpeak-NG ile desteklenmektedir • Türkçe (tr) dil modeli
        </Typography>
      </Box>
    </Box>
  )
}
