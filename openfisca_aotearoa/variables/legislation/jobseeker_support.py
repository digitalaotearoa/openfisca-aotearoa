"""This module provides eligibility and amount for Jobseeker Support."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class jobseeker_support(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DAY
    label = "Jobseeker Support eligibility and amount"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783144"

    def formula_2013_07_15(people, period, parameters):
        work_gap = people("work_gap", period)
        age = people("age", period)
        net_weekly_benefit = parameters(period).legislation.jobseeker_support.net_weekly_benefit

        return work_gap * net_weekly_benefit[age]
