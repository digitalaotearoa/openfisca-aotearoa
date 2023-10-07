"""This module provides the calculation of Superannuation's Income Tests."""

import numpy

from openfisca_core import periods

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.acts.social_security import dictionary


class superannuation__income_test_1(dictionary.social_security__income_test_1):
    label = "Superannuation — Income Test 1"
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

    def formula_2018_11_26(families, period, params):
        # Income Test 1 means that the applicable rate of [a] benefit must be
        # reduced—

        # List of people with families.
        people = families.members

        applicable_rate = families.sum(
            people("superannuation__base", period),
            role = entities.Family.PRINCIPAL,
            )

        # (a) by 30 cents for every $1 of the total income of the beneficiary
        #     and the beneficiary’s spouse or partner that is more than $160 a
        #     week but not more than $250 a week; and
        total_income = families("superannuation__income", period)

        # Required for income tests as i.e. x¢ for every $y.
        floor = numpy.floor(total_income)

        # (b) by 70 cents for every $1 of that income that is more than $250 a
        # week
        scale = params(period).social_security.dictionary.income_test_1

        # The abatement rate regardless of benefit rate.
        abatement_rate = scale.calc(floor)

        # The abatement rate capped at the applicable benefit rate.
        return numpy.minimum(abatement_rate, applicable_rate)


class superannuation__income_test_2(dictionary.social_security__income_test_1):
    label = "Superannuation — Income Test 2"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784375"
    documentation = """
        Income Test 2 means that the applicable rate of [a] benefit must be
        reduced by 15 cents for every $1 of the total income of the beneficiary
        and the beneficiary’s spouse or partner that is more than $160 a week
        but not more than $250 a week; and by 35 cents for every $1 of that
        income that is more than $250 a week.
        """
    entity = entities.Family
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(families, period, params):
        # Income Test 2 means that the applicable rate of benefit must be
        # reduced—

        # List of people with families.
        people = families.members

        applicable_rate = families.sum(
            people("superannuation__base", period),
            role = entities.Family.PRINCIPAL,
            )

        # (a) by 15 cents for every $1 of the total income of the beneficiary
        #     and the beneficiary’s spouse or partner that is more than $160 a
        #     week but not more than $250 a week; and
        total_income = families("superannuation__income", period)

        # Required for income tests as i.e. x¢ for every $y.
        floor = numpy.floor(total_income)

        # (b) by 35 cents for every $1 of that income that is more than $250 a
        #     week
        scale = params(period).social_security.dictionary.income_test_2

        # The abatement rate regardless of benefit rate.
        abatement_rate = scale.calc(floor)

        # The abatement rate capped at the applicable benefit rate.
        return numpy.minimum(abatement_rate, applicable_rate)


class superannuation__income_test_3(dictionary.social_security__income_test_3):
    label = "Superannuation — Income Test 3"
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

        applicable_rate = families.sum(
            people("superannuation__base", period),
            role = entities.Family.PRINCIPAL,
            )

        # by 70 cents for every $1 of total income of the
        # beneficiary and the beneficiary’s spouse or partner that
        # is more than,—
        total_income = families("superannuation__income", period)

        # Required for income tests as i.e. x¢ for every $y.
        floor = numpy.floor(total_income)

        # (a) if the rate of benefit is a rate of New Zealand
        #     superannuation stated in clause 1 of Part 2 of
        #     Schedule 1 of the New Zealand Superannuation and
        #     Retirement Income Act 2001, $160 a week; or
        # (b) in any other case, $160 a week
        scale = params(period).social_security.dictionary.income_test_3a

        # The abatement rate regardless of benefit rate.
        abatement_rate = scale.calc(floor)

        # The abatement rate capped at the applicable benefit rate.
        return numpy.minimum(abatement_rate, applicable_rate)


class superannuation__income_test_4(dictionary.social_security__income_test_4):
    label = "Superannuation — Income Test 4"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784375"
    documentation = """
        Income Test 4 means that the applicable rate of [a] benefit must be
        reduced by 35 cents for every $1 of the total income of the beneficiary
        and the beneficiary’s spouse or partner that is more than $160 a week.
        """
    entity = entities.Family
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(families, period, params):
        # Income Test 4 means that the applicable rate of [a] benefit must be
        # reduced

        # List of people with families.
        people = families.members

        applicable_rate = families.sum(
            people("superannuation__base", period),
            role = entities.Family.PRINCIPAL,
            )

        # by 35 cents for every $1 of the total income of the
        # beneficiary and the beneficiary’s spouse or partner that
        # is more than $160 a week.
        total_income = families("superannuation__income", period)

        # Required for income tests as i.e. x¢ for every $y.
        floor = numpy.floor(total_income)

        scale = params(period).social_security.dictionary.income_test_4

        # The abatement rate regardless of benefit rate.
        abatement_rate = scale.calc(floor)

        # The abatement rate capped at the applicable benefit rate.
        return numpy.minimum(abatement_rate, applicable_rate)
