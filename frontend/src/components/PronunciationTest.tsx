import { useState, useRef, useEffect } from 'react'
import {
  Box,
  Typography,
  Button,
  Paper,
  LinearProgress,
  Alert,
  CircularProgress,
  Card,
  CardContent,
} from '@mui/material'
import MicIcon from '@mui/icons-material/Mic'
import StopIcon from '@mui/icons-material/Stop'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'

interface PronunciationTestProps {
  participantId: string
  onComplete: () => void
}

const turkishWords = [
  'araba', 'bahçe', 'çocuk', 'diş', 'elma',
  'futbol', 'güneş', 'havuç', 'ışık', 'jimnastik',
  'karpuz', 'limon', 'masa', 'nane', 'okul',
  'para', 'radyo', 'sandalye', 'şapka', 'tiyatro',
  'üzüm', 'vişne', 'yarış', 'zaman', 'gözlük',
  'kahve', 'defter', 'müzik', 'pencere', 'çanta',
]

export default function PronunciationTest({
  participantId,
  onComplete,
}: PronunciationTestProps) {
  const [started, setStarted] = useState(false)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isRecording, setIsRecording] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [results, setResults] = useState<any[]>([])
  const [error, setError] = useState('')

  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])

  const currentWord = turkishWords[currentIndex]
  const progress = (currentIndex / turkishWords.length) * 100

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)

      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
        await uploadAudio(audioBlob)
        stream.getTracks().forEach((track) => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
      setError('')
    } catch (err) {
      setError('Mikrofon erişimi reddedildi. Lütfen izin verin.')
      console.error(err)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const uploadAudio = async (audioBlob: Blob) => {
    setIsUploading(true)

    try {
      const formData = new FormData()
      formData.append('participant_id', participantId)
      formData.append('word', currentWord)
      formData.append('word_index', currentIndex.toString())
      formData.append('audio', audioBlob, `${currentWord}.wav`)

      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Yükleme başarısız')
      }

      const result = await response.json()
      setResults([...results, result])

      // Move to next word
      if (currentIndex < turkishWords.length - 1) {
        setCurrentIndex(currentIndex + 1)
      } else {
        // Test complete
        setTimeout(() => onComplete(), 1000)
      }
    } catch (err) {
      setError('Yükleme hatası. Lütfen tekrar deneyin.')
      console.error(err)
    } finally {
      setIsUploading(false)
    }
  }

  if (!started) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '70vh',
        }}
      >
        <Paper elevation={3} sx={{ p: 6, textAlign: 'center', borderRadius: 3 }}>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
            Telaffuz Testine Hazır mısınız?
          </Typography>

          <Typography variant="body1" color="text.secondary" paragraph sx={{ mt: 2 }}>
            Size gösterilecek {turkishWords.length} kelimeyi sesli olarak okuyacaksınız.
            Her kelime için:
          </Typography>

          <Box
            component="ul"
            sx={{ textAlign: 'left', maxWidth: 400, mx: 'auto', mt: 3 }}
          >
            <li>
              <Typography variant="body2">
                Kelimeyi ekranda göreceksiniz
              </Typography>
            </li>
            <li>
              <Typography variant="body2">
                "Kaydet" butonuna basın ve kelimeyi okuyun
              </Typography>
            </li>
            <li>
              <Typography variant="body2">
                "Dur" butonuna basarak kaydı bitirin
              </Typography>
            </li>
            <li>
              <Typography variant="body2">
                Otomatik olarak bir sonraki kelimeye geçilir
              </Typography>
            </li>
          </Box>

          <Button
            variant="contained"
            size="large"
            onClick={() => setStarted(true)}
            sx={{ mt: 4, py: 2, px: 6, textTransform: 'none', fontSize: '1.1rem' }}
          >
            Teste Başla
          </Button>
        </Paper>
      </Box>
    )
  }

  return (
    <Box sx={{ maxWidth: 700, mx: 'auto', py: 4 }}>
      <Paper elevation={2} sx={{ p: 4, borderRadius: 3 }}>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
          Telaffuz Testi
        </Typography>

        <Box sx={{ mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="caption" color="text.secondary">
              İlerleme
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {currentIndex + 1} / {turkishWords.length}
            </Typography>
          </Box>
          <LinearProgress variant="determinate" value={progress} />
        </Box>

        <Card
          sx={{
            mt: 4,
            mb: 4,
            bgcolor: 'primary.main',
            color: 'white',
            textAlign: 'center',
            py: 6,
          }}
        >
          <CardContent>
            <Typography variant="h2" sx={{ fontWeight: 700 }}>
              {currentWord}
            </Typography>
          </CardContent>
        </Card>

        <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
          {!isRecording && !isUploading && (
            <Button
              variant="contained"
              size="large"
              startIcon={<MicIcon />}
              onClick={startRecording}
              sx={{ py: 2, px: 6, textTransform: 'none', fontSize: '1rem' }}
            >
              Kaydet
            </Button>
          )}

          {isRecording && (
            <Button
              variant="contained"
              color="error"
              size="large"
              startIcon={<StopIcon />}
              onClick={stopRecording}
              sx={{ py: 2, px: 6, textTransform: 'none', fontSize: '1rem' }}
            >
              Dur
            </Button>
          )}

          {isUploading && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <CircularProgress size={24} />
              <Typography>Yükleniyor...</Typography>
            </Box>
          )}
        </Box>

        {error && (
          <Alert severity="error" sx={{ mt: 3 }}>
            {error}
          </Alert>
        )}

        {results.length > 0 && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              Son Sonuç:
            </Typography>
            <Paper sx={{ p: 2, bgcolor: 'success.light', color: 'white' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <CheckCircleIcon />
                <Typography>
                  {results[results.length - 1].word} -{' '}
                  {results[results.length - 1].feedback}
                </Typography>
              </Box>
            </Paper>
          </Box>
        )}
      </Paper>
    </Box>
  )
}
