"""TODO: Add missing doctring."""

from openfisca_core.periods import DateUnit
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class weekly_accommodation_costs(Variable):
    label = "TODO"
    reference = "TODO"
    documentation = """TODO"""
    entity = Person
    value_type = float
    default_value = 0
    definition_period = DateUnit.WEEK
