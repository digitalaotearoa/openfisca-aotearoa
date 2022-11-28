"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class incapacity_for_employment__corporation_determination(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.DAY
    label = "Corporation determination of incapacity"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM101462.html"


class incapacity_for_employment__caused_covered_injury(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "The incapacity is caused by the injury for which they have cover"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM101462.html"
