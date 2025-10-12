# Contributing to PhoneticHybrid

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

See `SETUP_GUIDE.md` for complete installation instructions.

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable names

```python
# Good
def extract_features(audio_path: Path, sample_rate: int = 16000) -> np.ndarray:
    """Extract acoustic features from audio file."""
    pass

# Bad
def ef(p, sr=16000):
    pass
```

### TypeScript (Frontend)
- Use functional components with hooks
- Follow Airbnb style guide
- Use TypeScript strict mode
- Proper prop typing

```typescript
// Good
interface WelcomeProps {
  onNext: () => void
}

export default function Welcome({ onNext }: WelcomeProps) {
  return <Box>...</Box>
}

// Bad
function Welcome(props) {
  return <div>...</div>
}
```

## Commit Messages

Use conventional commits:

```
feat: add new audio feature extraction method
fix: resolve CORS issue in production
docs: update training instructions
refactor: simplify pronunciation scoring logic
test: add unit tests for API endpoints
```

## Pull Request Process

1. **Fork** the repository
2. **Create branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make changes** following code style guidelines
4. **Test thoroughly**:
   ```bash
   # Backend tests
   cd backend
   pytest
   
   # Frontend tests
   cd frontend
   npm run test
   ```
5. **Update documentation** if needed
6. **Commit** with meaningful messages
7. **Push** to your fork
8. **Open Pull Request** with description:
   - What changes were made
   - Why the changes are needed
   - Any breaking changes
   - Screenshots (for UI changes)

## Areas for Contribution

### High Priority
- [ ] Add more phonetic features (pitch contours, stress patterns)
- [ ] Implement user authentication
- [ ] Add real-time feedback during recording
- [ ] Improve model architecture (transformer-based)
- [ ] Multi-language support

### Medium Priority
- [ ] Add unit tests (target >80% coverage)
- [ ] Implement data visualization dashboard
- [ ] Add export functionality (CSV, PDF reports)
- [ ] Optimize audio processing pipeline
- [ ] Add docker-compose setup

### Low Priority
- [ ] Dark mode support
- [ ] Accessibility improvements (WCAG 2.1)
- [ ] Internationalization (i18n)
- [ ] Progressive Web App (PWA) features
- [ ] Offline mode support

## Bug Reports

When reporting bugs, include:

1. **Description** - Clear description of the bug
2. **Steps to Reproduce** - Exact steps to reproduce the issue
3. **Expected Behavior** - What should happen
4. **Actual Behavior** - What actually happens
5. **Environment**:
   - OS version
   - Browser version (for frontend issues)
   - Python version (for backend issues)
   - Node version (for frontend issues)
6. **Screenshots** - If applicable
7. **Logs** - Error messages or stack traces

## Feature Requests

For feature requests, provide:

1. **Problem** - What problem does this solve?
2. **Solution** - Proposed solution
3. **Alternatives** - Alternative solutions considered
4. **Implementation** - High-level implementation plan
5. **Impact** - Who benefits from this feature?

## Code Review Guidelines

Reviewers should check:

- Code follows style guidelines
- Tests pass and cover new code
- Documentation is updated
- No security vulnerabilities
- Performance considerations addressed
- Backward compatibility maintained

## Testing Guidelines

### Backend Tests
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_participant():
    response = client.post("/register", json={
        "name": "Test User",
        "age": 25,
        "gender": "Kadın",
        "consent": True
    })
    assert response.status_code == 200
    assert "participant_id" in response.json()
```

### Frontend Tests
```typescript
// src/components/Welcome.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import Welcome from './Welcome'

test('calls onNext when button clicked', () => {
  const mockOnNext = jest.fn()
  render(<Welcome onNext={mockOnNext} />)
  
  const button = screen.getByText(/Başlamak İçin Tıklayın/i)
  fireEvent.click(button)
  
  expect(mockOnNext).toHaveBeenCalled()
})
```

## Documentation

When adding features, update:

- `README.md` - High-level changes
- Component/function docstrings
- API documentation (if endpoints change)
- `SETUP_GUIDE.md` (if setup changes)
- `ml_colab/ai_training_instructions.txt` (if training changes)

## Questions?

For questions about contributing:
- Open a GitHub Discussion
- Check existing issues and PRs
- Review documentation in `/ml_colab` and project root

Thank you for contributing! 🎉
