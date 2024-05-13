"""This module provides eligibility and amount for Supported Living Payment."""
import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities

# rates
# reduced using "Schedule 2 Income Test 1": https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784553
# reduced using "Schedule 2 Income Test 2": https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784555


class supported_living_payment__benefit(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "The final net benefit entitlement"
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784861"

    def formula_2018_11_26(people, period, parameters):
        return people("supported_living_payment__entitled", period) * numpy.clip(
            people("supported_living_payment__base", period) - people("supported_living_payment__reduction", period),
            0,
            people("supported_living_payment__base", period)
        )


class supported_living_payment__reduction(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "The amount the base benefit is reduced base on the appropriate Income Test and the person & their partners income"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"

    def formula_2018_11_26(people, period, parameters):
        family_income = people.family.sum(people.family.members("social_security__income", period), role=entities.Family.PARTNER) + people.family.sum(people.family.members("social_security__income", period), role=entities.Family.PRINCIPAL)

        # numpy.floor required for income tests as it's "35c for every $1"
        family_income = numpy.floor(family_income)

        test_1 = people("schedule_4__part1_1_c", period) + \
            people("schedule_4__part1_1_e", period) + \
            people("schedule_4__part1_1_f", period)

        test_3 = people("schedule_4__part1_1_a", period) + \
            people("schedule_4__part1_1_b", period) + \
            people("schedule_4__part1_1_d", period) + \
            people("schedule_4__part1_1_i", period) + \
            people("schedule_4__part1_1_j", period)

        test_4 = people("schedule_4__part1_1_g", period) + \
            people("schedule_4__part1_1_h", period)

        scale_1 = parameters(period).social_security.income_test_1
        scale_3 = parameters(period).social_security.income_test_3b
        scale_4 = parameters(period).social_security.income_test_4
        return people("supported_living_payment__entitled", period) * \
            (
                (scale_1.calc(family_income) * test_1) + (scale_3.calc(family_income) * test_3) + (scale_4.calc(family_income) * test_4)
            )

    def formula_2020_11_09(people, period, parameters):
        family_income = people.family.sum(people.family.members("social_security__income", period), role=entities.Family.PARTNER) + people.family.sum(people.family.members("social_security__income", period), role=entities.Family.PRINCIPAL)

        # numpy.floor required for income tests as it's "35c for every $1"
        family_income = numpy.floor(family_income)

        test_1 = people("schedule_4__part1_1_c", period) + \
            people("schedule_4__part1_1_e", period) + \
            people("schedule_4__part1_1_f", period)

        test_3 = people("schedule_4__part1_1_a", period) + \
            people("schedule_4__part1_1_b", period) + \
            people("schedule_4__part1_1_d", period) + \
            people("schedule_4__part1_1_j", period)

        test_4 = people("schedule_4__part1_1_g", period) + \
            people("schedule_4__part1_1_h", period)

        scale_1 = parameters(period).social_security.income_test_1
        scale_3 = parameters(period).social_security.income_test_3b
        scale_4 = parameters(period).social_security.income_test_4
        return people("supported_living_payment__entitled", period) * \
            (
                (scale_1.calc(family_income) * test_1) + (scale_3.calc(family_income) * test_3) + (scale_4.calc(family_income) * test_4)
            )


class supported_living_payment__base(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Jobseeker Support - Base Amount, (this is taxed and the amounts are supplied after tax, i.e. net)"

    def formula_2018_11_26(people, period, parameters):
        clause_1_a_net_weekly_benefit = people("schedule_4__part1_1_a", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_a"])
        clause_1_b_net_weekly_benefit = people("schedule_4__part1_1_b", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_b"])
        clause_1_c_net_weekly_benefit = people("schedule_4__part1_1_c", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_c"])
        clause_1_d_i_net_weekly_benefit = people("schedule_4__part1_1_d_i", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_d_i"])
        clause_1_d_ii_net_weekly_benefit = people("schedule_4__part1_1_d_ii", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_d_i"])
        clause_1_e_i_net_weekly_benefit = people("schedule_4__part1_1_e_i", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_e_i"])
        clause_1_e_ii_net_weekly_benefit = people("schedule_4__part1_1_e_ii", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_e_ii"])
        clause_1_f_i_net_weekly_benefit = people("schedule_4__part1_1_f_i", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_f_i"])
        clause_1_f_ii_net_weekly_benefit = people("schedule_4__part1_1_f_ii", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_f_ii"])
        clause_1_g_i_net_weekly_benefit = people("schedule_4__part1_1_g_i", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_g_i"])
        clause_1_g_ii_net_weekly_benefit = people("schedule_4__part1_1_g_ii", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_g_ii"])
        clause_1_h_i_net_weekly_benefit = people("schedule_4__part1_1_h_i", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_h_i"])
        clause_1_h_ii_net_weekly_benefit = people("schedule_4__part1_1_h_ii", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_h_ii"])

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
        # Calculate the gross amount (before benefit reductions).
        #
        # Note: we're not calculating eligibility here, so the result of this
        # calculation is a "theoretical amount".
        base = clause_1_a_net_weekly_benefit + clause_1_b_net_weekly_benefit + clause_1_c_net_weekly_benefit + clause_1_d_net_weekly_benefit + clause_1_e_net_weekly_benefit + clause_1_f_net_weekly_benefit + \
            clause_1_d_i_net_weekly_benefit + clause_1_d_ii_net_weekly_benefit + \
            clause_1_e_i_net_weekly_benefit + clause_1_e_ii_net_weekly_benefit + \
            clause_1_f_i_net_weekly_benefit + clause_1_f_ii_net_weekly_benefit
            clause_1_g_i_net_weekly_benefit + clause_1_g_ii_net_weekly_benefit + \
            clause_1_h_i_net_weekly_benefit + clause_1_h_ii_net_weekly_benefit

        return base

    def formula_2020_11_09(people, period, parameters):
        clause_1_a_net_weekly_benefit = people("schedule_4__part1_1_a", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_a"])
        clause_1_b_net_weekly_benefit = people("schedule_4__part1_1_b", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_b"])
        clause_1_c_net_weekly_benefit = people("schedule_4__part1_1_c", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_c"])
        clause_1_d_net_weekly_benefit = people("schedule_4__part1_1_d", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_d"])
        clause_1_e_net_weekly_benefit = people("schedule_4__part1_1_e", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_e"])
        clause_1_f_net_weekly_benefit = people("schedule_4__part1_1_f", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_f"])
        clause_1_g_i_net_weekly_benefit = people("schedule_4__part1_1_g_i", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_g_i"])
        clause_1_g_ii_net_weekly_benefit = people("schedule_4__part1_1_g_ii", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_g_ii"])
        clause_1_h_i_net_weekly_benefit = people("schedule_4__part1_1_h_i", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_h_i"])
        clause_1_h_ii_net_weekly_benefit = people("schedule_4__part1_1_h_ii", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_h_ii"])
        clause_1_j_i_net_weekly_benefit = people("schedule_4__part1_1_j_i", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_j_i"])
        clause_1_j_ii_net_weekly_benefit = people("schedule_4__part1_1_j_ii", period) * (parameters(period.first_day).social_security.supported_living_payment.base.clauses["clause_1_j_ii"])

        # Calculate the gross amount (before benefit reductions).
        #
        # Note: we're not calculating eligibility here, so the result of this
        # calculation is a "theoretical amount".
        base = clause_1_a_net_weekly_benefit + clause_1_b_net_weekly_benefit + clause_1_c_net_weekly_benefit + clause_1_d_net_weekly_benefit + clause_1_e_net_weekly_benefit + clause_1_f_net_weekly_benefit + \
            clause_1_g_i_net_weekly_benefit + clause_1_g_ii_net_weekly_benefit + \
            clause_1_h_i_net_weekly_benefit + clause_1_h_ii_net_weekly_benefit + \
            clause_1_j_i_net_weekly_benefit + clause_1_j_ii_net_weekly_benefit

        return base


class supported_living_payment__living_with_parent(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "As defined in Part 1 of Schedule 4 of the Social Security Act, Part 1, 8"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"


class supported_living_payment__transferred_15_july_2013(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "As defined in Part 1 of Schedule 4 of the Social Security Act, Part 1, 1(c)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
