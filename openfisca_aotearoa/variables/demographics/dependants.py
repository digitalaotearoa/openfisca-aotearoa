"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

# Import the entities specifically defined for this tax and benefit system
from openfisca_aotearoa import entities


class living_with_parent_or_guardian(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "is living with a parent or guardian"
    definition_period = periods.DateUnit.WEEK


class financially_supported_by_parent_or_guardian(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "is being financially supported by a parent or guardian"
    definition_period = periods.DateUnit.WEEK
