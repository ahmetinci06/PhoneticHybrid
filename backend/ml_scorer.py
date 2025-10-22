"""
ML-based pronunciation scorer using trained neural network.
Replaces heuristic scoring with learned model predictions.
"""

import torch
import torch.nn as nn
import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PronunciationScorer(nn.Module):
    """Neural network for pronunciation quality scoring."""
    
    def __init__(self, input_dim, hidden_dims=[128, 64, 32], dropout=0.3):
        super(PronunciationScorer, self).__init__()
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev_dim = hidden_dim
        
        # Output layer: single score [0, 1]
        layers.append(nn.Linear(prev_dim, 1))
        layers.append(nn.Sigmoid())
        
        self.model = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.model(x)


class MLPronunciationScorer:
    """
    ML-based pronunciation scorer that loads trained model
    and predicts pronunciation quality scores (0-100).
    """
    
    def __init__(self, model_dir: str = "models"):
        """
        Initialize ML scorer by loading trained model and scaler.
        
        Args:
            model_dir: Directory containing model files
        """
        self.model_dir = Path(model_dir)
        self.model = None
        self.scaler_mean = None
        self.scaler_scale = None
        self.feature_names = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        self._load_model()
    
    def _load_model(self):
        """Load trained model weights and scaler parameters."""
        try:
            # Load model architecture info
            model_info_path = self.model_dir / "model_info.json"
            if not model_info_path.exists():
                logger.warning(f"Model info not found: {model_info_path}")
                return False
            
            with open(model_info_path, 'r') as f:
                model_info = json.load(f)
            
            # Initialize model architecture
            self.model = PronunciationScorer(
                input_dim=model_info['input_dim'],
                hidden_dims=model_info.get('hidden_dims', [128, 64, 32]),
                dropout=model_info.get('dropout', 0.3)
            ).to(self.device)
            
            # Load model weights
            model_weights_path = self.model_dir / "pronunciation_scorer.pth"
            if not model_weights_path.exists():
                logger.warning(f"Model weights not found: {model_weights_path}")
                return False
            
            self.model.load_state_dict(torch.load(model_weights_path, map_location=self.device))
            self.model.eval()
            
            # Load scaler parameters
            scaler_path = self.model_dir / "scaler_params.json"
            if not scaler_path.exists():
                logger.warning(f"Scaler params not found: {scaler_path}")
                return False
            
            with open(scaler_path, 'r') as f:
                scaler_params = json.load(f)
            
            self.scaler_mean = np.array(scaler_params['mean'])
            self.scaler_scale = np.array(scaler_params['scale'])
            self.feature_names = scaler_params['feature_names']
            
            logger.info(f"✓ ML model loaded successfully from {self.model_dir}")
            logger.info(f"  Input features: {len(self.feature_names)}")
            logger.info(f"  Device: {self.device}")
            logger.info(f"  Test MAE: {model_info.get('test_mae', 'N/A')}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")
            self.model = None
            return False
    
    def is_available(self) -> bool:
        """Check if ML model is loaded and ready."""
        return self.model is not None
    
    def _extract_feature_vector(self, features: Dict) -> np.ndarray:
        """
        Extract feature vector in correct order for model input.
        
        Args:
            features: Dictionary with extracted acoustic features
            
        Returns:
            NumPy array of features in correct order
        """
        feature_vector = []
        
        for feature_name in self.feature_names:
            if feature_name in features:
                feature_vector.append(features[feature_name])
            else:
                # Missing feature - use 0 as default
                logger.warning(f"Missing feature: {feature_name}, using 0")
                feature_vector.append(0.0)
        
        return np.array(feature_vector, dtype=np.float32)
    
    def _normalize_features(self, feature_vector: np.ndarray) -> np.ndarray:
        """
        Normalize features using stored scaler parameters.
        
        Args:
            feature_vector: Raw feature vector
            
        Returns:
            Normalized feature vector
        """
        return (feature_vector - self.scaler_mean) / self.scaler_scale
    
    def predict_score(self, features: Dict) -> float:
        """
        Predict pronunciation quality score using ML model.
        
        Args:
            features: Dictionary with extracted acoustic features
                     (same format as extract_acoustic_features from inference.py)
        
        Returns:
            Predicted score (0-100)
        """
        if not self.is_available():
            raise RuntimeError("ML model not loaded. Cannot predict score.")
        
        try:
            # Extract and normalize features
            feature_vector = self._extract_feature_vector(features)
            feature_vector_normalized = self._normalize_features(feature_vector)
            
            # Convert to tensor
            feature_tensor = torch.FloatTensor(feature_vector_normalized).unsqueeze(0).to(self.device)
            
            # Predict
            with torch.no_grad():
                prediction = self.model(feature_tensor).item()
            
            # Convert from [0, 1] to [0, 100]
            score = prediction * 100.0
            
            # Clip to valid range
            score = max(0.0, min(100.0, score))
            
            return float(score)
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise
    
    def predict_with_confidence(self, features: Dict, num_samples: int = 10) -> Dict:
        """
        Predict score with uncertainty estimation using dropout.
        
        Args:
            features: Acoustic features dictionary
            num_samples: Number of Monte Carlo samples for uncertainty
            
        Returns:
            Dictionary with mean, std, and confidence interval
        """
        if not self.is_available():
            raise RuntimeError("ML model not loaded.")
        
        try:
            # Enable dropout for uncertainty estimation
            self.model.train()
            
            feature_vector = self._extract_feature_vector(features)
            feature_vector_normalized = self._normalize_features(feature_vector)
            feature_tensor = torch.FloatTensor(feature_vector_normalized).unsqueeze(0).to(self.device)
            
            predictions = []
            for _ in range(num_samples):
                with torch.no_grad():
                    pred = self.model(feature_tensor).item() * 100.0
                    predictions.append(pred)
            
            # Back to eval mode
            self.model.eval()
            
            predictions = np.array(predictions)
            mean_score = np.mean(predictions)
            std_score = np.std(predictions)
            
            # 95% confidence interval
            ci_lower = mean_score - 1.96 * std_score
            ci_upper = mean_score + 1.96 * std_score
            
            return {
                'score': float(mean_score),
                'std': float(std_score),
                'confidence_interval': [float(ci_lower), float(ci_upper)],
                'samples': num_samples
            }
            
        except Exception as e:
            logger.error(f"Uncertainty prediction failed: {e}")
            raise


