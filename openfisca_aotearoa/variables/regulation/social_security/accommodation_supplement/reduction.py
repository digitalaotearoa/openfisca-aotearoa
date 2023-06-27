"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class accommodation_supplement__reduction(variables.Variable):
    label = "Income-based reductions"
    reference = "https://legislation.govt.nz/regulation/public/2018/0202/latest/LMS96265.html"
    documentation = """TODO"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, params):
        return 0
