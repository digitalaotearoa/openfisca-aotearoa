"""This module provides the calculation of Income Test 3.

Income Test 3 means that the applicable rate of [a] benefit must be reduced by
70 cents for every $1 of total income of the beneficiary and the beneficiary’s
spouse or partner that is more than, if the rate of benefit is a rate of New
Zealand superannuation stated in clause 1 of Part 2 of Schedule 1 of the New
Zealand Superannuation and Retirement Income Act 2001, $160 a week; or
in any other case, $160 a week.

"""

from abc import abstractmethod

# We import the required OpenFisca modules needed to define a formula.
from openfisca_core import periods, variables

# We import the required `entities` corresponding to our formulas.
from openfisca_aotearoa import entities


class social_security__income_test_3(variables.Variable):
    label = "Dictionary — Income Test 3"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784375"
    documentation = """
        Income Test 3 means that the applicable rate of [a] benefit must be
        reduced by 70 cents for every $1 of total income of the beneficiary and
        the beneficiary’s spouse or partner that is more than, if the rate of
        benefit is a rate of New Zealand superannuation stated in clause 1 of
        Part 2 of Schedule 1 of the New Zealand Superannuation and Retirement
        Income Act 2001, $160 a week; or in any other case, $160 a week.
        """
    entity = entities.Family
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    @abstractmethod
    def formula_2018_11_26(families, period, params):
        raise NotImplementedError()
