# pylint: disable= W0613
""" Strategy class for image/jpg """

from dataclasses import dataclass
from typing import Any, Dict, Optional

import dlite
from oteapi.models.resourceconfig import ResourceConfig
from oteapi.strategy-interfaces.factory import StrategyFactory
from oteapi.strategy-interfaces.iparsestrategy import create_parse_strategy


@dataclass
@StrategyFactory.register(
    ("mediaType", "dlite-image/jpg"),
    ("mediaType", "dlite-image/jpeg"),
    ("mediaType", "dlite-image/j2p"),
    ("mediaType", "dlite-image/png"),
    ("mediaType", "dlite-image/gif"),
    ("mediaType", "dlite-image/tiff"),
    ("mediaType", "dlite-image/eps"),
)
class DliteImageDataParseStrategy:

    resource_config: ResourceConfig

    def __post_init__(self):
        self.localpath = "/ote-data"
        self.filename = self.resource_config.configuration["artifactName"]
        if self.resource_config.configuration:
            self.conf = self.resource_config.configuration
        else:
            self.conf = {}

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize"""
        return dict(crop=self.conf["crop"])

    def parse(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        parse_strategy = create_parse_strategy(mediatype_dict(self.resource_config))
        read_output = parse_strategy.parse(session)
        print(read_output)
        self.conf.update(session)
        dlite.storage_path.append(str("app/entities/*.json"))
        coll = dlite.get_collection(session["collection_id"])
        cropped = dlite.Instance("blob:" + read_output["cropped_filename"])
        coll.add("blob", cropped)
        return dict(dliteparsecrop="ok")


def mediatype_dict(resource_config: ResourceConfig):
    mediatype = resource_config.mediaType
    resource_config.mediaType = mediatype.replace("dlite-", "")
    return resource_config
