"""This module provides eligibility and amount for Jobseeker Support."""

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from openfisca_core import holders, periods, variables

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities


class immigration__holds_resident_visa(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Holder of a resident visa"


class immigration__permanent_resident(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Holder of a permanent resident visa"
    reference = "http://legislation.govt.nz/act/public/2009/0051/latest/whole.html#DLM1440311"


class immigration__resident(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Holder of a permanent resident visa or a resident visa"
    reference = "http://legislation.govt.nz/act/public/2009/0051/latest/whole.html#DLM1440311"

    def formula(persons, period, parameters):
        return persons("immigration__holds_resident_visa", period) + persons("immigration__permanent_resident", period)


class immigration__citizen_or_resident(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "NZ Citizen or Resident"
    reference = "http://legislation.govt.nz/act/public/2009/0051/latest/whole.html#DLM1440311"

    def formula(persons, period, parameters):
        return persons("citizenship__citizen", period) + persons("immigration__permanent_resident", period) + persons("immigration__resident", period)


class immigration__recognised_refugee(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DAY
    label = "is recognised as a refugee"
    set_input = holders.set_input_dispatch_by_period
    reference = "https://www.legislation.govt.nz/act/public/2009/0051/latest/whole.html#DLM1440502"


class immigration__protected_person(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "is recognised as a a protected person in New Zealand"


class immigration__temporary_entry_class_visa(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DAY
    reference = "https://www.legislation.govt.nz/act/public/2009/0051/latest/whole.html#DLM1440546"
    label = "means a temporary visa, a limited visa, or an interim visa"
    set_input = holders.set_input_dispatch_by_period
