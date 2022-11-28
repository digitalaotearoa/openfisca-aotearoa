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


class social_security__income(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    label = "Income of a person as defined in Part 2"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784816"
