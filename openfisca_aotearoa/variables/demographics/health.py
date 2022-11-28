"""TODO: Add missing doctring."""

import datetime

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class full_capacity(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "is of full capacity (a person shall be deemed to be of full capacity if he is not of unsound mind)"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443689.html#DLM443689"


class date_of_injury(variables.Variable):
    value_type = datetime.date
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
