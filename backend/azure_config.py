"""
Azure Speech Services Configuration Module
Handles secure loading of Azure credentials from environment variables.
"""

import os
from typing import Optional
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


class AzureConfig:
    """Configuration container for Azure Speech Services."""
    
    def __init__(self):
        """Initialize Azure configuration from environment variables."""
        self.speech_key = os.getenv('AZURE_SPEECH_KEY', '')
        self.region = os.getenv('AZURE_REGION', '')
        
    def is_configured(self) -> bool:
        """
        Check if Azure credentials are properly configured.
        
        Returns:
            bool: True if both speech_key and region are set
        """
        return bool(self.speech_key and self.region)
    
    def get_speech_key(self) -> str:
        """Get Azure Speech API key."""
        if not self.speech_key:
            logger.warning("AZURE_SPEECH_KEY not set in environment")
        return self.speech_key
    
    def get_region(self) -> str:
        """Get Azure region."""
        if not self.region:
            logger.warning("AZURE_REGION not set in environment")
        return self.region
    
    def validate(self) -> None:
        """
        Validate Azure configuration and raise exception if invalid.
        
        Raises:
            ValueError: If configuration is missing or invalid
        """
        if not self.is_configured():
            missing = []
            if not self.speech_key:
                missing.append('AZURE_SPEECH_KEY')
            if not self.region:
                missing.append('AZURE_REGION')
            
            raise ValueError(
                f"Azure configuration incomplete. Missing: {', '.join(missing)}. "
                f"Please set these environment variables in your .env file."
            )


# Global configuration instance
_azure_config: Optional[AzureConfig] = None


def get_azure_config() -> AzureConfig:
    """
    Get or create the global Azure configuration instance.
    
    Returns:
        AzureConfig: The Azure configuration object
    """
    global _azure_config
    
    if _azure_config is None:
        _azure_config = AzureConfig()
        
        if _azure_config.is_configured():
            logger.info(f"Azure Speech Services configured for region: {_azure_config.region}")
        else:
            logger.warning("Azure Speech Services not configured. Set AZURE_SPEECH_KEY and AZURE_REGION in .env")
    
    return _azure_config


def validate_azure_config() -> bool:
    """
    Validate Azure configuration and return status.
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    try:
        config = get_azure_config()
        config.validate()
        return True
    except ValueError as e:
        logger.error(f"Azure configuration validation failed: {e}")
        return False


# For backward compatibility
def get_speech_config():
    """
    Get Azure Speech SDK configuration object.
    
    Returns:
        azure.cognitiveservices.speech.SpeechConfig: Configured speech config
        
    Raises:
        ImportError: If azure-cognitiveservices-speech is not installed
        ValueError: If Azure configuration is incomplete
    """
    try:
        import azure.cognitiveservices.speech as speechsdk
    except ImportError:
        raise ImportError(
            "azure-cognitiveservices-speech not installed. "
            "Install with: pip install azure-cognitiveservices-speech"
        )
    
    config = get_azure_config()
    config.validate()
    
    speech_config = speechsdk.SpeechConfig(
        subscription=config.get_speech_key(),
        region=config.get_region()
    )
    
    # Set language to Turkish
    speech_config.speech_recognition_language = "tr-TR"
    
    return speech_config
