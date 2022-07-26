"""TODO: Add missing doctring."""

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class jobseeker_support__is_prepared_for_employment(Variable):
    value_type = bool
    default_value = True
    entity = Person
    label = "Is prepared for employment?"
    definition_period = MONTH
    reference = "TODO"


class jobseeker_support__meets_age_threshold(Variable):
    value_type = bool
    default_value = True
    entity = Person
    label = "Meets the age test for Jobseeker Support?"
    definition_period = MONTH
    reference = "http://legislation.govt.nz/act/public/1964/0136/latest/DLM5478527.html"

    def formula_1964(persons, period, parameters):
        # over the simpler age threshold
        jobseeker_age = parameters(period).entitlements.social_security.jobseeker_support.age_threshold
        over_age_threshold = persons("age", period.start) >= jobseeker_age

        # over the threshold for appliants with a dependent child
        jobseeker_age_with_dependent_child = parameters(period).entitlements.social_security.jobseeker_support.age_threshold_with_dependent_child
        has_dependent_child = persons("social_security__has_dependant_child", period)
        over_age_threshold_with_dependent_child = (persons("age", period.start) >= jobseeker_age_with_dependent_child) * has_dependent_child

        return over_age_threshold + over_age_threshold_with_dependent_child


class eligible_for_jobseeker(Variable):
    value_type = bool
    entity = Person
    # We need week, but core doesn't support this yet
    # https://github.com/openfisca/openfisca-core/issues/763
    # definition_period = WEEK.
    definition_period = MONTH
    label = "Eligible for Job Seeker Support"
    reference = "http://legislation.govt.nz/act/public/1964/0136/latest/DLM5478527.html"

    # Note this is the commencement of an amendment (day after the 2013 amendment was assented)
    # https://legislation.govt.nz/act/public/2013/0013/latest/DLM4542346.html?search=qs_act%40bill%40regulation%40deemedreg_jobseeker_resel_25_y&p=1
    def formula_2013_04_17(persons, period, parameters):
        # The applicant
        residency_requirements = persons("social_security__meets_residential_requirements_for_certain_benefits", period)

        age_requirement = persons("jobseeker_support__meets_age_threshold", period)

        # income low enough?
        income = persons("jobseeker_support__below_income_threshold", period)

        # Prepared to work
        prepared = persons("jobseeker_support__is_prepared_for_employment", period)

        return age_requirement * income * prepared * residency_requirements

    # Note the more people are eligible becuase there's no income test.
    # but if the person's income is high the amount they get is zero
    def formula_2018_11_26(persons, period, parameters):

        has_work_gap = persons("jobseeker_support__has_work_gap", period)
        is_available_for_work = persons("jobseeker_support__is_available_for_work", period)
        age_requirements = persons("jobseeker_support__meets_age_threshold", period)
        residency = persons("social_security__meets_residential_requirements_for_certain_benefits", period)

        return has_work_gap * is_available_for_work * age_requirements * residency
