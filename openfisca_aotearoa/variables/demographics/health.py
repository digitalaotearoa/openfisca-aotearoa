"""TODO: Add missing doctring."""

from datetime import date

from openfisca_core import holders, periods, variables

from openfisca_aotearoa import entities


class full_capacity(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "is of full capacity (a person shall be deemed to be of full capacity if he is not of unsound mind)"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443689.html#DLM443689"


class date_of_injury(variables.Variable):
    value_type = date
    entity = entities.Person
    label = "Date of injury, ACC act does not explicitly define this term but does add to it for specific circumstances"
    definition_period = periods.ETERNITY  # This variable cannot change over time.
    reference = ""


class totally_blind(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Person is totally blind"


class has_disability(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Person has a disability"
    definition_period = periods.MONTH
    reference = "This appears to not be defined within legislation"
    set_input = holders.set_input_dispatch_by_period
