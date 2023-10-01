"""This module provides eligibility and amount for Sole parent support."""

import numpy

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from openfisca_core import holders, periods, variables

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities


class sole_parent_support__benefit(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "The final net benefit entitlement"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784854.html"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(people, period, _params):
        entitled = people("sole_parent_support__entitled", period)
        applicable_rate = people("sole_parent_support__base", period)
        abatement_rate = people("sole_parent_support__abatement", period)

        return (
            + entitled
            * numpy.clip(applicable_rate - abatement_rate, 0, applicable_rate)
            )


class sole_parent_support__base(variables.Variable):
    label = "Sole parent support — Applicable rate"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784854.html"
    documentation = """
        Base amount or applicable rate of sole parent support (this is, taxed,
        and the amounts are supplied after tax, i.e. net).
        """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.WEEK

    def formula_2018_11_26(people, period, params):
        clause_1_weekly_benefit = (
            params(period.first_day)
            .social_security
            .sole_parent_support.base
            )

        return (
            + people("sole_parent_support__entitled", period)
            * clause_1_weekly_benefit
            )


class sole_parent_support__abatement(variables.Variable):
    label = "Sole parent support — Abatement rate"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784854.html"
    documentation = """
        The amount the base benefit is reduced based on the appropriate Income
        Test and the person & their partners income.
        """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.WEEK

    def formula_2018_11_26(people, period, _params):
        return people.family("social_security__income_test_1", period)


class sole_parent_support__income(variables.Variable):
    label = "Sole parent support — Income"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784854.html"
    documentation = """Total income of the people and their partners."""
    entity = entities.Family
    value_type = float
    default_value = 0
    definition_period = periods.WEEK

    def formula_2018_11_26(families, period, params):
        # 1. To a beneficiary with 1 or more dependent children
        beneficiary_income = families.sum(
            families.members("social_security__income", period),
            role = entities.Family.PRINCIPAL,
            )

        spouse_or_partner_income = families.sum(
            families.members("social_security__income", period),
            role = entities.Family.PARTNER,
            )

        family_income = beneficiary_income + spouse_or_partner_income

        # 2. For the purposes of clause 1, MSD may disregard up to $20 a week
        #    of the beneficiary’s personal earnings used to meet the cost of
        #    childcare for any of the beneficiary’s dependent children.
        childcare_deduction_limit = (
            params(period.first_day)
            .social_security
            .sole_parent_support
            .childcare_deduction_limit
            )

        childcare_costs = families.sum(
            families.members(
                "sole_parent_support__weekly_childcare_cost",
                period,
                )
            )

        total_income = (
            + family_income
            - numpy.clip(childcare_costs, 0, childcare_deduction_limit)
            )

        return total_income


class sole_parent_support__weekly_childcare_cost(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "the cost of childcare for any of the beneficiary’s dependent children"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784854.html"
