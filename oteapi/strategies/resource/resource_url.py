"""Strategy class for resource/url."""

from typing import Literal

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict
from oteapi.models.resourceconfig import ResourceConfig
from pydantic import Field, AnyHttpUrl
from pydantic.dataclasses import dataclass


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

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict({})

    def get(self) -> AttrDict:
        """resource distribution."""
        return dict(self.resource_config)
