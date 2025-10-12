import { useState } from 'react'
import { Container } from '@mui/material'
import Welcome from './components/Welcome'
import ConsentForm from './components/ConsentForm'
import OrthodonticSurvey from './components/OrthodonticSurvey'
import PronunciationTest from './components/PronunciationTest'
import FinishScreen from './components/FinishScreen'

type Step = 'welcome' | 'consent' | 'survey' | 'test' | 'finish'

function App() {
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
    </Container>
  )
}

export default App
