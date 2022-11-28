"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class acc_part_2__suffered_personal_injury(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "Has suffered a personal injury"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM100910.html"
