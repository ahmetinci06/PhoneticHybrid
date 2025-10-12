import { useState } from 'react'
import { Box, Typography, Button, Paper, Alert, LinearProgress } from '@mui/material'
import LikertScale from './LikertScale'

interface OrthodonticSurveyProps {
  participantId: string
  onComplete: () => void
}

const surveyQuestions = [
  'Ortodontik tedavilerin amacını biliyorum',
  'Tel tedavisinin nasıl çalıştığını anlıyorum',
  'Şeffaf plak (invisalign) tedavisini duydum',
  'Ortodonti uzmanı ile diş hekiminin farkını biliyorum',
  'Ortodontik tedavilerin yan etkilerini biliyorum',
  'Ortodontik cihazların hijyenine dikkat etmenin önemini biliyorum',
  'Tedavi sonrası pekiştirme (retainer) kullanımının gerekliliğini biliyorum',
  'Erken yaşta ortodontik müdahalenin önemini biliyorum',
]

export default function OrthodonticSurvey({
  participantId,
  onComplete,
}: OrthodonticSurveyProps) {
  const [responses, setResponses] = useState<number[]>(
    new Array(surveyQuestions.length).fill(0)
  )
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleResponseChange = (index: number, value: number) => {
    const newResponses = [...responses]
    newResponses[index] = value
    setResponses(newResponses)
  }

  const handleSubmit = async () => {
    // Validation
    if (responses.some((r) => r === 0)) {
      setError('Lütfen tüm soruları cevaplayınız')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await fetch('http://localhost:8000/survey', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          participant_id: participantId,
          responses: responses,
        }),
      })

      if (!response.ok) {
        throw new Error('Anket kaydedilemedi')
      }

      onComplete()
    } catch (err) {
      setError('Bir hata oluştu. Lütfen tekrar deneyin.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const answeredCount = responses.filter((r) => r !== 0).length
  const progress = (answeredCount / surveyQuestions.length) * 100

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', py: 4 }}>
      <Paper elevation={2} sx={{ p: 4, borderRadius: 3 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
          Ortodontik Bilgi Anketi
        </Typography>

        <Typography variant="body2" color="text.secondary" paragraph>
          Lütfen aşağıdaki ifadeleri değerlendiriniz.
        </Typography>

        <Box sx={{ mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="caption" color="text.secondary">
              İlerleme
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {answeredCount} / {surveyQuestions.length}
            </Typography>
          </Box>
          <LinearProgress variant="determinate" value={progress} />
        </Box>

        <Box sx={{ mt: 4 }}>
          {surveyQuestions.map((question, index) => (
            <LikertScale
              key={index}
              question={`${index + 1}. ${question}`}
              value={responses[index]}
              onChange={(value) => handleResponseChange(index, value)}
            />
          ))}
        </Box>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        <Button
          variant="contained"
          size="large"
          fullWidth
          onClick={handleSubmit}
          disabled={loading || answeredCount < surveyQuestions.length}
          sx={{ mt: 3, py: 1.5, textTransform: 'none', fontSize: '1rem' }}
        >
          {loading ? 'Kaydediliyor...' : 'Anketi Tamamla'}
        </Button>
      </Paper>
    </Box>
  )
}
