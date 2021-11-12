# pylint: disable=W0613, W0511
""" Strategy class for image/jpg """

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from pydantic.main import BaseModel

from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory


class DataConfig(BaseModel):
    artifactName: Optional[str]


@dataclass
@StrategyFactory.register(("scheme", "http"), ("scheme", "https"))
class HTTPSStrategy:

    resource_config: ResourceConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize"""
        return dict()

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Download via http/https and store on local cache"""
        req = requests.get(self.resource_config.downloadUrl, allow_redirects=True)
        if self.resource_config.configuration is not None:
            dataConfig = DataConfig(**self.resource_config.configuration)
            filename = dataConfig.artifactName
        else:
            filename = self.resource_config.downloadUrl.path.split("/")[-1]
            self.resource_config.configuration = dict(artifactName=filename)
        # TODO: Use configurable cache storage location
        filepath = f"/ote-data/{filename}"
        print(f"-> STORING AT {filepath}")
        with open(filepath, "wb") as output:
            output.write(req.content)
            return dict(filename=filepath)
