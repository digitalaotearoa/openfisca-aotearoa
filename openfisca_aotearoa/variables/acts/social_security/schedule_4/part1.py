"""This module provides eligibility and amount for Jobseeker Support."""

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
import numpy

from openfisca_core import periods, variables

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities


class schedule_4__part1_1_a(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(a)"

    def formula_2018_11_26(people, period, parameters):
        # Get `single` for each person in `people` at `period`, where `period`
        # is "forever", as in "Are you single now?"
        single = numpy.logical_not(people("in_a_relationship", period))
        age = people("age", period.first_day)

        clause_1_a_i = single * (age < 20) * people("jobseeker_support__living_with_parent", period)
        # clause_1_a_ii TODO specific exclusion for benefits commenced before 1 July 1998

        return clause_1_a_i


class schedule_4__part1_1_b(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(b)"

    def formula_2018_11_26(people, period, parameters):
        single = numpy.logical_not(people("in_a_relationship", period))
        age = people("age", period.first_day)

        return numpy.logical_not(people("schedule_4__part1_1_a", period)) * \
            single * (age < 25) * \
            (people("social_security__dependent_children", period) == 0)


class schedule_4__part1_1_c(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(c)"

    def formula_2018_11_26(people, period, parameters):
        single = numpy.logical_not(people("in_a_relationship", period))

        return numpy.logical_not(people("schedule_4__part1_1_a", period)) * \
            numpy.logical_not(people("schedule_4__part1_1_b", period)) * \
            single * \
            people("jobseeker_support__transferred_15_july_2013",  periods.DateUnit.ETERNITY) * \
            (people("social_security__dependent_children", period) == 0)


class schedule_4__part1_1_d(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(d)"

    def formula_2018_11_26(people, period, parameters):
        single = numpy.logical_not(people("in_a_relationship", period))

        return numpy.logical_not(people("schedule_4__part1_1_a", period)) * \
            numpy.logical_not(people("schedule_4__part1_1_b", period)) * \
            numpy.logical_not(people("schedule_4__part1_1_c", period)) * \
            single * \
            (people("social_security__dependent_children", period) == 0)


class schedule_4__part1_1_e(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(e)"

    def formula_2018_11_26(people, period, parameters):
        single = numpy.logical_not(people("in_a_relationship", period))

        return numpy.logical_not(people("schedule_4__part1_1_a", period)) * \
            single * \
            (people("social_security__dependent_children", period) > 0) * \
            people("social_security__age_youngest_dependant_child", period.first_day) >= 14


class schedule_4__part1_1_f(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(f)"

    def formula_2018_11_26(people, period, parameters):
        single = numpy.logical_not(people("in_a_relationship", period))

        return numpy.logical_not(people("schedule_4__part1_1_a", period)) * \
            numpy.logical_not(people("schedule_4__part1_1_e", period)) * \
            single * \
            (people("social_security__dependent_children", period) > 0)


class schedule_4__part1_1_g(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(g)"

    def formula_2018_11_26(people, period, parameters):
        return people("in_a_relationship", period) * \
            people.family.any(people.family.members("social_security__granted_main_benefit", period), role = entities.Family.PARTNER)


class schedule_4__part1_1_g_i(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(g)(i)"

    def formula_2018_11_26(people, period, parameters):
        return people("schedule_4__part1_1_g", period) * \
            (people("social_security__dependent_children", period) < 1)


class schedule_4__part1_1_g_ii(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(g)(ii)"

    def formula_2018_11_26(people, period, parameters):
        return people("schedule_4__part1_1_g", period) * \
            (people("social_security__dependent_children", period) >= 1)


class schedule_4__part1_1_h(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(h)"

    def formula_2018_11_26(people, period, parameters):
        return people("in_a_relationship", period) * \
            people.family.any(people.family.members("super__being_paid_nz_superannuation", period.first_month), role = entities.Family.PARTNER)

    def formula_2020_11_09(people, period, parameters):
        return people("in_a_relationship", period) * \
            people.family.any(people.family.members("super__being_paid_nz_superannuation", period.first_month), role = entities.Family.PARTNER) + \
            people.family.any(people.family.members("veterans_support__being_paid_a_veterans_pension", period.first_month), role = entities.Family.PARTNER)


class schedule_4__part1_1_h_i(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(h)(i)"

    def formula_2018_11_26(people, period, parameters):
        return people("schedule_4__part1_1_h", period) * \
            (people("social_security__dependent_children", period) < 1)


class schedule_4__part1_1_h_ii(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(h)(ii)"

    def formula_2018_11_26(people, period, parameters):
        return people("schedule_4__part1_1_h", period) * \
            (people("social_security__dependent_children", period) >= 1)


class schedule_4__part1_1_i(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(i)"
    end = "2020-11-09"

    def formula_2018_11_26(people, period, parameters):
        return people("in_a_relationship", period) * \
            people.family.any(people.family.members("super__being_paid_nz_superannuation", period.first_month), role = entities.Family.PARTNER)


class schedule_4__part1_1_i_i(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(i)(i)"
    end = "2020-11-09"

    def formula_2018_11_26(people, period, parameters):
        return people("schedule_4__part1_1_i", period) * \
            (people("social_security__dependent_children", period) < 1)


class schedule_4__part1_1_i_ii(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(i)(ii)"
    end = "2020-11-09"

    def formula_2018_11_26(people, period, parameters):
        return people("schedule_4__part1_1_i", period) * \
            (people("social_security__dependent_children", period) >= 1)


class schedule_4__part1_1_j(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(j)"

    def formula_2018_11_26(people, period, parameters):
        return people("in_a_relationship", period) * \
            numpy.logical_not(people("schedule_4__part1_1_g", period)) * \
            numpy.logical_not(people("schedule_4__part1_1_h", period)) * \
            numpy.logical_not(people("schedule_4__part1_1_i", period))

    def formula_2020_11_09(people, period, parameters):
        return people("in_a_relationship", period) * \
            numpy.logical_not(people("schedule_4__part1_1_g", period)) * \
            numpy.logical_not(people("schedule_4__part1_1_h", period))


class schedule_4__part1_1_j_i(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(j)(i)"

    def formula_2018_11_26(people, period, parameters):
        return people("schedule_4__part1_1_j", period) * \
            (people("social_security__dependent_children", period) < 1)


class schedule_4__part1_1_j_ii(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    label = "Part 1 Jobseeker Support - Clause 1(j)(ii)"

    def formula_2018_11_26(people, period, parameters):
        return people("schedule_4__part1_1_j", period) * \
            (people("social_security__dependent_children", period) >= 1)
