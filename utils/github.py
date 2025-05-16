import io
import os
import logging
import zipfile
from typing import Optional

import requests

import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(message)s")


def request_github_token():
    logger.info(
        "You need a Github access token (https://github.com/settings/personal-access-tokens/new) to download "
        "BetterDiscord CI releases. Create token with public repository access and enter here:"
    )
    config.GITHUB_TOKEN = input(">>> ")
    config.dump_github_token()


def get_headers():
    if not config.GITHUB_TOKEN:
        config.load_github_token()

        if not config.GITHUB_TOKEN:
            request_github_token()

    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {config.GITHUB_TOKEN}"
    }


def get_last_successful_run_id(workflows_url: str, workflow_author: str, limit: int = 5) -> Optional[str]:
    logger.info(f"Trying to get last {limit} runs from {workflow_author}...")

    try:
        runs_resp = requests.get(workflows_url, headers=get_headers() | {"per_page": str(limit)})
        runs_resp.raise_for_status()
        workflow_runs = runs_resp.json()["workflow_runs"][:limit]

        for run in workflow_runs:
            if run.get("name") != workflow_author:
                continue

            if run.get("conclusion") != "success":
                continue

            return run["id"]
        else:
            logger.warning(f"No successful runs in latest {limit} {workflow_author} builds.")
            return None
    except Exception as e:
        logger.error(str(e), exc_info=e)
        return None


def get_artifacts_from_run(repo: str, author: str, run_id: str) -> Optional[dict]:
    logger.info(f"Trying to get artifacts from {author} run (id: {run_id})...")

    try:
        arts_resp = requests.get(f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/artifacts", headers=get_headers())
        arts_resp.raise_for_status()
        return arts_resp.json()["artifacts"]
    except Exception as e:
        logger.error(str(e), exc_info=e)
        return None


def find_artefact(artifacts: dict) -> Optional[dict]:
    return next((a for a in artifacts if a.get("name").lower() == "artifact"), None)


def download_artifact(artifact: dict) -> bool:
    try:
        download_url = artifact.get("archive_download_url")
        logger.info(f"Trying to download and extract artifact (url: {download_url})")

        os.makedirs(os.path.dirname(config.BD_CI_ASAR_PATH), exist_ok=True)

        zip_resp = requests.get(download_url, headers=get_headers())
        zip_resp.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(zip_resp.content)) as z:
            for name in z.namelist():
                if not name.endswith(".asar"):
                    continue

                with open(config.BD_CI_ASAR_PATH, "wb") as f:
                    f.write(z.read(name))
                break
            else:
                raise Exception("Artifact file was not found in workflow archive.")
        logger.info("Artifact has been successfully downloaded.")
        return True

    except requests.exceptions.HTTPError as e:
        logger.error("Failed to download BetterDiscord CI asar: Invalid github token.", exc_info=e)
        request_github_token()

        if input("Retry download? (y/n): ") == "y":
            download_artifact(artifact)
        else:
            return False

    except Exception as e:
        logger.error(str(e), exc_info=e)
        return False
