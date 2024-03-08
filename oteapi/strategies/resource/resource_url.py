"""Strategy class for resource/url."""

import sys

if sys.version_info >= (3, 10):
    from typing import Literal
else:
    from typing_extensions import Literal

from pydantic import Field
from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, HostlessAnyUrl, ResourceConfig


class ResourceURLConfig(ResourceConfig):
    """Resource URL strategy config."""

    resourceType: Literal["resource/url"] = Field(
        "resource/url",
        description=ResourceConfig.model_fields["resourceType"].description,
    )
    downloadUrl: HostlessAnyUrl = Field(
        ...,
        description=ResourceConfig.model_fields["downloadUrl"].description,
    )
    mediaType: str = Field(
        ...,
        description=ResourceConfig.model_fields["mediaType"].description,
    )


@dataclass
class ResourceURLStrategy:
    """Basic resource strategy targeting downloadUrl resources."""

    resource_config: ResourceURLConfig

    def initialize(self) -> "AttrDict":
        """Initialize."""
        return AttrDict()

    def get(self) -> "AttrDict":
        """resource distribution."""
        return AttrDict(
            **self.resource_config.model_dump(
                mode="json", exclude_unset=True, exclude={"resourceType"}
            )
        )
