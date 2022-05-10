"""This module provides work-related demographic variables."""

from openfisca_core.periods import DAY, MONTH
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class fulltime_employment(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "The person is not in full-time employment"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783146"


class hours_per_week_employed(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "The hours per week a person is employed for"


class losing_earnings_from_health_injury(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "The person is losing earnings from health injury"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783146"
