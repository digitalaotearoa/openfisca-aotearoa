"""This module provides the calculation of Income Test 3.

Income Test 3 means that the applicable rate of [a] benefit must be reduced by
70 cents for every $1 of total income of the beneficiary and the beneficiary’s
spouse or partner that is more than, if the rate of benefit is a rate of New
Zealand superannuation stated in clause 1 of Part 2 of Schedule 1 of the New
Zealand Superannuation and Retirement Income Act 2001, $160 a week; or
in any other case, $160 a week.

"""

# We import `inspect` to know where is this `variable` being called from.
import inspect
# We import `os` to provide a useful error message when a benefit is not valid.
import os

# We import numpy to use its `floor` function, needed for income tests as i.e.
# we need to reduce x¢ for every $y".
import numpy

# We import the required OpenFisca modules needed to define a formula.
from openfisca_core import periods, variables

# We import the required `entities` corresponding to our formulas.
from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.exegesis.income_tested_benefit import (
    IncomeTestedBenefit,
    )


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

    def formula_2018_11_26(families, period, params):
        # Income Test 3 means that the applicable rate of benefit must be
        # reduced—

        # List of people with families.
        people = families.members

        # Where is this income-test being called from.
        callers = [frame.filename for frame in inspect.stack()[5:7]]

        for benefit in IncomeTestedBenefit:
            for caller in callers:
                if benefit.name in caller:
                    applicable_rate = families.sum(
                        people(f"{benefit.name}__base", period),
                        role = entities.Family.PRINCIPAL,
                        )

                    # by 70 cents for every $1 of total income of the
                    # beneficiary and the beneficiary’s spouse or partner that
                    # is more than,—
                    total_income = families(f"{benefit.name}__income", period)

                    # Required for income tests as i.e. x¢ for every $y.
                    floor = numpy.floor(total_income)

                    # (a) if the rate of benefit is a rate of New Zealand
                    #     superannuation stated in clause 1 of Part 2 of
                    #     Schedule 1 of the New Zealand Superannuation and
                    #     Retirement Income Act 2001, $160 a week; or
                    if benefit.name in ("superannuation", "veterans_pension"):
                        scale = (
                            params(period)
                            .social_security
                            .dictionary
                            .income_test_3a
                            )

                    # (b) in any other case, $160 a week
                    else:
                        scale = (
                            params(period)
                            .social_security
                            .dictionary
                            .income_test_3b
                            )

                    # The abatement rate regardless of benefit rate.
                    abatement_rate = scale.calc(floor)

                    # The abatement rate capped at the applicable benefit rate.
                    return numpy.minimum(abatement_rate, applicable_rate)

        raise InvalidBenefitError(callers)


class InvalidBenefitError(NotImplementedError):
    """Raise when a benefit is not valid for an income test."""

    def __init__(self, callers):
        message = "The provided files do not contain an income-tested benefit:"
        super().__init__(os.linesep.join([message, *callers]))
