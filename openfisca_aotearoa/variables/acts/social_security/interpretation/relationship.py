"""This module provides eligibility and amount for Jobseeker Support."""

from openfisca_core import periods, variables
from openfisca_core import holders

from openfisca_aotearoa import entities


class social_security__in_a_relationship(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Social Security Act definition of 'in a relationship'"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784538"
    set_input = holders.set_input_dispatch_by_period

    def formula(persons, period, parameters):
        return persons("person_has_partner", period.first_month)


class social_security__been_married_or_civil_union_or_de_facto_relationship(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Has been married or in a civil union or de facto relationship"
    reference = "https://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM4686082"


class social_security__parent(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Is a parent?"