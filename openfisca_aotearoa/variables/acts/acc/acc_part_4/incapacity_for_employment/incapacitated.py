"""TODO: Add missing doctring."""

from openfisca_core.periods import DAY, ETERNITY
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class incapacity_for_employment__corporation_determination(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Corporation determination of incapacity"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM101462.html"


class acc__lope__incapacity_for_employment__by_covered_injury(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = "The incapacity is caused by the injury for which they have cover"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM101462.html"
