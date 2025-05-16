import os
from dataclasses import dataclass

import config


@dataclass
class PluginInfo:
    url: str
    save_path: str
    _name: str | None = None

    @classmethod
    def from_url(cls, url: str) -> "PluginInfo":
        return cls(
            url=url,
            save_path=os.path.join(config.APPDATA, "BetterDiscord/plugins", url.split("/")[-1])
        )

    def get_name(self) -> str:
        if self._name is None:
            self._name = self.url.split("/")[-1].rstrip(".plugin.js")
        return self._name

    def is_installed(self) -> bool:
        return os.path.exists(self.save_path)

