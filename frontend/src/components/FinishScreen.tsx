import { Box, Typography, Button, Paper } from '@mui/material'
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline'

interface FinishScreenProps {
  onRestart: () => void
}

export default function FinishScreen({ onRestart }: FinishScreenProps) {
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
        <CheckCircleOutlineIcon
          sx={{
            fontSize: 100,
            color: 'success.main',
            mb: 3,
          }}
        />

        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          sx={{ fontWeight: 700, color: 'success.main' }}
        >
          Tebrikler!
        </Typography>

        <Typography variant="h5" color="text.secondary" paragraph sx={{ mb: 3 }}>
          Testi Başarıyla Tamamladınız
        </Typography>

        <Typography variant="body1" color="text.secondary" paragraph>
          Katılımınız için teşekkür ederiz. Telaffuz kayıtlarınız başarıyla
          kaydedildi ve analiz edildi.
        </Typography>

        <Typography variant="body2" color="text.secondary" paragraph sx={{ mb: 4 }}>
          Verileriniz güvenli bir şekilde saklanacak ve sadece bilimsel araştırma
          amaçlı kullanılacaktır.
        </Typography>

        <Button
          variant="outlined"
          size="large"
          onClick={onRestart}
          sx={{
            mt: 2,
            py: 1.5,
            px: 4,
            textTransform: 'none',
            fontSize: '1rem',
          }}
        >
          Ana Sayfaya Dön
        </Button>
      </Paper>
    </Box>
  )
}
