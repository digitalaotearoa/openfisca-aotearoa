"""This module provides gross amount for Jobseeker Support."""

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from openfisca_core.periods import DateUnit
from openfisca_core.variables import Variable

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa.entities import Person

# We define the `jobseeker_support__gross` variable.
#
# Please note that by itself a `variable` is not a rule but just a
# specification of such a rule.
#
# A `variable` can contain several rules, otherwise called `formulas`, that is,
# several ways it can be calculated, depending on ther date at which we want to
# calculate it. Said otherwise, as a `concept`, any modelled benefit like
# `jobseeker_support` exist since big bang until big crunch, yet the way of
#  calculating it depends on the applicable law at the requested `period`.
#
# For more information on OpenFisca's `variables`:
# https://openfisca.org/doc/key-concepts/variables.html
class jobseeker_support__gross(Variable):
    value_type = float
    entity = Person
    definition_period = DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Jobseeker Support - Gross Amount"
    documentation = """
        Schedule 4 - Rates of benefits
        Part 1 -  Jobseeker support

        1   (a) To a single beneficiary under the age of 20 years who is—
                (i)     living with a parent (as that term is defined in clause
                        8); and
                (ii)    whose benefit commenced on or after 1 July 1998
        """

    def formula_2013_07_15(people, period, parameters):
        # Get `single` for each person in `people` at `period`, where `period`
        # is "forever", as in "Are you single now?"
        single = people("single", DateUnit.ETERNITY)

        # Get `age` for each person in `people` at `period`, where `period` is
        # the last day of last week.
        #
        # The value of `period` can either be represent an `instant`, like
        # `yesterday`, `last month`, `two years ago`; or a `period`, like
        # `last year's first quarter` (which translates to last year's first
        # three months), `over the last three years`, etc.
        age = people("age", period.first_day.offset(-1))

        # Get `living_with_parent_or_guardian` for each person in `people` at
        # `period`, where `period` is the month of last day of last week.
        living_with_parent_or_guardian = people(
            "living_with_parent_or_guardian",
            period.first_day.offset(-1).first_month,
            )

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
            * (age < 20)
            * living_with_parent_or_guardian
            * net_weekly_benefit
            )
