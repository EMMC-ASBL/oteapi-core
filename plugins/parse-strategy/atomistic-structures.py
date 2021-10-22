""" Strategy class for image/jpg """

from dataclasses import dataclass
from app.strategy.factory import StrategyFactory
from typing import Dict, Optional, Any
from app.models.resourceconfig import ResourceConfig
import ase
from ase import Atoms

@dataclass
@StrategyFactory.register(
    ('mediaType', 'chemical/x-xyz'),
    ('mediaType', 'chemical/x-cif'),
    ('mediaType', 'chemical/x-vasp'),  # Not an official internet mediatype
    )
class AtomisticStructureParseStrategy:

    resource_config: ResourceConfig

    def __post_init__(self):
        self.localpath = '/app/data'
        self.filename = self.resource_config.downloadUrl.path.rsplit('/', 1)[-1]
        if self.resource_config.configuration:
            self.conf = self.resource_config.configuration
        else:
            self.conf = {}

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict: #pylint: disable=W0613
        """ Initialize"""
        return dict()

    def parse(self, session: Optional[Dict[str, Any]] = None) -> Dict: #pylint: disable=W0613
        atoms = ase.io.read(f'{self.localpath}/{self.filename}')

        # The Molecule.json contains metadata for energy. We should probably
        # delete that
        # Also, where should this metadata definition reside?
        Molecule = dlite.Instance('json:Molecule.json')  # DLite Metadata  

        atoms.calc = EMT()
        basename = os.path.splitext(f'{self.filename'})[0]
        inst = Molecule(dims=[len(atoms), 3], id=basename)  # DLite instance
        inst.symbols = atoms.get_chemical_symbols()
        inst.masses = atoms.get_masses()
        inst.positions = atoms.positions

        # This should be in a calculation
        atoms.calc = EMT()
        inst.energy = atoms.get_potential_energy()

        # So we have read a molecule and linked it to the correct metadata (
        # actually, we have made new instance of the metadata populated with
        # values. We should probably just have the link between the Metadata
        # and the file.
        # How should we now make the collection?
        coll = dlite.Collection('molecules')
        coll.add(label=basename, inst=inst)
        coll.save('json', 'atomscaledata.json', 'mode=w')


        # Q: Does it have to return a Dict?
        # Q: If it has to return a Dict, what are reqs of this dict?
        return Dict('I have no idea')
