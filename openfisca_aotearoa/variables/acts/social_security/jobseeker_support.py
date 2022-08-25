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


# We define the `jobseeker_support` variable.
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
class jobseeker_support(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DAY
    label = "Jobseeker Support eligibility and amount"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783144"

    # Define how to calculate `jobseeker_support`.
    #
    # We're defining the `formula` for `jobseeker_support` with the suffix
    # `2013_07_15`, because that's the date at which the `jobseeker_support`
    # benefit commenced.
    #
    # For more information on OpenFisca's formulas and their evolution:
    # https://openfisca.org/doc/coding-the-legislation/40_legislation_evolutions.html?highlight=dated#formula-evolution
    def formula_2013_07_15(people, period, parameters):
        # Calculate `work_gap` for each person in `people` at `period`.
        #
        # It is called `people` and not `person` because it actually contains
        # an collection of `person`, also known a `vector`.
        #
        # For more information on OpenFisca's vectorial computing:
        # https://openfisca.org/doc/coding-the-legislation/25_vectorial_computing.html
        work_gap = people("work_gap", period)

        # Get `age` for each person in `people` at `period`.
        #
        # The value of `period` can either be represent an `instant`, like
        # `yesterday`, `last month`, `two years ago`; or a `period`, like
        # `last year's first quarter` (which translates to last year's first
        # three months), `over the last three years`, etc.
        #
        # In this case, we want to know how old people where, are, or will be
        # at the `instant` of application of the calculation, for example the
        # date of the day at which they request Jobseeker Support.
        #
        # For more information on OpenFisca's `periods` and `instants`:
        # https://openfisca.org/doc/key-concepts/periodsinstants.html
        age = people("age", period)

        # Calculate `net_weekly_benefit` for each age `age` at `period`.
        #
        # We are using a special type or built-in parameter called
        # `single_amount`, that allowa us to find the corresponding
        # `net_weekly_benefit` from a continuous data input.
        #
        # For more information on OpenFisca `scales`:
        # https://openfisca.org/doc/coding-the-legislation/legislation_parameters.html?highlight=rates#creating-scales
        net_weekly_benefit = (
            parameters(period)
            .jobseeker_support
            .net_weekly_benefit
            .calc(age)
            )

        # Calculate eligibility and amount of Jobseeker Support.
        return work_gap * net_weekly_benefit


class jobseeker_support__below_income_threshold(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Income is below Job Seeker Support threshold?"
    definition_period = periods.MONTH