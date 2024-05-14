"""This module provides eligibility and amount for Supported Living Payment."""
from functools import reduce
from operator import add, mul

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class supported_living_payment__benefit(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "The final net benefit entitlement"
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784861"

    def formula_2018_11_26(people, period, parameters):
        base_rate = people("supported_living_payment__base", period)
        abatement_rate = people("supported_living_payment__reduction", period)
        rate = numpy.clip(base_rate - abatement_rate, 0, base_rate)
        entitled = people("supported_living_payment__entitled", period)
        return entitled * rate


class supported_living_payment__reduction(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "The amount the base benefit is reduced base on the appropriate Income Test and the person & their partners income"
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784861"

    def formula_2018_11_26(people, period, parameters):
        family_income = add(
            people.family.sum(
                people.family.members("social_security__income", period),
                role=entities.Family.PARTNER),
            people.family.sum(
                people.family.members("social_security__income", period),
                role=entities.Family.PRINCIPAL))

        # numpy.floor required for income tests as it's "35c for every $1"
        family_income = numpy.floor(family_income)

        # test 1 is used if any of these clauses apply
        test_1 = reduce(add, [
            people("schedule_4__part3_1_a", period),
            people("schedule_4__part3_1_b", period),
            people("schedule_4__part3_1_c", period),
            people("schedule_4__part3_1_g_i", period),
            people("schedule_4__part3_1_g_ii", period),
            people("schedule_4__part3_1_h_i", period),
            people("schedule_4__part3_1_h_ii", period)])

        # test 2 is used if any of these clauses apply
        test_2 = reduce(add, [
            people("schedule_4__part3_1_d_i", period),
            people("schedule_4__part3_1_d_ii", period),
            people("schedule_4__part3_1_e_i", period),
            people("schedule_4__part3_1_e_ii", period),
            people("schedule_4__part3_1_f_i", period),
            people("schedule_4__part3_1_f_ii", period)])

        scale_1 = parameters(period).social_security.income_test_1
        scale_2 = parameters(period).social_security.income_test_2

        return mul(
            people("supported_living_payment__entitled", period),
            add(
                (scale_1.calc(family_income) * test_1),
                (scale_2.calc(family_income) * test_2)))

    def formula_2020_11_09(people, period, parameters):
        family_income = add(
            people.family.sum(
                people.family.members("social_security__income", period),
                role=entities.Family.PARTNER),
            people.family.sum(
                people.family.members("social_security__income", period),
                role=entities.Family.PRINCIPAL))

        # numpy.floor required for income tests as it's "35c for every $1"
        family_income = numpy.floor(family_income)

        # test 1 is used if any of these clauses apply
        test_1 = reduce(add, [
            people("schedule_4__part3_1_a", period),
            people("schedule_4__part3_1_b", period),
            people("schedule_4__part3_1_c", period),
            people("schedule_4__part3_1_g_i", period),
            people("schedule_4__part3_1_g_ii", period),
            people("schedule_4__part3_1_h_i", period),
            people("schedule_4__part3_1_h_ii", period)])

        # test 2 is used if any of these clauses apply
        test_2 = reduce(add, [
            people("schedule_4__part3_1_d_i", period),
            people("schedule_4__part3_1_d_ii", period),
            people("schedule_4__part3_1_e_i", period),
            people("schedule_4__part3_1_e_ii", period)])

        scale_1 = parameters(period).social_security.income_test_1
        scale_2 = parameters(period).social_security.income_test_2

        return mul(
            people("supported_living_payment__entitled", period),
            add(
                (scale_1.calc(family_income) * test_1),
                (scale_2.calc(family_income) * test_2)))


class supported_living_payment__base(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Supported Living Payment - Base Amount, (this is taxed and the amounts are supplied after tax, i.e. net)"

    def formula_2018_11_26(people, period, parameters):
        clauses = parameters(period.first_day).social_security.supported_living_payment.base.clauses
        # benefit = eligibility (boolean) * rate (float)
        clause_1_a_net_weekly_benefit = people("schedule_4__part3_1_a", period) * clauses["clause_1_a"]
        clause_1_b_net_weekly_benefit = people("schedule_4__part3_1_b", period) * clauses["clause_1_b"]
        clause_1_c_net_weekly_benefit = people("schedule_4__part3_1_c", period) * clauses["clause_1_c"]
        clause_1_d_i_net_weekly_benefit = people("schedule_4__part3_1_d_i", period) * clauses["clause_1_d_i"]
        clause_1_d_ii_net_weekly_benefit = people("schedule_4__part3_1_d_ii", period) * clauses["clause_1_d_i"]
        clause_1_e_i_net_weekly_benefit = people("schedule_4__part3_1_e_i", period) * clauses["clause_1_e_i"]
        clause_1_e_ii_net_weekly_benefit = people("schedule_4__part3_1_e_ii", period) * clauses["clause_1_e_ii"]
        clause_1_f_i_net_weekly_benefit = people("schedule_4__part3_1_f_i", period) * clauses["clause_1_f_i"]
        clause_1_f_ii_net_weekly_benefit = people("schedule_4__part3_1_f_ii", period) * clauses["clause_1_f_ii"]
        clause_1_g_i_net_weekly_benefit = people("schedule_4__part3_1_g_i", period) * clauses["clause_1_g_i"]
        clause_1_g_ii_net_weekly_benefit = people("schedule_4__part3_1_g_ii", period) * clauses["clause_1_g_ii"]
        clause_1_h_i_net_weekly_benefit = people("schedule_4__part3_1_h_i", period) * clauses["clause_1_h_i"]
        clause_1_h_ii_net_weekly_benefit = people("schedule_4__part3_1_h_ii", period) * clauses["clause_1_h_ii"]
        return reduce(add, [
            clause_1_a_net_weekly_benefit,
            clause_1_b_net_weekly_benefit,
            clause_1_c_net_weekly_benefit,
            clause_1_d_i_net_weekly_benefit,
            clause_1_d_ii_net_weekly_benefit,
            clause_1_e_i_net_weekly_benefit,
            clause_1_e_ii_net_weekly_benefit,
            clause_1_f_i_net_weekly_benefit,
            clause_1_f_ii_net_weekly_benefit,
            clause_1_g_i_net_weekly_benefit,
            clause_1_g_ii_net_weekly_benefit,
            clause_1_h_i_net_weekly_benefit,
            clause_1_h_ii_net_weekly_benefit])

    def formula_2020_11_09(people, period, parameters):
        clauses = parameters(period.first_day).social_security.supported_living_payment.base.clauses
        # benefit = eligibility (boolean) * rate (float)
        clause_1_a_net_weekly_benefit = people("schedule_4__part3_1_a", period) * clauses["clause_1_a"]
        clause_1_b_net_weekly_benefit = people("schedule_4__part3_1_b", period) * clauses["clause_1_b"]
        clause_1_c_net_weekly_benefit = people("schedule_4__part3_1_c", period) * clauses["clause_1_c"]
        clause_1_d_i_net_weekly_benefit = people("schedule_4__part3_1_d_i", period) * clauses["clause_1_d_i"]
        clause_1_d_ii_net_weekly_benefit = people("schedule_4__part3_1_d_ii", period) * clauses["clause_1_d_i"]
        clause_1_e_i_net_weekly_benefit = people("schedule_4__part3_1_e_i", period) * clauses["clause_1_e_i"]
        clause_1_e_ii_net_weekly_benefit = people("schedule_4__part3_1_e_ii", period) * clauses["clause_1_e_ii"]
        clause_1_g_i_net_weekly_benefit = people("schedule_4__part3_1_g_i", period) * clauses["clause_1_g_i"]
        clause_1_g_ii_net_weekly_benefit = people("schedule_4__part3_1_g_ii", period) * clauses["clause_1_g_ii"]
        clause_1_h_i_net_weekly_benefit = people("schedule_4__part3_1_h_i", period) * clauses["clause_1_h_i"]
        clause_1_h_ii_net_weekly_benefit = people("schedule_4__part3_1_h_ii", period) * clauses["clause_1_h_ii"]
        return reduce(add, [
            clause_1_a_net_weekly_benefit,
            clause_1_b_net_weekly_benefit,
            clause_1_c_net_weekly_benefit,
            clause_1_d_i_net_weekly_benefit,
            clause_1_d_ii_net_weekly_benefit,
            clause_1_e_i_net_weekly_benefit,
            clause_1_e_ii_net_weekly_benefit,
            clause_1_g_i_net_weekly_benefit,
            clause_1_g_ii_net_weekly_benefit,
            clause_1_h_i_net_weekly_benefit,
            clause_1_h_ii_net_weekly_benefit])
