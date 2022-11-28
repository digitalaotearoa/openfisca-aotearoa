"""TODO: Add missing doctring."""

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class marriage__married(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "is married (marriage means the union of 2 people, regardless of their sex, sexual orientation, or gender identity)"
    reference = "http://www.legislation.govt.nz/act/public/1955/0092/latest/DLM292034.html#DLM5545702"