# Global scorer instance
_ml_scorer = None


def get_ml_scorer(model_dir: str = "models") -> Optional[MLPronunciationScorer]:
    """
    Get or create global ML scorer instance.
    
    Args:
        model_dir: Directory containing model files
        
    Returns:
        MLPronunciationScorer instance or None if not available
    """
    global _ml_scorer
    
    if _ml_scorer is None:
        try:
            _ml_scorer = MLPronunciationScorer(model_dir=model_dir)
            if not _ml_scorer.is_available():
                logger.warning("ML scorer initialized but model not loaded")
                _ml_scorer = None
        except Exception as e:
            logger.error(f"Failed to initialize ML scorer: {e}")
            _ml_scorer = None
    
    return _ml_scorer


def predict_pronunciation_score(features: Dict, use_ml: bool = True) -> float:
    """
    Predict pronunciation score using ML model (if available) or fallback to heuristic.
    
    Args:
        features: Acoustic features dictionary
        use_ml: Whether to try using ML model first
        
    Returns:
        Pronunciation score (0-100)
    """
    if use_ml:
        scorer = get_ml_scorer()
        if scorer and scorer.is_available():
            try:
                return scorer.predict_score(features)
            except Exception as e:
                logger.warning(f"ML prediction failed, falling back to heuristic: {e}")
    
    # Fallback to heuristic scoring
    from inference import PronunciationAnalyzer
    analyzer = PronunciationAnalyzer()
    
    # Get heuristic score (returns 0-1, convert to 0-100)
    heuristic_score = 0.7  # Base score
    
    # Simple heuristic based on available features
    if 'pitch_mean' in features and features['pitch_mean'] > 0:
        heuristic_score += 0.1
    if 'formants' in features and features['formants'].get('F1', 0) > 0:
        heuristic_score += 0.1
    if 'energy_mean' in features and features['energy_mean'] > 0.01:
        heuristic_score += 0.1
    
    return heuristic_score * 100.0
