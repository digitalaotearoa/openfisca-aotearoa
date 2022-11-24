"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.demographics.housing import AccommodationType

class accommodation_supplement(variables.Variable):
    label = "TODO"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """TODO"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        entitled = people("accommodation_supplement__entitled", period)
        # TODO: move to parameter
        accommodation_costs = people("accommodation_costs", period)
        accommodation_type = people("accommodation_type", period)
        rate = (accommodation_type == AccommodationType.lodging) * .62 + 1
        cost = accommodation_costs * rate
        rebate = people("accommodation_supplement__rebate", period)
        cutout = people("accommodation_supplement__cutout", period)

        return entitled * numpy.maximum(numpy.minimum(cost - rebate, cutout), 0)
