class Config:
    # Debug settings
    DEBUG = False

    # TTS settings
    TTS_SPEED = 200

    # Image processing settings
    THRESHOLDING = 70

    @classmethod
    def enable_debug(cls):
        cls.DEBUG = True

    @classmethod
    def disable_debug(cls):
        cls.DEBUG = False

    @classmethod
    def update_settings(cls, settings_dict):
        """Update configuration settings from a dictionary"""
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
        """Get all configuration settings as a dictionary"""
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith("_")
            and not callable(getattr(cls, key))
            and isinstance(getattr(cls, key), (bool, int, float, str, list, dict))
        }
