"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class civil_union__civil_union(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Two people, whether they are of different or the same sex, may enter into a civil union under this Ac"
    reference = "http://www.legislation.govt.nz/act/public/2004/0102/latest/DLM323410.html"
