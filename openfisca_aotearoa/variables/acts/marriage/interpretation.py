"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class marriage__married(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "is married (marriage means the union of 2 people, regardless of their sex, sexual orientation, or gender identity)"
    reference = "http://www.legislation.govt.nz/act/public/1955/0092/latest/DLM292034.html#DLM5545702"
