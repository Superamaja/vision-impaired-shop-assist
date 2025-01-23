class Config:
    DEBUG = False

    @classmethod
    def enable_debug(cls):
        cls.DEBUG = True

    @classmethod
    def disable_debug(cls):
        cls.DEBUG = False
