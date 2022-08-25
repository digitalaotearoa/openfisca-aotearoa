"""TODO: Add missing doctring."""

from numpy import clip, logical_not

from openfisca_core.periods import DAY, ETERNITY
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class acc__sched_1__incapacitated_for_6_months(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = "Incapacitated for 6 months"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"


class acc__sched_1__loe_more_than_lope(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = "Loss of earnings entitlement is more than loss of potential earnings entitlement"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"


class acc__sched_1__engaged_fulltime_study_or_training(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Engaged in full-time study or training, does not include full-time study or training in living or social skills"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"


class acc__sched_1__lope_eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Corporation determination of incapacity"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"

    def formula(persons, period, parameters):
        suffered_personal_injury = persons("acc__part_2__suffered_personal_injury", period)
        has_cover = persons("acc__cover", period)
        incapacitated = persons("incapacity_for_employment__corporation_determination", period)
        lodged_claim = persons("acc_part_3__lodged_claim", period)
        by_injury = persons("acc__lope__incapacity_for_employment__by_covered_injury", period)
        potential_earner = persons("acc__potential_earner", period)

        over_or_equal_18 = (persons("age", period) >= 18)
        not_engaged_in_study_at_entitlement = logical_not(persons("acc__sched_1__engaged_fulltime_study_or_training", period))
        earner = persons("acc__earner", period)
        not_earner_with_higher_loe = logical_not(earner * persons("acc__sched_1__loe_more_than_lope", period))

        six_months = persons("acc__sched_1__incapacitated_for_6_months", period)

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


class acc__sched_1__weekly_earnings(Variable):
    value_type = float
    entity = Person
    definition_period = DAY
    label = "Weekly earnings"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"


class acc__sched_1__lope_weekly_compensation(Variable):
    value_type = float
    entity = Person
    definition_period = DAY
    label = "Compensation per week"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"

    def formula(persons, period, parameters):
        hourly_rate_week = parameters(period).minimum_wage.adult_rate * 40
        minimum_earnings = clip(persons("acc__sched_1__minimum_weekly_earnings", period), hourly_rate_week, None)
        abatement = minimum_earnings * parameters(period).acc.weekly_compensation_abatement
        weekly_earnings = persons("acc__sched_1__weekly_earnings", period)
        return clip((abatement - (abatement + weekly_earnings - minimum_earnings)), 0, None) * persons("acc__sched_1__lope_eligible", period)
