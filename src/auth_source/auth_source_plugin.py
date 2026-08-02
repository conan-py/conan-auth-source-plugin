"""
    The implementation of the auth source plugin
"""
import logging
from typing import Optional

from auth_source.authenticator import AuthenticatorFactory
from auth_source.config import make_config
from auth_source.source_credentials import load_source_credentials, find_first_credentials
from auth_source.types import AuthSourceDetails

# A conan authentication plugin is not given the conan api or a logger, as it
# might cause recursion problems. Since the logger is not available, reach out
# and get the logger named conan.
logger = logging.getLogger("conan")


def plugin(url: str) -> Optional[AuthSourceDetails]:
    """
        A Conan authentication for source credentials authenticator.

        If the source URL is configured to support generating a github application token
        then return a valid token.
    """
    logging.debug("Loading 'source_credentials.json'")
    source_credentials = load_source_credentials()
    if source_credentials:
        logging.info("Finding credentials for '%s'", url)
        credentials = find_first_credentials(url, source_credentials)
        if credentials:
            config = make_config(credentials)
            if config:
                auth = AuthenticatorFactory.make_authenticator(url, config.type)
                token = auth.make_token(config)
                if token:
                    headers = credentials.get("headers")
                    return {"token": token, "headers": headers} if headers else {"token": token}
                logger.warning("Failed to get github application token '%s'", url)
            else:
                logger.warning("Failed to make configuration for '%s'", url)
        else:
            logger.info("No 'source_credentials.json' configuration for '%s'", url)
    else:
        logger.warning("No 'source_credentials.json' found")
    return None
