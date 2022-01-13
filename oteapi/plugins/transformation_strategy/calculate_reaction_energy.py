"""
Transformation plugin for calculating reaction energy for a given reaction.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

import dlite
from oteapi.models.transformationconfig import TransformationConfig
from oteapi.strategy-interfaces.factory import StrategyFactory
from pydantic import BaseModel


class ReactionDataModel(BaseModel):
    stoichiometricReactants: Dict


# Define the calculation
def get_energy(reaction):
    """
    Args:
        reaction: dict with energy value of reactants and products as keys
                  and stochiometric coefficient as value
                  Negative stochiometric coefficients for reactants.
                  Positive stochiometric coefficients for products.
    Returns:
        reaction energy
    """
    energy = 0
    for label, n in reaction.items():
        energy += n * float(label)
    return energy


@dataclass
@StrategyFactory.register(("transformation_type", "reaction/calc-reaction-energy"))
class ReactionCalculation:
    """Transformations"""

    transformation_config: TransformationConfig

    def __post_init__(self):

        if self.transformation_config.configuration:
            self.conf = self.transformation_config.configuration
        else:
            self.conf = {}

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Initialize a job"""
        if "collection_id" in session:
            coll = dlite.get_collection(session["collection_id"])
        else:
            coll = dlite.Collection()
            dlite.get_collection(coll.uuid)

        return dict(collection_id=coll.uuid)

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Get molecule energies and calculate reaction energies."""

        reactionData = ReactionDataModel(**self.conf)
        # Get collection from the session
        coll = dlite.get_collection(session["collection_id"])

        # Convert molecule-names to energies and make new
        # dict with stochiometry for each energy
        stoichiometricEnergies = dict()
        for key, val in reactionData.stoichiometricReactants.items():
            molecule = coll.get(key)
            stoichiometricEnergies[molecule.groundstate_energy] = val
        # Calculate reaction energy
        energy = get_energy(stoichiometricEnergies)
        return dict(reaction_energy=energy)
