from datetime import datetime


class BotConfig:
    _silence_until: datetime | None = None
    _always_silent = False

    @classmethod
    def is_silent(cls) -> bool:
        if cls._always_silent:
            return True
        if cls._silence_until is None:
            return False
        return datetime.now() <= cls._silence_until

    @classmethod
    def set_silence_until(cls, until: datetime) -> None:
        cls._silence_until = until
        cls._always_silent = False

    @classmethod
    def silence(cls):
        cls._silence_until = None
        cls._always_silent = True
    
    @classmethod
    def remove_silence(cls):
        cls._silence_until = None
        cls._always_silent = False

