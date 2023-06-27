"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


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
        accommodation_costs = people("accommodation_costs", period)
        rate = people("accommodation_supplement__rate", period)
        cost = accommodation_costs * rate
        rebate = people("accommodation_supplement__rebate", period)
        cutout = people("accommodation_supplement__cutout", period)

        return entitled * numpy.maximum(numpy.minimum(cost - rebate, cutout), 0)
