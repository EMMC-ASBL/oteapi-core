"""BaseSettings for oteapi-core"""
from pydantic import BaseSettings, Field


class OteApiCoreSettings(BaseSettings):
    """Basic configuration for the oteapi-core."""

    expose_secrets: bool = Field(
        False,
        description="""Wether SecretStr in pydantic should be exposed or not.
        WARNING: Depending on the configuration and user management of the services
        using oteapi-core, secrets might be readable by other users when seralized!
        This especially takes place when then models and configs are put into the cache.
        Hence be carefull while using this option in production.""",
    )

    class Config:
        """Pydantic config for the OteApiCoreSettings."""

        env_prefix = "OTEAPI_"


settings = OteApiCoreSettings()
