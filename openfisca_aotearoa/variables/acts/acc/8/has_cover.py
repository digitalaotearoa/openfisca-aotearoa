"""TODO: Add missing doctring."""

from openfisca_core.periods import DAY
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class acc__has_cover(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = u"Has cover for a personal injury"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM100605.html"
