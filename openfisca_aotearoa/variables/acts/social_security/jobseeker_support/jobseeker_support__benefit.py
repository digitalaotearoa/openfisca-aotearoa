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


class jobseeker_support__benefit(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = ""
    reference = ""


class jobseeker_support__base(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Jobseeker Support - Base Amount, (this is taxed and the amounts are supplied after tax, i.e. net)"

    def formula_2018_11_26(people, period, parameters):
        # Get `single` for each person in `people` at `period`, where `period`
        # is "forever", as in "Are you single now?"
        single = numpy.logical_not(people("social_security__in_a_relationship", period))
        age = people("age", period.first_day)

        clause_1_a =  single * (age < 20) * people("jobseeker_support__living_with_parent", period)
        # clause_1_a_ii this could not be true any more? 1998 is more than 20 years ago

        clause_1_b = numpy.logical_not(clause_1_a) * \
            single * (age < 25) * (people("social_security__dependent_children", period ) == 0)

        clause_1_c = people("jobseeker_support__transferred_15_july_2013",  periods.DateUnit.ETERNITY)  * (people("social_security__dependent_children", period ) == 0)

        clause_1_d = numpy.logical_not(clause_1_a + clause_1_b + clause_1_c) * \
            single * (people("social_security__dependent_children", period ) == 0)


        clause_1_e = single * (people("social_security__dependent_children", period ) > 0) * \
            people("social_security__age_youngest_dependant_child", period.first_day) >= 14

        clause_1_f = numpy.logical_not(clause_1_a) * numpy.logical_not(clause_1_e) * \
            single * (people("social_security__dependent_children", period ) > 0)


        in_a_relationship = numpy.logical_not(single)
        clause_1_g = people.family.any(people.family.members("social_security__granted_main_benefit", period), role=entities.Family.PARTNER)
        clause_1_g_i = in_a_relationship * clause_1_g * (people("social_security__dependent_children", period ) < 1)
        clause_1_g_ii = in_a_relationship * clause_1_g * (people("social_security__dependent_children", period ) >= 1)

        clause_1_h = people.family.any(people.family.members("super__being_paid_nz_superannuation", period.first_month), role=entities.Family.PARTNER)
        clause_1_h_i = in_a_relationship * clause_1_h * (people("social_security__dependent_children", period ) < 1)
        clause_1_h_ii = in_a_relationship * clause_1_h * (people("social_security__dependent_children", period ) >= 1)

        clause_1_i = people.family.any(people.family.members("veterans_support__being_paid_a_veterans_pension", period.first_month), role=entities.Family.PARTNER)
        clause_1_i_i = in_a_relationship * clause_1_i * (people("social_security__dependent_children", period ) < 1)
        clause_1_i_ii = in_a_relationship * clause_1_i * (people("social_security__dependent_children", period ) >= 1)

        clause_1_j = in_a_relationship * numpy.logical_not(clause_1_g) * numpy.logical_not(clause_1_h) * numpy.logical_not(clause_1_i)
        clause_1_j_i = in_a_relationship * clause_1_j * (people("social_security__dependent_children", period ) < 1)
        clause_1_j_ii = in_a_relationship * clause_1_j * (people("social_security__dependent_children", period ) >= 1)

        # part2 Housekeeper increases

        # part3   exceptions relating to person who spouse or partner is ineligible for a benefit for a period because
        # part3_i
        # part3_ii
        # part3_a voluntary unemployment or loss of employment through misconduct
        # part3_b failures to comply with work test etc
        # part3_c strike action

        # part4   relates to clause_1_e and is a number of exceptions relating to the 14th/15th of July 2013
        # part4_a
        # part4_b
        # part4_c

        # part5 MSD may disregard up to $20 a week of the beneficiary's personal earnings used to meet the cost of childcare for any of the beneficiary's dependent children

        # part6 lose regular support of spouse, partner who is subject to sentence of imprisonment

        # part7 dependent child can not be counted if receiving orphans benefit or unsupported child's benefit

        clause_1_a_net_weekly_benefit = clause_1_a * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_a"])
        clause_1_b_net_weekly_benefit = clause_1_b * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_b"])
        clause_1_c_net_weekly_benefit = clause_1_c * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_c"])
        clause_1_d_net_weekly_benefit = clause_1_d * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_d"])
        clause_1_e_net_weekly_benefit = clause_1_e * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_e"])
        clause_1_f_net_weekly_benefit = clause_1_f * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_f"])
        clause_1_g_i_net_weekly_benefit = clause_1_g_i * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_g_i"])
        clause_1_g_ii_net_weekly_benefit = clause_1_g_ii * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_g_ii"])
        clause_1_h_i_net_weekly_benefit = clause_1_h_i * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_h_i"])
        clause_1_h_ii_net_weekly_benefit = clause_1_h_ii * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_h_ii"])

        clause_1_i_i_net_weekly_benefit = clause_1_i_i * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_i_i"])
        clause_1_i_ii_net_weekly_benefit = clause_1_i_ii * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_i_ii"])

        clause_1_j_i_net_weekly_benefit = clause_1_j_i * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_j_i"])
        clause_1_j_ii_net_weekly_benefit = clause_1_j_ii * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_j_ii"])


         # Calculate the gross amount (before benefit reductions).
        #
        # Note: we're not calculating eligibility here, so the result of this
        # calculation is a "theoretical amount".
        base = clause_1_a_net_weekly_benefit + clause_1_b_net_weekly_benefit + clause_1_c_net_weekly_benefit + clause_1_d_net_weekly_benefit + clause_1_e_net_weekly_benefit + clause_1_f_net_weekly_benefit + \
            clause_1_g_i_net_weekly_benefit + clause_1_g_ii_net_weekly_benefit + \
            clause_1_h_i_net_weekly_benefit + clause_1_h_ii_net_weekly_benefit + \
            clause_1_i_i_net_weekly_benefit + clause_1_i_ii_net_weekly_benefit + \
            clause_1_j_i_net_weekly_benefit + clause_1_j_ii_net_weekly_benefit
        return people("jobseeker_support__entitled", period) * base

    def formula_2020_11_09(people, period, parameters):
        # This is the date clause 1 (i) was repealed as per: https://www.legislation.govt.nz/act/public/2018/0032/152.0/DLM6784850.html
        # (by section 43(2) of the New Zealand Superannuation and Veteran’s Pension Legislation Amendment Act 2020 (2020 No 36))

        # Get `single` for each person in `people` at `period`, where `period`
        # is "forever", as in "Are you single now?"
        single = numpy.logical_not(people("social_security__in_a_relationship", period))
        age = people("age", period.first_day)

        clause_1_a =  single * (age < 20) * people("jobseeker_support__living_with_parent", period)
        # clause_1_a_ii this could not be true any more? 1998 is more than 20 years ago

        clause_1_b = numpy.logical_not(clause_1_a) * \
            single * (age < 25) * (people("social_security__dependent_children", period ) == 0)

        clause_1_c = people("jobseeker_support__transferred_15_july_2013",  periods.DateUnit.ETERNITY)  * (people("social_security__dependent_children", period ) == 0)

        clause_1_d = numpy.logical_not(clause_1_a + clause_1_b + clause_1_c) * \
            single * (people("social_security__dependent_children", period ) == 0)


        clause_1_e = single * (people("social_security__dependent_children", period ) > 0) * \
            people("social_security__age_youngest_dependant_child", period.first_day) >= 14

        clause_1_f = numpy.logical_not(clause_1_a) * numpy.logical_not(clause_1_e) * \
            single * (people("social_security__dependent_children", period ) > 0)


        in_a_relationship = numpy.logical_not(single)
        clause_1_g = people.family.any(people.family.members("social_security__granted_main_benefit", period), role=entities.Family.PARTNER)
        clause_1_g_i = in_a_relationship * clause_1_g * (people("social_security__dependent_children", period ) < 1)
        clause_1_g_ii = in_a_relationship * clause_1_g * (people("social_security__dependent_children", period ) >= 1)

        clause_1_h = people.family.any(people.family.members("super__being_paid_nz_superannuation", period.first_month), role=entities.Family.PARTNER) + \
            people.family.any(people.family.members("veterans_support__being_paid_a_veterans_pension", period.first_month), role=entities.Family.PARTNER)
        clause_1_h_i = in_a_relationship * clause_1_h * (people("social_security__dependent_children", period ) < 1)
        clause_1_h_ii = in_a_relationship * clause_1_h * (people("social_security__dependent_children", period ) >= 1)

        clause_1_j = in_a_relationship * numpy.logical_not(clause_1_g) * numpy.logical_not(clause_1_h)
        clause_1_j_i = in_a_relationship * clause_1_j * (people("social_security__dependent_children", period ) < 1)
        clause_1_j_ii = in_a_relationship * clause_1_j * (people("social_security__dependent_children", period ) >= 1)

        # part2 Housekeeper increases

        # part3   exceptions relating to person who spouse or partner is ineligible for a benefit for a period because
        # part3_i
        # part3_ii
        # part3_a voluntary unemployment or loss of employment through misconduct
        # part3_b failures to comply with work test etc
        # part3_c strike action

        # part4   relates to clause_1_e and is a number of exceptions relating to the 14th/15th of July 2013
        # part4_a
        # part4_b
        # part4_c

        # part5 MSD may disregard up to $20 a week of the beneficiary's personal earnings used to meet the cost of childcare for any of the beneficiary's dependent children

        # part6 lose regular support of spouse, partner who is subject to sentence of imprisonment

        # part7 dependent child can not be counted if receiving orphans benefit or unsupported child's benefit

        clause_1_a_net_weekly_benefit = clause_1_a * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_a"])
        clause_1_b_net_weekly_benefit = clause_1_b * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_b"])
        clause_1_c_net_weekly_benefit = clause_1_c * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_c"])
        clause_1_d_net_weekly_benefit = clause_1_d * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_d"])
        clause_1_e_net_weekly_benefit = clause_1_e * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_e"])
        clause_1_f_net_weekly_benefit = clause_1_f * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_f"])
        clause_1_g_i_net_weekly_benefit = clause_1_g_i * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_g_i"])
        clause_1_g_ii_net_weekly_benefit = clause_1_g_ii * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_g_ii"])
        clause_1_h_i_net_weekly_benefit = clause_1_h_i * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_h_i"])
        clause_1_h_ii_net_weekly_benefit = clause_1_h_ii * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_h_ii"])
        clause_1_j_i_net_weekly_benefit = clause_1_j_i * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_j_i"])
        clause_1_j_ii_net_weekly_benefit = clause_1_j_ii * (parameters(period.first_day).social_security.jobseeker_support.base.clauses["clause_1_j_ii"])

        # Calculate the gross amount (before benefit reductions).
        #
        # Note: we're not calculating eligibility here, so the result of this
        # calculation is a "theoretical amount".
        base = clause_1_a_net_weekly_benefit + clause_1_b_net_weekly_benefit + clause_1_c_net_weekly_benefit + clause_1_d_net_weekly_benefit + clause_1_e_net_weekly_benefit + clause_1_f_net_weekly_benefit + \
            clause_1_g_i_net_weekly_benefit + clause_1_g_ii_net_weekly_benefit + \
            clause_1_h_i_net_weekly_benefit + clause_1_h_ii_net_weekly_benefit + \
            clause_1_j_i_net_weekly_benefit + clause_1_j_ii_net_weekly_benefit
        return people("jobseeker_support__entitled", period) * base


class p(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = ""
    reference = ""


class jobseeker_support__reduction(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = ""
    reference = ""


class jobseeker_support__living_with_parent(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "As defined in Part 1 of Schedule 4 of the Social Security Act, Part 1, 8"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"


class jobseeker_support__transferred_15_july_2013(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "As defined in Part 1 of Schedule 4 of the Social Security Act, Part 1, 1(c)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
