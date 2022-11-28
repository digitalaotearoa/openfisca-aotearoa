"""TODO: Add missing doctring."""

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core import holders, periods, variables

from openfisca_aotearoa import entities


class income_tax__dependent_child(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DAY
    label = "Determines if a Person is classified as financially dependant"
    reference = "http://legislation.govt.nz/act/public/2007/0097/latest/DLM1520575.html#DLM1520883"
    set_input = holders.set_input_dispatch_by_period

    def formula(person, period, parameters):
        # NOTE: using the age at the start of the month
        # Age changes on a DAY, but this calculation only has a granularity of MONTH
        age = person("age", period.start)
        # TODO - It's not this simple, this needs to be tweaked to include the edge criteria above.
        # not in a marriage, civil union, or de facto relationship
        # is or less than 15
        # or 16 and 17 and not financially independant
        # is 18 and many conditions (see act)
        return age <= 18


class income_tax__principal_caregiver(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Is the person the principal caregiver"
    reference = "https://legislation.govt.nz/act/public/2007/0097/latest/DLM1520575.html#DLM1522335"
    set_input = holders.set_input_dispatch_by_period
