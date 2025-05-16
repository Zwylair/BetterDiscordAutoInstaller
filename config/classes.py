from enum import Enum


class DiscordEdition(Enum):
    STABLE = "Discord"
    CANARY = "DiscordCanary"
    PTB = "DiscordPTB"

    @classmethod
    def from_str(cls, value: str) -> "DiscordEdition":
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"Unknown type: {value!r}")

    def to_str(self) -> str:
        return self.value

    def __str__(self):
        return self.value
