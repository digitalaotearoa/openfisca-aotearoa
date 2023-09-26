"""This module provides eligibility and amount for Jobseeker Support."""

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

    def formula_2018_11_26(people, period, parameters):
        return people("sole_parent_support__entitled", period) * numpy.clip(people("sole_parent_support__base", period) - people("sole_parent_support__reduction", period), 0, people("sole_parent_support__base", period))


class sole_parent_support__base(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784854.html"
    label = "Jobseeker Support - Base Amount, (this is taxed and the amounts are supplied after tax, i.e. net)"

    def formula_2018_11_26(people, period, parameters):

        clause_1_weekly_benefit = parameters(period.first_day).social_security.sole_parent_support.base

        return people("sole_parent_support__entitled", period) * clause_1_weekly_benefit


class sole_parent_support__reduction(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "The amount the base benefit is reduced base on the appropriate Income Test and the person & their partners income"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"

    def formula_2018_11_26(people, period, parameters):
        family_income = people.family.sum(people.family.members("social_security__income", period), role=entities.Family.PARTNER) + people.family.sum(people.family.members("social_security__income", period), role=entities.Family.PRINCIPAL)

        childcare_deduction_limit = parameters(period.first_day).social_security.sole_parent_support.childcare_deduction_limit
        family_income = family_income - numpy.clip(people("sole_parent_support__weekly_childcare_cost", period), 0, childcare_deduction_limit)
        # numpy.floor required for income tests as it's "35c for every $1"
        family_income = numpy.floor(family_income)

        scale_1 = parameters(period).social_security.income_test_1
        return people("sole_parent_support__entitled", period) * scale_1.calc(family_income)


class sole_parent_support__weekly_childcare_cost(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "the cost of childcare for any of the beneficiary’s dependent children"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784854.html"
