"""Jobseeker support's income tests.

The income tests are the applicable rate at which the jobseeker support
at which the benefit must be reduced.

"""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class jobseeker_support__income_test_1(variables.Variable):
    label = "Jobseeker support's income test (1)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784375"
    documentation = """
        Jobseeker support must be reduced by 30 cents for every $1 of the total
        income of the beneficiary and the beneficiary’s spouse or partner that
        is more than $160 a week but not more than $250 a week; and by 70 cents
        for every $1 of that income that is more than $250 a week.
    """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, parameters):
        family = people.family

        beneficiary_income = family.sum(
            family.members("social_security__income", period),
            role = entities.Family.PRINCIPAL,
            )

        spouse_or_partner_income = family.sum(
            family.members("social_security__income", period),
            role = entities.Family.PARTNER,
            )

        total_income = numpy.floor(
            + beneficiary_income
            + spouse_or_partner_income
        )

        income_test_1 = parameters(period).social_security.income_test_1

        return income_test_1.calc(total_income)
