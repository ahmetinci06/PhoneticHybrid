# Backend API Documentation

## Overview

FastAPI backend for Turkish pronunciation analysis with ML inference.

## API Endpoints

### Health Check
```
GET /
```
Returns service status and model loading state.

### Register Participant
```
POST /register
Content-Type: application/json

{
  "name": "string",
  "age": integer,
  "gender": "string",
  "consent": boolean
}
```

### Save Survey
```
POST /survey
Content-Type: application/json

{
  "participant_id": "string",
  "responses": [1, 2, 3, 4, 5, ...]
}
```

### Upload Audio
```
POST /upload
Content-Type: multipart/form-data

participant_id: string
word: string
word_index: integer
audio: file (wav)
```

## Running

```bash
# Development
python main.py

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Dependencies

See `requirements.txt` for full list.
