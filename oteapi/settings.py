"""BaseSettings for oteapi-core.
This `configuration/settings`-class is intended to be incorporated as a
parentclass into the configuration of an FastAPI application.
See `https://fastapi.tiangolo.com/advanced/settings/` as reference.

Otherwise, check `https://github.com/EMMC-ASBL/oteapi-services/blob/master/app/main.py`
for a direct example of an inclusion of the OTE api and its settings into an FastAPI
instance.
"""
from pydantic import BaseSettings, Field


class OteApiCoreSettings(BaseSettings):
    """Basic configuration for the oteapi-core."""

    expose_secrets: bool = Field(
        False,
        description="""Whether `SecretStr` in `pydantic` should be exposed or not.

!!! warning
    Depending on the configuration and user management of the services
    using oteapi-core, secrets might be readable by other users when serialized!
    This especially takes place when then models and configs are put into the cache.
    Hence be careful while using this option in production.
""",
    )

    class Config:
        """Pydantic config for the OteApiCoreSettings."""

        env_prefix = "OTEAPI_"


settings = OteApiCoreSettings()
