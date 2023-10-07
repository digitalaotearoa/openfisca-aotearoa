"""Jobseeker Support — Abatement.

The amount the base benefit is reduced based on the appropriate Income Test and
the person & their partners income.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class jobseeker_support__abatement(variables.Variable):
    label = "Jobseeker Support — Abatement"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    documentation = """
        The amount the base benefit is reduced based on the appropriate Income
        Test and the person & their partners income.
        """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.WEEK

    def formula_2018_11_26(people, period, _params):
        families = people.family

        case_1 = (
            + people("schedule_4__part1_1_c", period)
            + people("schedule_4__part1_1_e", period)
            + people("schedule_4__part1_1_f", period)
            )

        case_3 = (
            + people("schedule_4__part1_1_a", period)
            + people("schedule_4__part1_1_b", period)
            + people("schedule_4__part1_1_d", period)
            + people("schedule_4__part1_1_i", period)
            + people("schedule_4__part1_1_j", period)
            )

        case_4 = (
            + people("schedule_4__part1_1_g", period)
            + people("schedule_4__part1_1_h", period)
            )

        income_test_1 = families("jobseeker_support__income_test_1", period)
        income_test_3 = families("jobseeker_support__income_test_3", period)
        income_test_4 = families("jobseeker_support__income_test_4", period)

        return (
            + case_1 * income_test_1
            + case_3 * income_test_3
            + case_4 * income_test_4
            )

    def formula_2020_11_09(people, period, _params):
        families = people.family

        case_1 = (
            + people("schedule_4__part1_1_c", period)
            + people("schedule_4__part1_1_e", period)
            + people("schedule_4__part1_1_f", period)
            )

        case_3 = (
            + people("schedule_4__part1_1_a", period)
            + people("schedule_4__part1_1_b", period)
            + people("schedule_4__part1_1_d", period)
            + people("schedule_4__part1_1_j", period)
            )

        case_4 = (
            + people("schedule_4__part1_1_g", period)
            + people("schedule_4__part1_1_h", period)
            )

        income_test_1 = families("jobseeker_support__income_test_1", period)
        income_test_3 = families("jobseeker_support__income_test_3", period)
        income_test_4 = families("jobseeker_support__income_test_4", period)

        return (
            + case_1 * income_test_1
            + case_3 * income_test_3
            + case_4 * income_test_4
            )
