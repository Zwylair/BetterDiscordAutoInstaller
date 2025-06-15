from typing import Optional

import config

DISABLE_DISCORD_VERSION_CHECKING: bool = False
DISABLE_BDAI_AUTOUPDATE: bool = False
USE_BD_CI_RELEASES: bool = False
GITHUB_TOKEN: Optional[str] = None
WORKFLOW_RUNS_LIMIT: int = 5
RERUN_DISCORD_EDITION: Optional[str] = config.DiscordEdition.STABLE.to_str()

DISCORD_PARENT_PATH: Optional[str] = None
DISCORD_CANARY_PARENT_PATH: Optional[str] = None
DISCORD_PTB_PARENT_PATH: Optional[str] = None
DISCORD_LAUNCH_MINIMIZED: bool = False
LAST_INSTALLED_DISCORD_VERSION: Optional[str] = None
LAST_INSTALLED_DISCORD_CANARY_VERSION: Optional[str] = None
LAST_INSTALLED_DISCORD_PTB_VERSION: Optional[str] = None

LAST_INSTALLED_BD_VERSION: Optional[str] = None
LAST_INSTALLED_BD_CI_VERSION: Optional[str] = None
