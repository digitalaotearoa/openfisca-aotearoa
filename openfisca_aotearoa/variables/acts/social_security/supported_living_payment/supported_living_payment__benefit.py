"""This module provides eligibility and amount for Supported Living Payment."""

from functools import reduce

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class supported_living_payment__benefit(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "The final net benefit entitlement"
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784861"

    def formula_2018_11_26(population, period, parameters):
        # Note: the clauses in this act unfortunately apply out of order
        base_rate = population("supported_living_payment__base", period)
        abatement_rate = population("supported_living_payment__reduction", period)

        # 5. Halves benefit & abatement if in a relationship & meets these requirements
        in_relationship = population("social_security__in_a_relationship", period)
        ssa_s4_p3_5_applies = in_relationship * population("schedule_4__part3_5", period)
        base_rate = numpy.where(
            ssa_s4_p3_5_applies,
            base_rate * 0.5,
            base_rate)
        abatement_rate = numpy.where(
            ssa_s4_p3_5_applies,
            abatement_rate * 0.5,
            abatement_rate)

        # ensure the reduction does not result in a negative benefit
        benefit_post_c1 = numpy.clip(base_rate - abatement_rate, 0, base_rate)

        # 2. Maximum amount from all sources
        clauses = parameters(period.first_day).social_security.supported_living_payment.base.clauses
        couple_cap = clauses["clause_2"]
        single_cap = clauses["clause_2s"] + couple_cap

        # 3. Additional 25% of income subsidy if beneficiary is blind
        is_blind = population("totally_blind", period)
        net_income = population("social_security__income", period)
        benefit_post_s3 = benefit_post_c1 + numpy.where(is_blind, 0.25, * net_income, 0 * net_income)

        # 4. Benefit must not exceed cap from clause 2
        benefit_post_c4 = numpy.where(
            in_relationship,
            numpy.clip(benefit_post_s3, 0, couple_cap),
            numpy.clip(benefit_post_s3, 0, single_cap))

        # 6. If clause 5 applies, partner is entitled to payment 1b or 1c
        ssa_s4_6_applies = ssa_s4_p3_5_applies * population("schedule_4__part3_6", period)
        no_children = population("social_security__dependent_children", period.first_week) < 1
        has_children = population("social_security__dependent_children", period.first_week) > 0
        clauses = parameters(period.first_day).social_security.supported_living_payment.base.clauses
        ssa_s4_6 = numpy.select(
            [ssa_s4_6_applies * no_children, ssa_s4_6_applies * has_children],
            [clauses["clause_1_b"], clauses["clause_1_c"]],
            default=0)
        benefit_post_c6 = benefit_post_c4 + ssa_s4_6

        # 7. If entitled as carer & in a couple, both are entitled as carers with a separate cap
        ssa_s4_7_rate = numpy.where(
            no_children,
            clauses["clause_1_hi"],
            clauses["clause_1_hii"])
        ssa_s4_7_gross_benefit = 2 * numpy.clip(ssa_s4_7_rate - abatement_rate, 0, ssa_s4_7_rate)
        ssa_s4_7_benefit = numpy.where(
            no_children,
            numpy.clip(ssa_s4_7_gross_benefit, 0, clauses["clause_7_a"]),
            numpy.clip(ssa_s4_7_gross_benefit, 0, clauses["clause_7_b"]))

        carer_entitled = population("supported_living_payment__carer__entitled", period, parameters)

        # if the population is entitled as a carer, use the larger of c7 or other clauses
        benefit_post_c7 = numpy.where(
            carer_entitled,
            numpy.maximum(benefit_post_c6, ssa_s4_7_benefit),
            benefit_post_c6)

        # 8. A dependent child is one who is not earning orphans' or unsupported child benefits

        is_entitled = population("supported_living_payment__entitled", period)

        return is_entitled * benefit_post_c7


# note: this does not calculate exemptions as under:
#     * SSA 2018, clause 422:
#         https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783992
#     * SSR 2018, schedule 10 clause 44:
#         https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS97179
# therefore only *non-exempt* income should be entered into social_security__income
class supported_living_payment__assessable_income(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "The assessable income of the principle & partner for the purposes of income tests."
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784861"

    def formula_2018_11_26(population, period):
        # 1. Income for SLP on the basis of blindness or disability:
        #     (a) disregard that part of the beneficiary’s income (not exceeding $20 a week) earned by the beneficiary’s own efforts; and
        #     (b) disregard all of the income of a totally blind beneficiary earned by the beneficiary’s own efforts.
        gross_principal_income = population("social_security__income", period)
        principal_blind = population("totally_blind", period)
        principal_disabled = population("supported_living_payment__restricted_work_capacity", period)
        principal_abled = numpy.logical_not(numpy.logical_or(principal_blind, principal_disabled))
        principal_disabled_income = gross_principal_income - (20 * period.size_in_weeks)
        principal_limits = {
            # if a beneficiary is receiving SLP for blindness, disregard all income
            principal_blind: numpy.clip(gross_principal_income, 0, 0),
            # if a beneficiary is receiving SLP for disability, disregard a maximum of $20
            principal_disabled: numpy.clip(principal_disabled_income, 0, principal_disabled_income),
            # otherwise, use the gross principal income
            principal_abled: gross_principal_income}
        # income based on whether principal population members are blind, disabled, or neither
        assessable_principal_income = numpy.select(list(principal_limits.keys()), list(principal_limits.values()))

        gross_partner_income = population.partner("social_security__income", period)
        partner_blind = population.partner("totally_blind", period)
        partner_disabled = population.partner("supported_living_payment__restricted_work_capacity", period)
        partner_abled = numpy.logical_not(numpy.logical_or(partner_blind, partner_disabled))
        partner_disabled_income = gross_partner_income - (20 * period.size_in_weeks)
        partner_limits = {
            # if a beneficiary is receiving SLP for blindness, disregard all income
            partner_blind: numpy.clip(gross_partner_income, 0, 0),
            # if a beneficiary is receiving SLP for disability, disregard a maximum of $20
            partner_disabled: numpy.clip(partner_disabled_income, 0, partner_disabled_income),
            # otherwise, use the gross principal income
            partner_abled: gross_partner_income}
        # income based on whether partner population members are blind, disabled, or neither
        assessable_partner_income = numpy.select(list(partner_limits.keys()), list(partner_limits.values()))

        # numpy.floor required for income tests; reductions are per whole dollar
        return numpy.floor(assessable_principal_income + assessable_partner_income)


class supported_living_payment__reduction(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "The amount the base benefit is reduced base on the appropriate Income Test and the person & their partners income"
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784861"

    def formula_2018_11_26(population, period, parameters):
        family_income = population("supported_living_payment__assessable_income", period)

        # test 1 is used if any of these clauses apply
        test_1_applies = reduce(numpy.logical_or, [
            population("schedule_4__part3_1_a", period),
            population("schedule_4__part3_1_b", period),
            population("schedule_4__part3_1_c", period),
            population("schedule_4__part3_1_g_i", period),
            population("schedule_4__part3_1_g_ii", period),
            population("schedule_4__part3_1_h_i", period),
            population("schedule_4__part3_1_h_ii", period)])

        # test 2 is used if any of these clauses apply
        test_2_applies = reduce(numpy.logical_or, [
            population("schedule_4__part3_1_d_i", period),
            population("schedule_4__part3_1_d_ii", period),
            population("schedule_4__part3_1_e_i", period),
            population("schedule_4__part3_1_e_ii", period),
            population("schedule_4__part3_1_f_i", period),
            population("schedule_4__part3_1_f_ii", period)])

        income_test_1 = parameters(period).social_security.income_test_1
        income_test_2 = parameters(period).social_security.income_test_2

        abatement = numpy.select(
            [test_1_applies, test_2_applies],
            [income_test_1.calc(family_income), income_test_2.calc(family_income)])

        # 5. Halves benefit & abatement if in a relationship & meets these requirements
        in_relationship = population("social_security__in_a_relationship", period)
        ssa_s4_5_applies = population("schedule_4__part3_5", period)
        return numpy.where(
            in_relationship * ssa_s4_5_applies,
            abatement * 0.5,
            abatement)

    def formula_2020_11_09(population, period, parameters):
        family_income = population("supported_living_payment__assessable_income", period)

        # test 1 is used if any of these clauses apply
        test_1_applies = reduce(numpy.logical_or, [
            population("schedule_4__part3_1_a", period),
            population("schedule_4__part3_1_b", period),
            population("schedule_4__part3_1_c", period),
            population("schedule_4__part3_1_g_i", period),
            population("schedule_4__part3_1_g_ii", period),
            population("schedule_4__part3_1_h_i", period),
            population("schedule_4__part3_1_h_ii", period)])

        # test 2 is used if any of these clauses apply
        test_2_applies = reduce(numpy.logical_or, [
            population("schedule_4__part3_1_d_i", period),
            population("schedule_4__part3_1_d_ii", period),
            population("schedule_4__part3_1_e_i", period),
            population("schedule_4__part3_1_e_ii", period)])

        income_test_1 = parameters(period).social_security.income_test_1
        income_test_2 = parameters(period).social_security.income_test_2

        abatement = numpy.select(
            [test_1_applies, test_2_applies],
            [income_test_1.calc(family_income), income_test_2.calc(family_income)])

        # 5. Halves benefit & abatement if in a relationship & meets these requirements
        in_relationship = population("social_security__in_a_relationship", period)
        ssa_s4_5_applies = population("schedule_4__part3_5", period)
        return numpy.where(
            in_relationship * ssa_s4_5_applies,
            abatement * 0.5,
            abatement)


class supported_living_payment__base(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Supported Living Payment - Base Amount, (this is taxed and the amounts are supplied after tax, i.e. net)"

    def formula_2018_11_26(population, period, parameters):
        clauses = parameters(period.first_day).social_security.supported_living_payment.base.clauses
        base_rate = numpy.select([
            population("schedule_4__part3_1_a", period),
            population("schedule_4__part3_1_b", period),
            population("schedule_4__part3_1_c", period),
            population("schedule_4__part3_1_d_i", period),
            population("schedule_4__part3_1_d_ii", period),
            population("schedule_4__part3_1_e_i", period),
            population("schedule_4__part3_1_e_ii", period),
            population("schedule_4__part3_1_f_i", period),
            population("schedule_4__part3_1_f_ii", period),
            population("schedule_4__part3_1_g_i", period),
            population("schedule_4__part3_1_g_ii", period),
            population("schedule_4__part3_1_h_i", period),
            population("schedule_4__part3_1_h_ii", period),
            ], [
            clauses["clause_1_a"],
            clauses["clause_1_b"],
            clauses["clause_1_c"],
            clauses["clause_1_d_i"],
            clauses["clause_1_d_i"],
            clauses["clause_1_e_i"],
            clauses["clause_1_e_ii"],
            clauses["clause_1_f_i"],
            clauses["clause_1_f_ii"],
            clauses["clause_1_g_i"],
            clauses["clause_1_g_ii"],
            clauses["clause_1_h_i"],
            clauses["clause_1_h_ii"],
            ])

        # 5. Halves benefit & abatement if in a relationship & meets these requirements
        in_relationship = population("social_security__in_a_relationship", period)
        ssa_s4_5_applies = population("schedule_4__part3_5", period)
        return numpy.where(
            in_relationship * ssa_s4_5_applies,
            base_rate * 0.5,
            base_rate)

    def formula_2020_11_09(population, period, parameters):
        clauses = parameters(period.first_day).social_security.supported_living_payment.base.clauses
        base_rate = numpy.select([
            population("schedule_4__part3_1_a", period),
            population("schedule_4__part3_1_b", period),
            population("schedule_4__part3_1_c", period),
            population("schedule_4__part3_1_d_i", period),
            population("schedule_4__part3_1_d_ii", period),
            population("schedule_4__part3_1_e_i", period),
            population("schedule_4__part3_1_e_ii", period),
            population("schedule_4__part3_1_g_i", period),
            population("schedule_4__part3_1_g_ii", period),
            population("schedule_4__part3_1_h_i", period),
            population("schedule_4__part3_1_h_ii", period),
            ], [
            clauses["clause_1_a"],
            clauses["clause_1_b"],
            clauses["clause_1_c"],
            clauses["clause_1_d_i"],
            clauses["clause_1_d_i"],
            clauses["clause_1_e_i"],
            clauses["clause_1_e_ii"],
            clauses["clause_1_g_i"],
            clauses["clause_1_g_ii"],
            clauses["clause_1_h_i"],
            clauses["clause_1_h_ii"],
            ])

        # 5. Halves benefit & abatement if in a relationship & meets these requirements
        in_relationship = population("social_security__in_a_relationship", period)
        ssa_s4_5_applies = population("schedule_4__part3_5", period)
        return numpy.where(
            in_relationship * ssa_s4_5_applies,
            base_rate * 0.5,
            base_rate)
