"""This module provides eligibility and amount for Jobseeker Support."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class fulltime_employment(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.DAY
    label = "Whether the person is fully employed"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783146.html"


class losing_earnings_from_health_injury(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    definition_period = periods.DAY
    label = "Person is losing money because of not being able to work"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783146.html"


class work_gap(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DAY
    label = "Person is either jobless or employed but losing money because of injury"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783146.html"

    def formula(people, period):
        fulltime_employment = people("fulltime_employment", period)
        losing_earnings_from_health_injury = people("losing_earnings_from_health_injury", period)

        return (
            + numpy.logical_not(fulltime_employment)
            + fulltime_employment * losing_earnings_from_health_injury
            )


class jobseeker_support(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DAY
    label = "Jobseeker Support eligibility and amount"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783145.html"

    def formula(people, period):
        return people("work_gap", period)