"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class accommodation_supplement__reduction(variables.Variable):
    label = "Income-based reductions"
    reference = "https://legislation.govt.nz/regulation/public/2018/0202/latest/LMS96265.html"
    documentation = """TODO"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, parameters):
        principal = people.has_role(entities.Family.PRINCIPAL)
        mingled = principal * people("social_security__in_a_relationship", period)
        singles = principal * numpy.logical_not(mingled)
        dependent_children = people("social_security__dependent_children", period)
        income_test_1 = parameters(period).social_security.income_test_1
        income_test_3_b = parameters(period).social_security.income_test_3b
        income_test_4 = parameters(period).social_security.income_test_4

        # (1) This regulation applies to the amount of accommodation supplement
        #     assessed—
        #     (a) under subpart 10 of Part 2 and Part 7 of Schedule 4 of the
        #         Act and these regulations; and
        #     (b) for a non-beneficiary (as defined in regulation 17).

        # TODO

        # (2) That amount must be reduced by 25 cents for every $1 of the
        #     relevant weekly income (see subclause (2A)) in excess of the
        #     income level specified in subclause (3).

        # (2A) Relevant weekly income
        income = people("accommodation_supplement__relevant_weekly_income", period)

        # (3)  The income level mentioned in subclause (2) is the amount of
        #      income that would prevent payment of jobseeker support,—

        #      (a) for a single applicant without dependent children, at the
        #          maximum rate in clause 1(d) of Part 1 of Schedule 4 of the
        #          Act;
        cond_a = singles * (dependent_children == 0)
        level_a = income_test_1.thresholds[1]
        # TODO: Add to parameters
        amount_a = numpy.maximum(numpy.floor(income - level_a) / 4, 0)
        ssr2018_part_2_sub_5_18_3_a = cond_a * amount_a

        #      (b) for a sole parent, at the appropriate maximum rate in clause
        #          1(e) or (f) of Part 1 of Schedule 4 of the Act as if Income
        #          Test 3 applied to that rate instead of Income Test 1;
        cond_b = singles * (dependent_children >= 1)
        level_b = income_test_1.thresholds[1]
        # TODO: Add to parameters
        amount_b = numpy.maximum(numpy.floor(income - level_b) / 4, 0)
        ssr2018_part_2_sub_5_18_3_b = cond_b * amount_b

        #      (c) for any other applicant, at the appropriate maximum rate in
        #          Part 1 of Schedule 4 of the Act.
        cond_c = numpy.logical_not(cond_a + cond_b)

        # TODO: Factor out into a function?
        rate_1 = (
            + people("schedule_4__part1_1_c", period)
            )

        # TODO: Factor out into a function?
        rate_3 = (
            + people("schedule_4__part1_1_a", period)
            + people("schedule_4__part1_1_b", period)
            + people("schedule_4__part1_1_i", period)
            + people("schedule_4__part1_1_j", period)
            )

        # TODO: Factor out into a function?
        rate_4 = (
            + people("schedule_4__part1_1_g", period)
            + people("schedule_4__part1_1_h", period)
            )

        # TODO: Factor out into a function?
        level_c = (
            + rate_1 * income_test_1.thresholds[1]
            + rate_3 * income_test_3_b.thresholds[1]
            + rate_4 * income_test_4.thresholds[1]
            )

        # TODO: Add as parameter?
        amount_c = numpy.maximum(numpy.floor(income - level_c) / 4, 0)
        ssr2018_part_2_sub_5_18_3_c = cond_c * amount_c

        return (
            + ssr2018_part_2_sub_5_18_3_a
            + ssr2018_part_2_sub_5_18_3_b
            + ssr2018_part_2_sub_5_18_3_c
            )

    def formula_2020_11_09(people, period, parameters):
        principal = people.has_role(entities.Family.PRINCIPAL)
        mingled = principal * people("social_security__in_a_relationship", period)
        singles = principal * numpy.logical_not(mingled)
        dependent_children = people("social_security__dependent_children", period)
        income_test_1 = parameters(period).social_security.income_test_1
        income_test_3_b = parameters(period).social_security.income_test_3b
        income_test_4 = parameters(period).social_security.income_test_4

        # (1) This regulation applies to the amount of accommodation supplement
        #     assessed—
        #     (a) under subpart 10 of Part 2 and Part 7 of Schedule 4 of the
        #         Act and these regulations; and
        #     (b) for a non-beneficiary (as defined in regulation 17).

        # TODO

        # (2) That amount must be reduced by 25 cents for every $1 of the
        #     relevant weekly income (see subclause (2A)) in excess of the
        #     income level specified in subclause (3).

        # (2A) Relevant weekly income
        income = people("accommodation_supplement__relevant_weekly_income", period)

        # (3)  The income level mentioned in subclause (2) is the amount of
        #      income that would prevent payment of jobseeker support,—

        #      (a) for a single applicant without dependent children, at the
        #          maximum rate in clause 1(d) of Part 1 of Schedule 4 of the
        #          Act;
        cond_a = singles * (dependent_children == 0)
        level_a = income_test_1.thresholds[1]
        # TODO: Add to parameters
        amount_a = numpy.maximum(numpy.floor(income - level_a) / 4, 0)
        ssr2018_part_2_sub_5_18_3_a = cond_a * amount_a

        #      (b) for a sole parent, at the appropriate maximum rate in clause
        #          1(e) or (f) of Part 1 of Schedule 4 of the Act as if Income
        #          Test 3 applied to that rate instead of Income Test 1;
        cond_b = singles * (dependent_children >= 1)
        level_b = income_test_1.thresholds[1]
        # TODO: Add to parameters
        amount_b = numpy.maximum(numpy.floor(income - level_b) / 4, 0)
        ssr2018_part_2_sub_5_18_3_b = cond_b * amount_b

        #      (c) for any other applicant, at the appropriate maximum rate in
        #          Part 1 of Schedule 4 of the Act.
        cond_c = numpy.logical_not(cond_a + cond_b)

        # TODO: Factor out into a function?
        rate_1 = (
            + people("schedule_4__part1_1_c", period)
            )

        # TODO: Factor out into a function?
        rate_3 = (
            + people("schedule_4__part1_1_a", period)
            + people("schedule_4__part1_1_b", period)
            + people("schedule_4__part1_1_j", period)
            )

        # TODO: Factor out into a function?
        rate_4 = (
            + people("schedule_4__part1_1_g", period)
            + people("schedule_4__part1_1_h", period)
            )

        # TODO: Factor out into a function?
        level_c = (
            + rate_1 * income_test_1.thresholds[1]
            + rate_3 * income_test_3_b.thresholds[1]
            + rate_4 * income_test_4.thresholds[1]
            )

        # TODO: Add as parameter?
        amount_c = numpy.maximum(numpy.floor(income - level_c) / 4, 0)
        ssr2018_part_2_sub_5_18_3_c = cond_c * amount_c

        return (
            + ssr2018_part_2_sub_5_18_3_a
            + ssr2018_part_2_sub_5_18_3_b
            + ssr2018_part_2_sub_5_18_3_c
            )
