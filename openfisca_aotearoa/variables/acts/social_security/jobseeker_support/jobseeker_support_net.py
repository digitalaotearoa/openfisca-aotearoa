"""This module provides eligibility and amount for Jobseeker Support."""

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from openfisca_core import periods, variables

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities

import numpy

from openfisca_core import holders


class jobseeker_support__net(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = ""
    reference = ""


class jobseeker_support__gross(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Jobseeker Support - Gross Amount"

    # What is this date significance?
    def formula_2013_07_15(people, period, parameters):
        # Get `single` for each person in `people` at `period`, where `period`
        # is "forever", as in "Are you single now?"
        single = numpy.logical_not(people("person_has_partner", periods.DateUnit.ETERNITY))
        age = people("age", period.first_day)


        part1_a =  single * (age < 20) * \
            people("jobseeker_support__living_with_parent", period)

        # part1_a_ii this could not be true any more? 1998 is more than 20 years ago

        part1_b = single * (age < 25) * \
            numpy.logical_not(people("social_security__person_has_dependent_child", period.first_month ))


        # Get `age` for each person in `people` at `period`, where `period` is
        # the last day of last week.
        age = people("age", period.first_day)

        # Get `living_with_parent_or_guardian` for each person in `people` at
        # `period`, where `period` is the month of last day of last week.
        part1_8 = people("jobseeker_support__living_with_parent", period.first_month)

        # Get `dependent_child` for each person in `people` at `period`, where
        # `period` is the month of last day of last week.
        dependent_child =

        # Calculate `net_weekly_benefit` for each age `age` at `period`, where
        # `period` is the last day of last week.
        #
        # We are using a special type or built-in parameter called
        # `single_amount`, that allows us to find the corresponding
        # `net_weekly_benefit` from a continuous data input.
        #
        # For more information on OpenFisca `scales`:
        # https://openfisca.org/doc/coding-the-legislation/legislation_parameters.html?highlight=rates#creating-scales
        net_weekly_benefit = (
            parameters(period.first_day.offset(-1))
            .jobseeker_support
            .net_weekly_benefit
            .calc(age)
            )

        # Calculate the gross amount (before benefit reductions).
        #
        # Note: we're not calculating eligibility here, so the result of this
        # calculation is a "theoretical amount".
        return (
            + single
            * (
                + (age < 20) * living_with_parent_or_guardian
                + (age < 25) * numpy.logical_not(dependent_child)
                + (age >= 25) * numpy.logical_not(dependent_child)
                )
            * net_weekly_benefit
            )


class jobseeker_support__cutoff(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = ""
    reference = ""


class jobseeker_support__reduction(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = ""
    reference = ""


class jobseeker_support__living_with_parent(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.WEEK
    label = "As defined in Part 1 of Schedule 4 of the Social Security Act"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"

