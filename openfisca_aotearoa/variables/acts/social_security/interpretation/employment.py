from openfisca_core import periods, variables
from openfisca_aotearoa import entities


class social_security__employment(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "The definition of employment from Schedule 2 (Dictionary)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784486"


class social_security__full_employment(variables.Variable):
    value_type = bool
    entity = entities.Person
    default_value = False
    definition_period = periods.WEEK
    label = "The definition of full employment or full-time employment from Schedule 2 (Dictionary)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784514"
