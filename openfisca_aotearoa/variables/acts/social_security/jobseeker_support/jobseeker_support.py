"""This module provides eligibility and amount for Jobseeker Support."""

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from openfisca_core import periods, variables

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities

import numpy

from openfisca_core import holders


# We define the `jobseeker_support` variable.
#
# Please note that by itself a `variable` is not a rule but just a
# specification of such a rule.
#
# A `variable` can contain several rules, otherwise called `formulas`, that is,
# several ways it can be calculated, depending on ther date at which we want to
# calculate it. Said otherwise, as a `concept`, any modelled benefit like
# `jobseeker_support` exist since big bang until big crunch, yet the way of
#  calculating it depends on the applicable law at the requested `period`.
#
# For more information on OpenFisca's `variables`:
# https://openfisca.org/doc/key-concepts/variables.html
class jobseeker_support__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Jobseeker Support eligibility and amount"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783144", "http://legislation.govt.nz/act/public/1964/0136/latest/DLM5478527.html"

    # Old Job Seeker formula for 1964 Act, rewritten to show gaps
    def formula_2013_04_17(persons, period, parameters):

        # this whole section could be covered by a question "is the person seeking work, prepared, available and taking reasonable steps to find it"
        ssa64_88B_1_a = numpy.logical_not(persons("social_security__full_employment", period))

        # ssa64_88B_1_a_i is seeking work - not coded as could be covered by a general question
        # ssa64_88B_1_a_ii is available - not coded as could be covered by a general question

        ssa64_88B_1_a_iii = persons("jobseeker_support__willing_and_able", period)

        ssa64_88B_1_a_iv = persons("jobseeker_support__taken_reasonable_steps", period)

        ssa64_88B_1_a = ssa64_88B_1_a * ssa64_88B_1_a_iii * ssa64_88B_1_a_iv

        # Exemption from Obligations: https://legislation.govt.nz/act/public/1964/0136/latest/DLM365312.html#DLM365312
        # ssa64_88B_1_b TODO not in full time employment, would comply with a but also qualifies for exemption under section 105
        ssa64_88B_1_c = numpy.logical_not(persons("social_security__full_employment", period)) * persons("jobseeker_support__limited_in_capacity", period)

        ssa64_88B_1_d = (persons("social_security__employment", period) + persons("social_security__full_employment", period)) * persons("jobseeker_support__losing_earnings", period)

        ssa64_88B_2 = persons("jobseeker_support__age_requirement", period)

        ssa64_88B_3 = persons("social_security__residential_requirement", period)

        ssa64_88B_4 = persons("jobseeker_support__minimum_income", period)

        # ssa64_88B_5 temporary period makes income sufficient to fully abate benefit...

        ssa64_88B_6 = persons("jobseeker_support__receiving", period) * \
            persons("social_security__full_employment", period) * persons("jobseeker_support__full_employment_temporary", period) * \
            persons("jobseeker_support__income_52_week_period_less_than", period)

        # ssa64_88B_7 loss of earnings by payment to substitute due to sickness or injury

        return ((ssa64_88B_1_a + ssa64_88B_6) + (ssa64_88B_1_a + ssa64_88B_1_c + ssa64_88B_1_d)) * ssa64_88B_2 * ssa64_88B_3 * (ssa64_88B_4 + ssa64_88B_6)

    def formula_2018_11_26(persons, period, parameters):

        ssa20_a = persons("jobseeker_support__work_gap", period)

        ssa20_b = persons("jobseeker_support__available_for_work", period)

        ssa20_c = persons("jobseeker_support__age_requirement", period)

        ssa20_d = persons("social_security__residential_requirement", period)

        ssa20_e = persons("jobseeker_support__minimum_income", period)

        # See ssa2018_25 - hardship grant (MSD may grant)
        # See ssa2018_26 - ineligibility
        # See ssa2018_26_a - TODO full time student
        # See ssa2018_26_b - TODO union strike
        # See ssa2018_26_c - TODO msd believes leave for employment related training
        # See ssa2018_27 - need for certificate with application if jobseeker_support__limited_in_capacity is true
        # See ssa2018_28 - MSD may at any time require applicant to undergo an examination by a prescribed health practitioner

        return ssa20_a * ssa20_b * ssa20_c * ssa20_d * ssa20_e


