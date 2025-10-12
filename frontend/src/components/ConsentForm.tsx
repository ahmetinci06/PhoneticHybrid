import { useState } from 'react'
import {
  Box,
  Typography,
  TextField,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Checkbox,
  Button,
  Paper,
  Alert,
} from '@mui/material'

interface ConsentFormProps {
  onComplete: (participantId: string) => void
}

export default function ConsentForm({ onComplete }: ConsentFormProps) {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    gender: '',
    consent: false,
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    // Validation
    if (!formData.name.trim()) {
      setError('Lütfen adınızı giriniz')
      return
    }
    if (!formData.age || parseInt(formData.age) < 1 || parseInt(formData.age) > 120) {
      setError('Lütfen geçerli bir yaş giriniz')
      return
    }
    if (!formData.gender) {
      setError('Lütfen cinsiyetinizi seçiniz')
      return
    }
    if (!formData.consent) {
      setError('Devam etmek için onay vermelisiniz')
      return
    }

    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formData.name,
          age: parseInt(formData.age),
          gender: formData.gender,
          consent: formData.consent,
        }),
      })

      if (!response.ok) {
        throw new Error('Kayıt başarısız')
      }

      const data = await response.json()
      onComplete(data.participant_id)
    } catch (err) {
      setError('Bir hata oluştu. Lütfen tekrar deneyin.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box sx={{ maxWidth: 700, mx: 'auto', py: 4 }}>
      <Paper elevation={2} sx={{ p: 4, borderRadius: 3 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
          KVKK & Kişisel Bilgiler
        </Typography>

        <Typography variant="body2" color="text.secondary" paragraph>
          Lütfen aşağıdaki formu doldurunuz. Verileriniz gizli tutulacaktır.
        </Typography>

        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <TextField
            fullWidth
            label="Ad Soyad"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            margin="normal"
            required
          />

          <TextField
            fullWidth
            label="Yaş"
            type="number"
            value={formData.age}
            onChange={(e) => setFormData({ ...formData, age: e.target.value })}
            margin="normal"
            required
            inputProps={{ min: 1, max: 120 }}
          />

          <FormControl component="fieldset" margin="normal" fullWidth>
            <FormLabel component="legend">Cinsiyet</FormLabel>
            <RadioGroup
              row
              value={formData.gender}
              onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
            >
              <FormControlLabel value="Kadın" control={<Radio />} label="Kadın" />
              <FormControlLabel value="Erkek" control={<Radio />} label="Erkek" />
              <FormControlLabel value="Diğer" control={<Radio />} label="Diğer" />
            </RadioGroup>
          </FormControl>

          <Box
            sx={{
              mt: 3,
              p: 3,
              bgcolor: 'grey.50',
              borderRadius: 2,
              border: '1px solid',
              borderColor: 'grey.300',
            }}
          >
            <Typography variant="h6" gutterBottom>
              KVKK Aydınlatma Metni
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Bu araştırma kapsamında toplanan ses kayıtları ve kişisel
              verileriniz sadece bilimsel araştırma amaçlı kullanılacak, üçüncü
              kişilerle paylaşılmayacaktır. Verileriniz şifreli olarak
              saklanacaktır.
            </Typography>

            <FormControlLabel
              control={
                <Checkbox
                  checked={formData.consent}
                  onChange={(e) =>
                    setFormData({ ...formData, consent: e.target.checked })
                  }
                />
              }
              label="KVKK metnini okudum ve kabul ediyorum"
            />
          </Box>

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}

          <Button
            type="submit"
            variant="contained"
            size="large"
            fullWidth
            disabled={loading}
            sx={{ mt: 3, py: 1.5, textTransform: 'none', fontSize: '1rem' }}
          >
            {loading ? 'Kaydediliyor...' : 'Devam Et'}
          </Button>
        </Box>
      </Paper>
    </Box>
  )
}
