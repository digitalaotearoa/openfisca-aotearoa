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

        rate_1 = (
            + people("schedule_4__part1_1_c", period)
        )
        rate_3 = (
            + people("schedule_4__part1_1_a", period)
            + people("schedule_4__part1_1_b", period)
            + people("schedule_4__part1_1_i", period)
            + people("schedule_4__part1_1_j", period)
        )
        rate_4 = (
            + people("schedule_4__part1_1_g", period)
            + people("schedule_4__part1_1_h", period)
        )

        # TODO: Add as parameter?
        for threshold in range (0, 999 * 100):
            if income_test_1.calc([threshold / 100]) == 0:
                income_level_c_1 = threshold / 100

            if income_test_3_b.calc([threshold / 100]) == 0:
                income_level_a = threshold / 100
                income_level_b = threshold / 100
                income_level_c_3_b = threshold / 100

            if income_test_4.calc([threshold / 100]) == 0:
                income_level_c_4 = threshold / 100

        income_level_c = (
            + rate_1 * income_level_c_1
            + rate_3 * income_level_c_3_b
            + rate_4 * income_level_c_4
        )

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
        # TODO: Add as parameter?
        ssr2018_part_2_sub_5_18_3_a = (
            + cond_a
            * numpy.maximum(
                numpy.floor(income - income_level_a) / 4,
                0,
                )
            )

        #      (b) for a sole parent, at the appropriate maximum rate in clause
        #          1(e) or (f) of Part 1 of Schedule 4 of the Act as if Income
        #          Test 3 applied to that rate instead of Income Test 1;
        cond_b = singles * (dependent_children >= 1)
        # TODO: Add as parameter?
        ssr2018_part_2_sub_5_18_3_b = (
            + cond_b
            * numpy.maximum(
                numpy.floor(income - income_level_b) / 4,
                0,
                )
            )

        #      (c) for any other applicant, at the appropriate maximum rate in
        #          Part 1 of Schedule 4 of the Act.
        cond_c = numpy.logical_not(cond_a + cond_b)
        # TODO: Add as parameter?
        ssr2018_part_2_sub_5_18_3_c = (
            + cond_c
            * numpy.maximum(
                numpy.floor(income - income_level_c) / 4,
                0,
                )
            )

        return (
            + ssr2018_part_2_sub_5_18_3_a
            + ssr2018_part_2_sub_5_18_3_b
            + ssr2018_part_2_sub_5_18_3_c
            )
