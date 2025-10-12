import { useState } from 'react'
import { Container, Box, Button, ButtonGroup } from '@mui/material'
import Welcome from './components/Welcome'
import ConsentForm from './components/ConsentForm'
import OrthodonticSurvey from './components/OrthodonticSurvey'
import PronunciationTest from './components/PronunciationTest'
import FinishScreen from './components/FinishScreen'
import PhonemePreview from './components/PhonemePreview'

type Step = 'welcome' | 'consent' | 'survey' | 'test' | 'finish'
type Mode = 'main' | 'phoneme'

function App() {
  const [mode, setMode] = useState<Mode>('main')
  const [step, setStep] = useState<Step>('welcome')
  const [participantId, setParticipantId] = useState<string>('')

  const handleWelcomeNext = () => {
    setStep('consent')
  }

  const handleConsentComplete = (id: string) => {
    setParticipantId(id)
    setStep('survey')
  }

  const handleSurveyComplete = () => {
    setStep('test')
  }

  const handleTestComplete = () => {
    setStep('finish')
  }

  const handleRestart = () => {
    setStep('welcome')
    setParticipantId('')
  }

  return (
    <Container maxWidth="lg" sx={{ minHeight: '100vh', py: 4 }}>
      {/* Mode Selector - Only show on welcome screen */}
      {step === 'welcome' && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
          <ButtonGroup variant="outlined" size="large">
            <Button
              variant={mode === 'main' ? 'contained' : 'outlined'}
              onClick={() => setMode('main')}
            >
              Telaffuz Testi
            </Button>
            <Button
              variant={mode === 'phoneme' ? 'contained' : 'outlined'}
              onClick={() => setMode('phoneme')}
            >
              Fonem Önizleyici
            </Button>
          </ButtonGroup>
        </Box>
      )}

      {/* Phoneme Preview Mode */}
      {mode === 'phoneme' && (
        <>
          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
            <Button variant="outlined" onClick={() => setMode('main')}>
              ← Ana Sayfaya Dön
            </Button>
          </Box>
          <PhonemePreview />
        </>
      )}

      {/* Main Test Flow */}
      {mode === 'main' && (
        <>
          {step === 'welcome' && <Welcome onNext={handleWelcomeNext} />}
          {step === 'consent' && <ConsentForm onComplete={handleConsentComplete} />}
          {step === 'survey' && (
            <OrthodonticSurvey
              participantId={participantId}
              onComplete={handleSurveyComplete}
            />
          )}
          {step === 'test' && (
            <PronunciationTest
              participantId={participantId}
              onComplete={handleTestComplete}
            />
          )}
          {step === 'finish' && <FinishScreen onRestart={handleRestart} />}
        </>
      )}
    </Container>
  )
}

export default App
