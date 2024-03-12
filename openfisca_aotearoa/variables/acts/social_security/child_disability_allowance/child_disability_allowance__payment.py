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


class child_disability_allowance__payment(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Rate of child disability allowance"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS118455", "#sd4-P9-tb1-tr1"

    def formula_2018_11_26(people, period, parameters):
        child_disability_allowance = parameters(period.first_day).social_security.child_disability_allowance.base.clauses["clause_1"]
        return people("child_disability_allowance__eligible", period) * child_disability_allowance
