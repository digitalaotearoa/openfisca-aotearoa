"""TODO: Add missing doctring."""

from openfisca_core import periods, variables
from openfisca_aotearoa import entities


class emergency_benefit__granted(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person is currently granted the Emergency benefit"
    definition_period = periods.WEEK
    reference = "Reference is unclear, but variable is utilised by the phrase: 'granted a main benefit'"
