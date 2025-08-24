"""
Configuration management for the Vision-Impaired Shopping Assistant.

This module provides centralized configuration settings for all components
including TTS, image processing, and debugging options.
"""


class Config:
    """
    Centralized configuration class for the shopping assistant application.

    This class manages all configuration settings including debug modes,
    text-to-speech parameters, image processing settings, and template strings.
    All settings are class-level attributes that can be updated dynamically.

    Attributes:
        DEBUG (bool): Enable/disable debug mode for visual output
        TTS_SPEED (int): Speech rate for text-to-speech engine
        TTS_OCR_TEMPLATE (str): Template for OCR text announcements
        TTS_BARCODE_FOUND_TEMPLATE (str): Template for product announcements
        TTS_BARCODE_NOT_FOUND_TEMPLATE (str): Message for unknown products
        THRESHOLDING (int): Image processing threshold value
    """

    # Debug settings
    DEBUG = False

    # TTS settings
    TTS_SPEED = 200
    TTS_OCR_TEMPLATE = "{text}"
    TTS_BARCODE_FOUND_TEMPLATE = (
        "Product: {product_name}, Brand: {brand}, Allergies: {allergies}"
    )
    TTS_BARCODE_NOT_FOUND_TEMPLATE = "Unknown barcode scanned"

    # Image processing settings
    THRESHOLDING = 70

    @classmethod
    def enable_debug(cls):
        """Enable debug mode to show visual processing windows."""
        cls.DEBUG = True

    @classmethod
    def disable_debug(cls):
        """Disable debug mode to hide visual processing windows."""
        cls.DEBUG = False

    @classmethod
    def update_settings(cls, settings_dict):
        """
        Update configuration settings from a dictionary.

        Args:
            settings_dict (dict): Dictionary containing setting keys and values

        Returns:
            dict: Dictionary of valid settings that were applied
        """
        valid_settings = {
            key: value
            for key, value in settings_dict.items()
            if hasattr(cls, key) and not key.startswith("_")
        }
        for key, value in valid_settings.items():
            setattr(cls, key, type(getattr(cls, key))(value))
        return valid_settings

    @classmethod
    def get_all_settings(cls):
        """
        Get all configuration settings as a dictionary.

        Returns:
            dict: All public configuration settings and their current values
        """
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith("_")
            and not callable(getattr(cls, key))
            and isinstance(getattr(cls, key), (bool, int, float, str, list, dict))
        }
