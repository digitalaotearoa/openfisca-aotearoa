"""TODO: Add missing doctring."""

from openfisca_core import holders, indexed_enums, periods, variables

from openfisca_aotearoa import entities


# TODO: Refactor and split between accommodation type and cost type
class AccommodationType(indexed_enums.Enum):
    unknown = "We have no idea"
    rent = "Rent"
    board = "Board"
    lodging = "Lodging"
    mortgage = "Mortgage"
    social_housing = "Social housing"
    residential_care = "Residential care"


# TODO: Refactor and split between accommodation type and cost type
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


class arrears(variables.Variable):
    label = "Arrears"
    reference = "https://en.wiktionary.org/wiki/arrear#English"
    documentation = """Unpaid debts"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK


class housing_costs(variables.Variable):
    label = "Housing costs"
    reference = "https://www.workandincome.govt.nz/housing/live-in-home/housing-costs/index.html"
    documentation = """On-going costs of rent, board, lodging, or ownership."""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula(people, period, _params):
        tenants = people("residential_tenancies__tenant", period)
        rent = people.tenancy("residential_tenancies__rent", period)
        bond = people.tenancy("residential_tenancies__bond", period)

        return (rent + bond) * tenants


class service_costs(variables.Variable):
    label = "Service costs"
    reference = "https://www.workandincome.govt.nz/housing/live-in-home/housing-costs/index.html"
    documentation = """Costs of services used by the occupants of a premise."""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK


class arrears(variables.Variable):
    label = "Arrears"
    reference = "https://en.wiktionary.org/wiki/arrear#English"
    documentation = """Unpaid debts"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK
