from io import StringIO
from textwrap import dedent
from typing import Optional, Type

import pytest
from conan.internal.model.options import Options
from conan.internal.model.profile import Profile

from auth_source.source_credentials import find_first_credentials
from auth_source.types import SourceCredentials, CredentialBlock


class TestSourceCredentialsJson:

    @pytest.mark.parametrize(
        "url, credentials, expected",
        [
            # Check an empty template renders ok
            ("https://example.com/org/repo",
             {"credentials": [{
                 "type": "",
                 "url": "https://example.com",
                 "app_id": "abc"
             }]},
             {
                 "type": "",
                 "url": "https://example.com",
                 "app_id": "abc"
             }),
        ])
    def test_package_template(
            self,
            url: str,
            credentials: SourceCredentials,
            expected: Optional[CredentialBlock]):
        """
            Test that a package list template is rendered correctly
        """
        result = find_first_credentials(url, credentials)
        assert expected == result
