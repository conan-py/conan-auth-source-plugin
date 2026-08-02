from typing import Dict, Optional, TypedDict, List


CredentialBlock = TypedDict(
    "CredentialBlock",
    {
        "url": str,
        "username": Optional[str],
        "password": Optional[str],
        "token": Optional[str],
        "headers": Optional[Dict[str, str]],
        "type": str,

        "app_id": str,
        "app_installation_id": Optional[str],
        "app_private_key": Optional[str],
    },
)

# 2. Define the outer file layout without using a class
SourceCredentials = TypedDict(
    "SourceCredentials",
    {
        "credentials": List[CredentialBlock]
    }
)

AuthSourceDetails = TypedDict(
    "AuthSourceDetails",
    {
        "token": Optional[str],
        "username": Optional[str],
        "password": Optional[str],
        "headers": Optional[Dict[str, str]],
    }
)
