"""TODO: Add missing doctring."""

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class civil_union__civil_union(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Two people, whether they are of different or the same sex, may enter into a civil union under this Ac"
    reference = "http://www.legislation.govt.nz/act/public/2004/0102/latest/DLM323410.html"
