"""This module provides eligibility and amount for Jobseeker Support."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class social_security__been_married_or_civil_union_or_de_facto_relationship(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Has been married or in a civil union or de facto relationship"
    reference = "https://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM4686082"


class social_security__parent(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    label = "Is a parent?"
