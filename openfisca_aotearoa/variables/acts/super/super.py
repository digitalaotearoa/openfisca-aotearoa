"""TODO: Add missing doctring."""

from numpy import logical_not as not_

from openfisca_core.periods import ETERNITY, MONTH
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class super___eligibility_age(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = "The age the applicant will be eligible for NZ Super."
    reference = "http://www.legislation.govt.nz/act/public/2001/0084/latest/DLM114223.html"

    def formula(persons, period, parameters):
        return persons("super__eligible", period) * parameters(period).entitlements.superannuation.age_qualification


class super__eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Classified as eligible for NZ Super"
    reference = "http://www.legislation.govt.nz/act/public/2001/0084/latest/DLM113987.html"

    def formula(persons, period, parameters):
        return persons("immigration__citizen_or_resident", period) *\
            not_(persons("total_number_of_years_lived_in_nz_since_age_20", period) < 10) *\
            not_(persons("total_number_of_years_lived_in_nz_since_age_50", period) < 5) *\
            not_(persons("acc__receiving_compensation", period)) +\
            persons(
                "veterans_support__entitled", period)


class super__being_paid_nz_superannuation(Variable):
    value_type = bool
    entity = Person
    label = "New Zealand superannuation"
    definition_period = MONTH
