"""
Transformation plugin for calculating molcular energies with ase.EMT
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

import dlite
from ase import Atom, Atoms
from ase.calculators.emt import EMT
from oteapi.models.transformationconfig import TransformationConfig
from oteapi.strategy-interfaces.factory import StrategyFactory
from pydantic import BaseModel


class CalcMoleculeConfig(BaseModel):
    moleculeName: Optional[str]


@dataclass
@StrategyFactory.register(("transformation_type", "ase/calc-energy"))
class ASEMoleculeCalculation:
    """Transformations"""

    transformation_config: TransformationConfig

    def __post_init__(self):

        if self.transformation_config.configuration:
            self.conf = self.transformation_config.configuration
        else:
            self.conf = {}

    def initialize(
        self,
        session: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        """Initialize a job"""
        if "collection_id" in session:
            coll = dlite.get_collection(session["collection_id"])
        else:
            coll = dlite.Collection()
            dlite.get_collection(coll.uuid)
        return dict(collection_id=coll.uuid)

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Fetch result and print"""
        coll = dlite.get_collection(session["collection_id"])
        # Get the moleculeName from session if not defined
        # Note that Session only has one molecule_name at any given time
        # even if several molecules have been parsed
        moleculeData = CalcMoleculeConfig(**self.conf)
        if moleculeData.moleculeName is None:
            moleculeData.moleculeName = session["molecule_name"]

        # Get molecule from collection
        molecule = coll.get(moleculeData.moleculeName)

        # Make ase Atom object
        ase_molecule = Atoms()
        for i in range(0, molecule.natoms):
            symbol = molecule.properties["symbols"][i]
            mass = molecule.properties["masses"][i]
            position = molecule.properties["positions"][i]
            atom = Atom(symbol=symbol, mass=mass, position=position)
            ase_molecule.append(atom)

        # Calculate reaction energy and update energy value in collection
        ase_molecule.calc = EMT()
        molecule.groundstate_energy = ase_molecule.get_potential_energy()

        return dict(collection_id=coll.uuid)
