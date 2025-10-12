import { Box, Typography, Radio, RadioGroup, FormControlLabel } from '@mui/material'

interface LikertScaleProps {
  question: string
  value: number
  onChange: (value: number) => void
}

const options = [
  { value: 5, label: 'Kesinlikle Katılıyorum' },
  { value: 4, label: 'Katılıyorum' },
  { value: 3, label: 'Kararsızım' },
  { value: 2, label: 'Katılmıyorum' },
  { value: 1, label: 'Kesinlikle Katılmıyorum' },
]

export default function LikertScale({ question, value, onChange }: LikertScaleProps) {
  return (
    <Box
      sx={{
        p: 3,
        mb: 3,
        bgcolor: 'background.paper',
        borderRadius: 2,
        border: '1px solid',
        borderColor: 'divider',
      }}
    >
      <Typography variant="body1" sx={{ mb: 2, fontWeight: 500 }}>
        {question}
      </Typography>

      <RadioGroup
        value={value}
        onChange={(e) => onChange(parseInt(e.target.value))}
      >
        {options.map((option) => (
          <FormControlLabel
            key={option.value}
            value={option.value}
            control={<Radio />}
            label={option.label}
            sx={{
              '&:hover': {
                bgcolor: 'action.hover',
              },
              borderRadius: 1,
              px: 1,
            }}
          />
        ))}
      </RadioGroup>
    </Box>
  )
}
