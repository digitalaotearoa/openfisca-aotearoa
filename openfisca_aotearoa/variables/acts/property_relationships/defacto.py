"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class property_relationships__de_facto_relationship(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "in a de facto relationship, a relationship between 2 persons (whether a man and a woman, or a man and a man, or a woman and a woman)"
    reference = "http://www.legislation.govt.nz/act/public/1976/0166/latest/DLM441113.html"
