"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class acc_sched_1__incapacitated_for_6_months(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "Incapacitated for 6 months"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"


class acc_sched_1__loe_more_than_lope(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "Loss of earnings entitlement is more than loss of potential earnings entitlement"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"


class acc_sched_1__engaged_fulltime_study_or_training(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.DAY
    label = "Engaged in full-time study or training, does not include full-time study or training in living or social skills"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"


class acc_sched_1__lope_eligible(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.DAY
    label = "Corporation determination of incapacity"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"

    def formula(persons, period, parameters):
        suffered_personal_injury = persons("acc_part_2__suffered_personal_injury", period)
        has_cover = persons("acc__cover", period)
        incapacitated = persons("incapacity_for_employment__corporation_determination", period)
        lodged_claim = persons("acc_part_3__lodged_claim", period)
        by_injury = persons("incapacity_for_employment__caused_covered_injury", period)
        potential_earner = persons("acc__potential_earner", period)

        over_or_equal_18 = (persons("age", period) >= 18)
        not_engaged_in_study_at_entitlement = numpy.logical_not(persons("acc_sched_1__engaged_fulltime_study_or_training", period))
        earner = persons("acc__earner", period)
        not_earner_with_higher_loe = numpy.logical_not(earner * persons("acc_sched_1__loe_more_than_lope", period))

        six_months = persons("acc_sched_1__incapacitated_for_6_months", period)

        return (suffered_personal_injury
                * has_cover
                * incapacitated
                * lodged_claim
                * by_injury
                * potential_earner
                * over_or_equal_18
                * not_engaged_in_study_at_entitlement
                * not_earner_with_higher_loe
                * six_months)


class acc_sched_1__weekly_earnings(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.DAY
    label = "Weekly earnings"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"


class acc_sched_1__lope_weekly_compensation(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.DAY
    label = "Compensation per week"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"

    def formula(persons, period, parameters):
        hourly_rate_week = parameters(period).minimum_wage.adult_rate * 40
        minimum_earnings = numpy.clip(persons("acc_sched_1__minimum_weekly_earnings", period), hourly_rate_week, None)
        abatement = minimum_earnings * parameters(period).acc.weekly_compensation_abatement
        weekly_earnings = persons("acc_sched_1__weekly_earnings", period)
        return numpy.clip((abatement - (abatement + weekly_earnings - minimum_earnings)), 0, None) * persons("acc_sched_1__lope_eligible", period)
