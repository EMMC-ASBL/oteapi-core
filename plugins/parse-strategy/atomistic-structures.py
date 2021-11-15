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
    ("mediaType", "chemical/x-vasp"),  # Not an official internet mediatype
)
class AtomisticStructureParseStrategy:
    # Which filter to use for a parsing strategy?
    # resource_config must be wrong, but is filter right? why?
    resource_config: ResourceConfig

    def __post_init__(self):
        self.localpath = "/ote-data"
        self.filename = self.resource_config.downloadUrl.path.rsplit("/", 1)[-1]
        if self.resource_config.configuration:
            self.conf = self.resource_config.configuration
        else:
            self.conf = {}

    def initialize(
        self,
        session: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        """Initialize"""
        # coll = dlite.Collection()
        # dlite.get_collection(coll.uuid)
        print("initializes parser", session)
        return dict()  # collection_id=coll.uuid)

    def parse(
        self,
        session: Optional[Dict[str, Any]] = None,
        MoleculeModel: dlite.Instance = None,
    ) -> Dict:

        # Read the atoms and create and ase.Atoms object
        atoms = ase.io.read(f"{self.localpath}/{self.filename}")

        # The Molecule.json contains metadata for energy which is not part of
        # the molecular structure files.
        dlite.storage_path.append(str("/app/entities"))

        if "collection_id" in session:

            coll = dlite.get_collection(session["collection_id"])

        else:
            coll = dlite.Collection()
            dlite.get_collection(coll.uuid)

        if MoleculeModel == None:
            MoleculeModel = dlite.Instance(  # Need to fix storagepath
                "json:///app/entities/Molecule.json"
            )  # DLite Metadata

        basename = os.path.splitext(f"{self.filename}")[0]

        inst = MoleculeModel(dims=[len(atoms), 3], id=basename)  # DLite instance
        inst.symbols = atoms.get_chemical_symbols()
        inst.masses = atoms.get_masses()
        inst.positions = atoms.positions
        print(coll)

        inst.groundstate_energy = 0.0

        coll.add(label=basename, inst=inst)
        print(coll)
        # Return uuid of the collection that now includes the new parsed
        # molecule.
        # We are passing the data though, is that correct?

        return dict(collection_id=coll.uuid, molecule_name=basename)
