""" Strategy class for image/jpg """

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import ase.io
import dlite

from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory


@dataclass
@StrategyFactory.register(
    ("mediaType", "chemical/x-xyz"),
    ("mediaType", "chemical/x-cif"),
    ("mediaType", "chemical/x-vasp"),  # Not an official internet mediatype
)
class AtomisticStructureParseStrategy:

    resource_config: ResourceConfig

    def __post_init__(self):
        self.localpath = "/app/data"
        self.filename = self.resource_config.downloadUrl.path.rsplit("/", 1)[-1]
        if self.resource_config.configuration:
            self.conf = self.resource_config.configuration
        else:
            self.conf = {}

    def initialize(
        self, session: Optional[Dict[str, Any]] = None
    ) -> Dict:  # pylint: disable=W0613
        """Initialize"""
        coll = dlite.Collection()
        dlite.get_collection(coll.uuid)
        return dict(collection_id=coll.uuid)

    def parse(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        atoms = ase.io.read(f"{self.localpath}/{self.filename}")

        # The Molecule.json contains metadata for energy which is not part of
        # the molecular structure files.
        Molecule = dlite.Instance("json:Molecule.json")  # DLite Metadata

        basename = os.path.splitext(f"{self.filename}")[0]
        inst = Molecule(dims=[len(atoms), 3], id=basename)  # DLite instance
        inst.symbols = atoms.get_chemical_symbols()
        inst.masses = atoms.get_masses()
        inst.positions = atoms.positions

        inst.groundstate_energy = ""

        # So we have read a molecule and linked it to the correct metadata (
        # actually, we have made new instance of the metadata populated with
        # values. We should probably just have the link between the Metadata
        # and the file.
        # How should we now make the collection?
        coll = dlite.get_collection(session["collection_id"])
        coll.add(label=basename, inst=inst)

        # Return uuid of the collection that now includes the new parsed
        # molecule.
        return dict(collection_id=coll.uuid)
