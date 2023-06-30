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
        testable_income = people("jobseeker_support__testable_income", period)
        income_test_1 = parameters(period).social_security.income_test_1
        return income_test_1.calc(numpy.floor(testable_income))


class jobseeker_support__income_test_2(variables.Variable):
    label = "Jobseeker support's income test (2)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784375"
    documentation = """
        Jobseeker support must be reduced by 15 cents for every $1 of the total
        income of the beneficiary and the beneficiary’s spouse or partner that
        is more than $160 a week but not more than $250 a week; and by 35 cents
        for every $1 of that income that is more than $250 a week.
    """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, parameters):
        testable_income = people("jobseeker_support__testable_income", period)
        income_test_2 = parameters(period).social_security.income_test_2
        return income_test_2.calc(numpy.floor(testable_income))


class jobseeker_support__income_test_3_b(variables.Variable):
    label = "Jobseeker support's income test (3) (b)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784375"
    documentation = """
        Jobseeker support must be reduced by 70 cents for every $1 of the total
        income of the beneficiary and the beneficiary’s spouse or partner that
        is more than $160 a week.
    """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, parameters):
        testable_income = people("jobseeker_support__testable_income", period)
        income_test_3_b = parameters(period).social_security.income_test_3b
        return income_test_3_b.calc(numpy.floor(testable_income))


class jobseeker_support__income_test_4(variables.Variable):
    label = "Jobseeker support's income test (4)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784375"
    documentation = """
        Jobseeker support must be reduced by 35 cents for every $1 of the total
        income of the beneficiary and the beneficiary’s spouse or partner that
        is more than $160 a week.
    """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, parameters):
        testable_income = people("jobseeker_support__testable_income", period)
        income_test_4 = parameters(period).social_security.income_test_4
        return income_test_4.calc(numpy.floor(testable_income))
