"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class super___eligibility_age(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "The age the applicant will be eligible for NZ Super."
    reference = "http://www.legislation.govt.nz/act/public/2001/0084/latest/DLM114223.html"

    def formula(persons, period, parameters):
        return persons("super__entitled", period) * parameters(period).entitlements.superannuation.age_qualification


class super__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Classified as eligible for NZ Super"
    reference = "http://www.legislation.govt.nz/act/public/2001/0084/latest/DLM113987.html"

    def formula(persons, period, parameters):
        return persons("immigration__citizen_or_resident", period) *\
            numpy.logical_not(persons("total_number_of_years_lived_in_nz_since_age_20", period) < 10) *\
            numpy.logical_not(persons("total_number_of_years_lived_in_nz_since_age_50", period) < 5) *\
            numpy.logical_not(persons("acc__receiving_compensation", period)) +\
            persons(
                "veterans_support__entitled", period)


class super__receiving(variables.Variable):
    label = "TODO"
    reference = "TODO"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK


class super__base(variables.Variable):
    value_type = float
    default_value = 0
    entity = entities.Person
    label = "TODO"
    definition_period = periods.DateUnit.WEEK
    reference = "TODO"


class super__being_paid_nz_superannuation(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "New Zealand superannuation"
    definition_period = periods.DateUnit.MONTH
