# Deprecated ML Training Documentation

This folder contains documentation for the **old local ML training approach** that has been superseded by the Azure Speech Services integration.

## ⚠️ Note

These guides are **archived for reference only** and are no longer maintained. The project now uses Azure Cognitive Services for production-ready pronunciation analysis.

## Archived Documentation

- **[ML_TRAINING_GUIDE.md](ML_TRAINING_GUIDE.md)** - Complete guide for training custom ML models
- **[ML_QUICK_START.txt](ML_QUICK_START.txt)** - Quick start for the old ML workflow

## Why Deprecated?

The local ML training approach was replaced because:

1. **No Training Required** - Azure provides pre-trained models
2. **Better Accuracy** - Production-grade speech recognition
3. **Easier Deployment** - Just configure API keys
4. **Scalability** - Cloud-based processing
5. **Phoneme-Level Detail** - More granular feedback

## New Approach

For current pronunciation analysis, see:
- [Azure Integration Summary](../azure/AZURE_INTEGRATION_SUMMARY.md)
- [Pronunciation Analysis Guide](../guides/PRONUNCIATION_ANALYSIS_GUIDE.md)

## Archived Code

The corresponding code files are located in:
- `/backend/deprecated/` - Old training scripts
- `/backend/deprecated/ml_colab/` - Google Colab notebooks

## Migration

If you were using the old ML training system:
1. Set up Azure Speech Services (see main README)
2. Configure `.env` with Azure credentials
3. Use the new `/analyze/azure` endpoint

---

**Last Updated:** October 2025 (Archived)
