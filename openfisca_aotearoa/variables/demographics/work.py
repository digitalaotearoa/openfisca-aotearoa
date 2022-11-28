"""This module provides work-related demographic variables."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class fulltime_employment(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DAY
    label = "The person is not in full-time employment"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783146"


class hours_per_week_employed(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.MONTH
    label = "The hours per week a person is employed for"


class losing_earnings_from_health_injury(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DAY
    label = "The person is losing earnings from health injury"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783146"


class work_gap(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DAY
    label = "The person has a work gap"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783146"

    def formula(people, period):
        fulltime_employment = people("fulltime_employment", period)
        losing_earnings_from_health_injury = people("losing_earnings_from_health_injury", period)

        return (
            + numpy.logical_not(fulltime_employment)
            + fulltime_employment * losing_earnings_from_health_injury
            )
