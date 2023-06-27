"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.demographics.housing import AccommodationType


class accommodation_supplement__rate(variables.Variable):
    label = "TODO"
    reference = "TODO"
    documentation = """TODO"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        # TODO: move to parameter
        accommodation_type = people("accommodation_type", period)
        return (
            + (accommodation_type != AccommodationType.lodging)
            + (accommodation_type == AccommodationType.lodging)
            * .62
            )
