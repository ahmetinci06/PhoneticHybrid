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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
} from '@mui/material'
import MicIcon from '@mui/icons-material/Mic'
import StopIcon from '@mui/icons-material/Stop'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import { turkishWords } from '../config/words'

interface PronunciationTestProps {
  participantId: string
  onComplete: () => void
}

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
      formData.append('file', audioBlob, `${currentWord}.wav`)
      formData.append('word', currentWord)

      // Use Whisper-based analysis endpoint
      const response = await fetch('http://localhost:8000/analyze', {
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
            <Paper sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <CheckCircleIcon color="success" />
                <Typography variant="h6">
                  {results[results.length - 1].word}
                </Typography>
                <Chip 
                  label={results[results.length - 1].grade || 'N/A'} 
                  color="primary" 
                  size="small"
                />
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Tanınan Metin: <strong>{results[results.length - 1].recognized_text || 'N/A'}</strong>
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Genel Skor: <strong>{((results[results.length - 1].overall || 0) * 100).toFixed(1)}%</strong>
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Güven Skoru: <strong>{((results[results.length - 1].recognition_confidence || 0) * 100).toFixed(1)}%</strong>
                </Typography>
              </Box>

              {results[results.length - 1].segment_scores && 
               Object.keys(results[results.length - 1].segment_scores).length > 0 && (
                <>
                  <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                    Fonem Skorları:
                  </Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Fonem</TableCell>
                          <TableCell align="right">Skor</TableCell>
                          <TableCell align="right">Görsel</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {Object.entries(results[results.length - 1].segment_scores).map(
                          ([phoneme, score]: [string, any]) => (
                            <TableRow key={phoneme}>
                              <TableCell>
                                <span className="ipa-text" style={{ fontSize: '1.1rem' }}>
                                  {phoneme}
                                </span>
                              </TableCell>
                              <TableCell align="right">
                                {(score * 100).toFixed(1)}%
                              </TableCell>
                              <TableCell align="right">
                                <Box
                                  sx={{
                                    width: '100%',
                                    height: 8,
                                    bgcolor: 'grey.200',
                                    borderRadius: 1,
                                    overflow: 'hidden',
                                  }}
                                >
                                  <Box
                                    sx={{
                                      width: `${score * 100}%`,
                                      height: '100%',
                                      bgcolor: score >= 0.8 ? 'success.main' : score >= 0.6 ? 'warning.main' : 'error.main',
                                    }}
                                  />
                                </Box>
                              </TableCell>
                            </TableRow>
                          )
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </>
              )}
            </Paper>
          </Box>
        )}
      </Paper>
    </Box>
  )
}
