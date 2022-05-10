"""This module provides eligibility and amount for Jobseeker Support."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class jobseeker_support(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DAY
    label = "Jobseeker Support eligibility and amount"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783144"

    def formula_2013_07_15(people, period, parameters):
        # A person is entitled to jobseeker support if the person:

        # Is not in full-time employment.
        fulltime_employment = people("fulltime_employment", period)

        return numpy.logical_not(fulltime_employment)