class jobseeker_support__work_gap(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "The person is not in full-time employment or is losing earnings through a health condition or injury"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783146"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):

        ssa21_1_a = numpy.logical_not(persons("social_security__full_employment", period))
        ssa21_1_b = (persons("social_security__employment", period) + persons("social_security__full_employment", period)) * persons("jobseeker_support__losing_earnings", period)

        # ssa21_2 for the purposes of ssa21_1_b may treat as a loss of earnings a payment made to any other person who acts as a substitute during the period of persons health condition or injury

        ssa21_3_a = persons("jobseeker_support__receiving", period)
        ssa21_3_b = persons("social_security__full_employment", period) * persons("jobseeker_support__full_employment_temporary", period)
        ssa21_3_c = persons("jobseeker_support__income_52_week_period_less_than", period)

        return (ssa21_1_a + ssa21_1_b) + (ssa21_3_a * ssa21_3_b * ssa21_3_c)


class jobseeker_support__available_for_work(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "The person is not in full-time employment or is losing earnings through a health condition or injury"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783146"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):

        ssa22_a = persons("jobseeker_support__willing_and_able", period) * persons("jobseeker_support__taken_reasonable_steps", period)
        # ssa21_b = TODO qualify for exemption section 157
        ssa21_c = persons("jobseeker_support__limited_in_capacity", period)

        return ssa22_a + ssa21_c


class jobseeker_support__losing_earnings(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "In employment but is losing earnings through a health condition or injury"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783146"


class jobseeker_support__receiving(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "is receiving jobseeker support at the rate in clause 1(c), (e), or (f) of Part 1 of Schedule 4, SSA2018 21 3(a)"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783146"


class jobseeker_benefit__granted(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person is currently granted the Jobseeker benefit"
    definition_period = periods.WEEK
    reference = "Reference is unclear, but variable is utilised by the phrase: 'granted a main benefit'"


class jobseeker_support__full_employment_temporary(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "during a temporary period, Person engages in full-time employment, SSA2018 21 3(b)"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783146"


class jobseeker_support__income_52_week_period_less_than(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person’s all income when calculated over a 52-week period is less than the amount that would, under the appropriate income test, reduce the applicable rate of jobseeker support to zero, SSA2018 21 3(c)"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783146"


class jobseeker_support__willing_and_able(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Is prepared for employment?"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783149", "https://legislation.govt.nz/act/public/1964/0136/latest/DLM5478527.html"


class jobseeker_support__taken_reasonable_steps(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Has taken reasonable steps to find it (work)"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783149", "https://legislation.govt.nz/act/public/1964/0136/latest/DLM5478527.html"


class jobseeker_support__limited_in_capacity(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "because of a health condition, injury, or disability, is limited in capacity to seek, undertake, or be available for it (work)"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783149", "https://legislation.govt.nz/act/public/1964/0136/latest/DLM5478527.html"


class jobseeker_support__age_requirement(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Meets the age test for Jobseeker Support?"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783152", "http://legislation.govt.nz/act/public/1964/0136/latest/DLM5478527.html"
    set_input = holders.set_input_dispatch_by_period

    def formula_2013_04_17(persons, period, parameters):
        jobseeker_age_without_dependent_child = parameters(period).entitlements.social_security.jobseeker_support.age_threshold_without_dependent_child
        jobseeker_age_other = parameters(period).entitlements.social_security.jobseeker_support.age_threshold_other
        without_dependent_child = (persons("social_security__dependent_children", period) == 0)

        ssa64_84B_2_a = (persons("age", period.start) >= jobseeker_age_without_dependent_child) * without_dependent_child

        ssa64_84B_2_b = (persons("age", period.start) >= jobseeker_age_other) * numpy.logical_not(without_dependent_child)

        return ssa64_84B_2_a + ssa64_84B_2_b

    def formula_2018_11_26(persons, period, parameters):

        jobseeker_age_without_dependent_child = parameters(period).entitlements.social_security.jobseeker_support.age_threshold_without_dependent_child
        jobseeker_age_other = parameters(period).entitlements.social_security.jobseeker_support.age_threshold_other
        without_dependent_child = (persons("social_security__dependent_children", period) == 0)

        ssa23_a = (persons("age", period.start) >= jobseeker_age_without_dependent_child) * without_dependent_child
        ssa23_b = (persons("age", period.start) >= jobseeker_age_other) * numpy.logical_not(without_dependent_child)

        return ssa23_a + ssa23_b


class jobseeker_support__minimum_income(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Income is below Job Seeker Support threshold?"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783154", "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM5478527"
    set_input = holders.set_input_dispatch_by_period
