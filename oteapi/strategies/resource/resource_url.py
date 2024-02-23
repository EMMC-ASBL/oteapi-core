"""Strategy class for resource/url."""

import sys

if sys.version_info >= (3, 10):
    from typing import Literal
else:
    from typing_extensions import Literal

from pydantic import AnyHttpUrl, Field
from pydantic.dataclasses import dataclass

from oteapi.models.resourceconfig import ResourceConfig


class ResourceURLConfig(ResourceConfig):
    """JSON parse strategy filter config."""

    resourceType: Literal["resource/url"] = Field(
        "resource/url",
        description=ResourceConfig.model_fields["resourceType"].description,
    )
    downloadUrl: AnyHttpUrl = Field(
        ...,
        description=ResourceConfig.model_fields["downloadUrl"].description,
    )


@dataclass
class ResourceURLStrategy:
    """Parse strategy for JSON.

    **Registers strategies**:

    - `("strategyType", "resource/url")`

    """

    resource_config: ResourceURLConfig

    def initialize(self) -> dict:
        """Initialize."""
        return {}

    def get(self) -> dict:
        """resource distribution."""
        return dict(self.resource_config)
