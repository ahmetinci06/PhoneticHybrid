import { Box, Typography, Button, Paper } from '@mui/material'
import RecordVoiceOverIcon from '@mui/icons-material/RecordVoiceOver'

interface WelcomeProps {
  onNext: () => void
}

export default function Welcome({ onNext }: WelcomeProps) {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '80vh',
        textAlign: 'center',
      }}
    >
      <Paper
        elevation={3}
        sx={{
          p: 6,
          borderRadius: 4,
          maxWidth: 600,
          width: '100%',
        }}
      >
        <RecordVoiceOverIcon
          sx={{
            fontSize: 80,
            color: 'primary.main',
            mb: 3,
          }}
        />
        
        <Typography
          variant="h2"
          component="h1"
          gutterBottom
          sx={{
            fontWeight: 700,
            background: 'linear-gradient(45deg, #2563eb 30%, #7c3aed 90%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          PhoneticHybrid
        </Typography>
        
        <Typography
          variant="h5"
          color="text.secondary"
          paragraph
          sx={{ mb: 4 }}
        >
          Türkçe Telaffuz Analiz Platformu
        </Typography>
        
        <Typography
          variant="body1"
          color="text.secondary"
          paragraph
          sx={{ mb: 4 }}
        >
          Bu araştırma, Türkçe telaffuz kalitesini değerlendirmek için
          geliştirilmiş yapay zeka tabanlı bir platformdur. Lütfen 30 kelimeyi
          sesli olarak okuyunuz.
        </Typography>
        
        <Button
          variant="contained"
          size="large"
          onClick={onNext}
          sx={{
            py: 2,
            px: 6,
            fontSize: '1.1rem',
            borderRadius: 3,
            textTransform: 'none',
          }}
        >
          Başlamak İçin Tıklayın
        </Button>
      </Paper>
    </Box>
  )
}
