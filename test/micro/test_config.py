from typing import Optional

import pytest

from auth_source.config import make_config, Config
from auth_source.types import CredentialBlock


class TestSourceCredentialsJson:

    @pytest.mark.parametrize(
        "credential, expected",
        [
            # example with no github parameters
            (
                    {
                        "type": "",
                        "url": "https://example.com",
                    },
                    None
            ),

            # example with github parameters and application id as an integer
            (
                    {
                        "type": "",
                        "url": "https://example.com",
                        "app_id": "abc",
                        "app_private_key": "secret string",
                        "app_installation_id": 777
                    },
                    Config(
                        type="",
                        id="abc",
                        private_key="secret string",
                        installation_id=777
                    )
            ),
        ])
    def test_package_template(self, credential: CredentialBlock, expected: Optional[Config]):
        """
            Test that a config is loaded correctly. Given the environment is global,
            and is not injected, testing environment variable defaults is not tested.
        """
        result = make_config(credential)
        assert expected == result
