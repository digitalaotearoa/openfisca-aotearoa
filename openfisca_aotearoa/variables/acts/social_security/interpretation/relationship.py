"""This module provides eligibility and amount for Jobseeker Support."""

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html

from openfisca_core import periods, variables

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities


class social_security__in_a_relationship(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Social Security Act definition of 'in a relationship'"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784538"

    def formula(persons, period, parameters):
        return persons("married", period) + persons("civil_union", period) + persons("de_facto_relationship", period)


class social_security__been_married_or_civil_union_or_de_facto_relationship(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Has been married or in a civil union or de facto relationship"
    reference = "https://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM4686082"
