# pylint: disable=W0511, W0613 , W0612
"""
Mapping plugin for compevo usecase
"""
import tempfile
from dataclasses import dataclass
from typing import Any, Dict, Optional

import dlite
from matplotlib.pyplot import imread
from pydantic.main import BaseModel

from app.models.mappingconfig import MappingConfig
from app.strategy.factory import StrategyFactory



class ConfigDataModel(BaseModel):
    use_case: str = None
    image_type: str = None
    image_description: str = None


@dataclass
@StrategyFactory.register(("mappingType", "mapping/compevo-map"))
class CompevoMapping:
    """Mapping Interface"""

    mapping_config: MappingConfig

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize mapping"""

        return dict()

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Mapping the image using dlite"""

        mappings = [
            ("image_file", "rdf:type", "compevo:Image"),
            ("image_type", "rdf:type", "compevo:Format"),
            ("image_description", "rdf:type", "compevo:ImageDescription"),
            ("acquisition_time", "rdf:type", "compevo:ISO8601Time"),
            ("acquired_by", "rdf:type", "foaf:Person"),
            # Control mapping to new entity
            ("image_file", "dm:mappedTo", "pore_image"),
            ("image_file", "dm:mapTo", "http://compevo/ontotrans.emmc.eu/0.1/Image"),
            (
                "image_scale",
                "dm:mapValue",
                "http://compevo/ontotrans.emmc.eu/0.1/Image#scale",
            ),
            (
                "image_scale_unit",
                "dm:mapUnit",
                "http://compevo/ontotrans.emmc.eu/0.1/Image#scale",
            ),
        ]

        coll = dlite.get_collection(session["collection_id"])
        dlite.storage_path.append(str("app/entities/*.json"))
        s, p, o = find(mappings, s="image_file", p="dm:mappedTo")
        img = o
        blob = coll.get("blob")
        image = map_blob2image(blob)

        config = ConfigDataModel(**self.mapping_config.configuration)
        coll.add(img, image)
        coll.add_relation(img, "compevo:belongTo", config.use_case)
        coll.add_relation(img, "compevo:hasFormat", config.image_type)
        coll.add_relation(img, "dm:hasDescription", config.image_description)
        coll.add_relation(img, "crop", str(session["crop"]))
        s, p, o = find(mappings, s="image_file", p="rdf:type")
        coll.add_relation(img, "rdf:type", o)

        coll.remove("pore_image")
        coll.add("pore_image", image)
        return dict(MappingStep="compevo-map")


def find(relations, s=None, p=None, o=None):
    """Return first triple matching the query."""
    for ss, pp, oo in relations:
        if (s is None or s == ss) and (p is None or p == pp) and (o is None or o == oo):
            return ss, pp, oo


def map_blob2image(blob):
    """Map dlite instance of type Blob to Image."""
    output_uri = "http://compevo/ontotrans.emmc.eu/0.1/Image"
    with tempfile.NamedTemporaryFile(delete=False) as f:
        blob.save(f"blob:{f.name}")
        data = imread(f.name)
    dims = data.shape
    if len(dims) < 3:
        dims = data.shape + (1,) * (3 - len(dims))
    image = dlite.Instance(output_uri, dims)
    image.data = data
    return image
