import os
import tempfile

import dlite
from matplotlib.pyplot import imread


class blob2image(DLiteMappingBase):
    name = "blob2image"
    output_uri = "http://compevo/ontotrans.emmc.eu/0.1/Image"
    input_uris = ["http://meta.sintef.no/0.1/Blob"]
    cost = 25

    def map(self, instances):
        print("*** blob2image")
        blob_image = instances[0]
        with tempfile.NamedTemporaryFile(delete=False) as f:
            inst.save(f"blob:{f.name}")
            data = imread(f.name)
        dims = data.shape
        if len(dims) < 3:
            dims = data.shape + (1,) * (3 - len(dims))
        print("*** dims:", dims)
        image = dlite.Instance(output_uri, dims)
        print("*** image:", image)
        image.data = data
        return image
