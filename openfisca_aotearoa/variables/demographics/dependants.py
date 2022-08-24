"""TODO: Add missing doctring."""

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

# Import the entities specifically defined for this tax and benefit system
from openfisca_aotearoa.entities import Person


class dependent_child(Variable):
    value_type = bool
    entity = Person
    label = "has a dependent child or dependent children"
    definition_period = MONTH
    default_value = True


class living_with_parent_or_guardian(Variable):
    value_type = bool
    entity = Person
    label = "is living with a parent or guardian"
    definition_period = MONTH


class financially_supported_by_parent_or_guardian(Variable):
    value_type = bool
    entity = Person
    label = "is being financially supported by a parent or guardian"
    definition_period = MONTH
