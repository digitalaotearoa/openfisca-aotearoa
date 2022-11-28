"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class family_scheme__qualifies_for_minimum_family_tax_credit(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Is a person is qualified as eligible for the minimum family tax credit"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518564.html"

    def formula(persons, period, parameters):
        base_qualifies = persons("family_scheme__base_qualifies", period)
        received_tested_benefit = persons("social_security__received_income_tested_benefit", period.this_year)
        received_parents_allowance = persons("veterans_support__received_parents_allowance", period)
        received_childrens_pension = persons("veterans_support__received_childrens_pension", period)
        full_time_earner = persons("family_scheme__full_time_earner", period)

        return base_qualifies * full_time_earner * numpy.logical_not(received_tested_benefit) * numpy.logical_not(received_parents_allowance) * numpy.logical_not(received_childrens_pension)
