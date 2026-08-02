import logging
from typing import Protocol, runtime_checkable, Optional

from github import GithubIntegration

from auth_source.config import Config

logger = logging.getLogger("conan")


@runtime_checkable
class Authenticator(Protocol):
    def make_token(self, config: Config) -> Optional[str]:
        """
            Make a token given a configuration.

            The token is a short-lived (1 hour) cryptographic string starting with 'ghs_'.
        """
        ...


class GithubApplicationAuthenticator(Authenticator):

    def make_token(self, config: Config) -> str:
        """
            Create an authentication token for the given github application id.
        """
        logger.info(f"GitHub App auth for Installation ID: {config.installation_id}")

        integration = GithubIntegration(config.id, config.private_key)
        auth_connection = integration.get_access_token(config.installation_id)
        return auth_connection.token


class AuthenticatorFactory:

    @staticmethod
    def make_authenticator(_url: str, _auth_type : Optional[str]) -> Authenticator:
        """
            For now, only a github application authenticator is supported.
        """
        return GithubApplicationAuthenticator()
