"""TODO: Add missing doctring."""

from openfisca_core.periods import DAY
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class acc__sched_1__minimum_weekly_earnings(Variable):
    value_type = float
    entity = Person
    definition_period = DAY
    label = "Minimum weekly earnings"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104874.html"
