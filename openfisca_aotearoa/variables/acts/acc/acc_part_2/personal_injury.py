"""TODO: Add missing doctring."""

from openfisca_core.periods import ETERNITY
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class acc_part_2__suffered_personal_injury(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = "Has suffered a personal injury"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM100910.html"
