# Deployment Guide

## Production Deployment

### Backend (FastAPI)

#### Option 1: Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
cd backend
railway init

# Deploy
railway up
```

#### Option 2: Render

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: phoneizer-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Connect GitHub repo to Render
3. Deploy automatically on push

#### Option 3: DigitalOcean App Platform

```bash
# Create Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (React)

#### Option 1: Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel
```

#### Option 2: Netlify

```bash
# Build
npm run build

# Deploy dist/ folder via Netlify UI
```

#### Option 3: Cloudflare Pages

```bash
# Build command: npm run build
# Output directory: dist
# Connect GitHub repo to Cloudflare Pages
```

## Environment Variables

### Backend

Create `.env` file:
```
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend-domain.com
```

### Frontend

Create `.env.production`:
```
VITE_API_URL=https://your-backend-domain.com
```

Update `vite.config.ts` to use env variable:
```typescript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: import.meta.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

## Security Checklist

- [ ] Enable HTTPS (SSL/TLS certificates)
- [ ] Add rate limiting
- [ ] Implement authentication
- [ ] Sanitize file uploads
- [ ] Set proper CORS origins
- [ ] Add request validation
- [ ] Enable logging and monitoring
- [ ] Use environment variables for secrets
- [ ] Implement data encryption at rest
- [ ] Add backup strategy for participant data

## Performance Optimization

### Backend
- Use gunicorn with multiple workers
- Enable compression middleware
- Implement caching for static responses
- Optimize model loading (singleton pattern)
- Add request timeouts

### Frontend
- Enable code splitting
- Optimize bundle size
- Use lazy loading for components
- Compress images and assets
- Implement service worker for offline support
- Enable CDN for static assets

## Monitoring

### Backend Monitoring

```python
# Add to main.py
from fastapi import Request
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url} - {process_time:.2f}s")
    return response
```

### Recommended Tools
- **Backend:** Sentry, DataDog, New Relic
- **Frontend:** Google Analytics, Sentry
- **Infrastructure:** UptimeRobot, Pingdom

## Scaling

### Horizontal Scaling (Multiple Instances)
```bash
# Use load balancer (nginx, AWS ALB, etc.)
# Run multiple backend instances
uvicorn main:app --host 0.0.0.0 --port 8001 &
uvicorn main:app --host 0.0.0.0 --port 8002 &
uvicorn main:app --host 0.0.0.0 --port 8003 &
```

### Database Migration (if needed)
- Move from file storage to PostgreSQL/MongoDB
- Implement MinIO/S3 for audio storage
- Add Redis for caching

## Backup Strategy

```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backups/data_backup_$DATE.tar.gz data/
# Upload to cloud storage (S3, Drive, etc.)
```

## Health Checks

Add health check endpoint:
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "disk_space": shutil.disk_usage("/").free,
        "uptime": time.time() - start_time
    }
```

## Rollback Plan

1. Keep previous version tagged in Git
2. Maintain blue-green deployment
3. Test staging environment before production
4. Monitor error rates after deployment
5. Have rollback script ready

```bash
# Quick rollback
git checkout v1.0.0
# Redeploy
```
