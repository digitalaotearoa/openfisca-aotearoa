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



class number_of_years_lived_in_nz(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Number of years lived in NZ"


class total_number_of_years_lived_in_nz_since_age_20(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Total number of years lived in NZ since age 20"


class total_number_of_years_lived_in_nz_since_age_50(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Total number of years lived in NZ since age 50"
