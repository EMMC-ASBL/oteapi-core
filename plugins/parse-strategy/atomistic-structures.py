""" Strategy class for image/jpg """

from dataclasses import dataclass
from app.strategy.factory import StrategyFactory
from typing import Dict, Optional, Any
from app.models.resourceconfig import ResourceConfig
import ase
from ase import Atoms

@dataclass
@StrategyFactory.register(
    ('mediaType', 'structure/xyz'),
    ('mediaType', 'structure/vasp'),
    ('mediaType', 'structure/cif'),
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
    
    def parse(self, session: Optional[Dict[str, Any]] = None) -> Atoms: #pylint: disable=W0613
        # Q: Does it have to return a Dict?
        # Q: If it has to return a Dict, what are reqs of this dict?
        # This should be able to read various atomistic structure formats with
        # ase, start with .xyz, .cif and vasp/POSCAR files.
        self.conf.update(session)
        atoms = ase.io.read(f'{self.localpath}/{self.filename}')
        return atoms
