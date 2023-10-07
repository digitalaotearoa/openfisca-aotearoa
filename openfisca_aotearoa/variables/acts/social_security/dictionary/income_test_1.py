"""This module provides the base Variable for calculation of Income Test 1.

Income Test 1 means that the applicable rate of [a] benefit must be
reduced by 30 cents for every $1 of the total income of the beneficiary and the
beneficiary’s spouse or partner that is more than $160 a week but not more than
$250 a week; and by 70 cents for every $1 of that income that is more than $250
a week.

"""

from abc import abstractmethod

# We import the required OpenFisca modules needed to define a formula.
from openfisca_core import periods, variables

# We import the required `entities` corresponding to our formulas.
from openfisca_aotearoa import entities


class social_security__income_test_1(variables.Variable):
    label = "Dictionary — Income Test 1"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784375"
    documentation = """
        Income Test 1 means that the applicable rate of [a] benefit must be
        reduced by 30 cents for every $1 of the total income of the beneficiary
        and the beneficiary’s spouse or partner that is more than $160 a week
        but not more than $250 a week; and by 70 cents for every $1 of that
        income that is more than $250 a week.
        """
    entity = entities.Family
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    @abstractmethod
    def formula_2018_11_26(families, period, params):
        raise NotImplementedError()
