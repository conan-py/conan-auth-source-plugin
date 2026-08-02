import json
import os
import platform
from typing import Optional

from conan.errors import ConanException
from conan.internal.paths import get_conan_user_home
from conan.internal.util.files import load
from jinja2 import Template

from auth_source.types import SourceCredentials, CredentialBlock


def load_source_credentials() -> Optional[SourceCredentials]:
    """
        Reach out into Conan and load the source credentials file. This is not provided as a
        plugin API parameter, so this needs to be loaded again. The `source_credentials.json`
        file is a jinja2 template that must render as JSON.
    """
    home_folder = get_conan_user_home()
    creds_path = os.path.join(home_folder, "source_credentials.json")
    if os.path.exists(creds_path):
        try:
            template = Template(load(creds_path))
            content = template.render({"platform": platform, "os": os})
            return json.loads(content)
        except Exception as e:
            raise ConanException(f"Error loading 'source_credentials.json' {creds_path}: {repr(e)}")
    return None


def find_first_credentials(url: str, source_credentials: Optional[SourceCredentials]) -> Optional[CredentialBlock]:
    """
        Find the first credential block that has a 'url' that is at the start of the source url.
    """
    credentials_list = source_credentials.get("credentials", [])
    for block in credentials_list:
        # Extract the configuration URL pattern from the current block
        config_url = block.get("url")
        if config_url and url.startswith(config_url):
            return block
    return None  # not found
