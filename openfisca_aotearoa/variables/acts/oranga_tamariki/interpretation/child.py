"""TODO: Add missing doctring."""

from openfisca_core import holders, periods, variables

from openfisca_aotearoa import entities


class oranga_tamariki__child(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is a child as defined in the Interpretation"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/1989/0024/latest/DLM147094.html#DLM149204"
    set_input = holders.set_input_dispatch_by_period

    def formula(persons, period, parameters):
        return persons("age", period.start) < 14


class oranga_tamariki__parent(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is a parent as defined in the Interpretation"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/1989/0024/latest/DLM147094.html#DLM149285"
    set_input = holders.set_input_dispatch_by_period
