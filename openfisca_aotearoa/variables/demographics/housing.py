"""TODO: Add missing doctring."""

from openfisca_core import holders, indexed_enums, periods, variables

from openfisca_aotearoa import entities


class AccommodationType(indexed_enums.Enum):
    unknown = "We have no idea"
    rent = "Rent"
    board = "Board"
    lodging = "Lodging"
    mortgage = "Mortgage"
    social_housing = "Social housing"
    residential_care = "Residential care"


class accommodation_type(variables.Variable):
    label = "TODO"
    reference = "TODO"
    documentation = """TODO"""
    entity = entities.Person
    value_type = indexed_enums.Enum
    possible_values = AccommodationType
    default_value = AccommodationType.unknown
    definition_period = periods.DateUnit.WEEK
    set_input = holders.set_input_dispatch_by_period


class accommodation_costs(variables.Variable):
    label = "TODO"
    reference = "TODO"
    documentation = """TODO"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK
    set_input = holders.set_input_dispatch_by_period
