"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables
from openfisca_core import holders

from openfisca_aotearoa import entities


class social_security__dependent_children(variables.Variable):
    value_type = float
    entity = entities.Person
    label = "has a dependent child (or children)"
    definition_period = periods.MONTH
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS7234"
    set_input = holders.set_input_dispatch_by_period

    def formula(persons, period, parameters):
        return sum(persons.family.members("social_security__dependent_child", period.first_month))


class social_security__child(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is a child as defined in Schedule 2, Dictionary"
    definition_period = periods.MONTH
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS6902"

    def formula(persons, period, parameters):
        under_16 = persons("age", period.start) < 16
        under_18 = persons("age", period.start) < 18

        financially_independent = persons(
            "social_security__financially_independent", period)

        return under_16 + (under_18 * numpy.logical_not(financially_independent))


class social_security__age_youngest_dependant_child(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.DAY
    label = "As defined in Part 1 of Schedule 4 of the Social Security Act, Part 1, 1(c)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    set_input = holders.set_input_dispatch_by_period

    def formula(persons, period, parameters):
        youngest_age = numpy.min(persons.family.members("age", period.start))
        return persons.family.members("social_security__dependent_child", period.first_month) * youngest_age


class social_security__dependent_child(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is a dependent child as defined in Schedule 2, Dictionary"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS7234"
    definition_period = periods.MONTH


# TODO: Review against the new 2018 act, not referenced anywhere
class social_security__child_in_family(variables.Variable):
    value_type = bool
    entity = entities.Family
    definition_period = periods.MONTH
    label = "Family has a child"

    def formula(families, period, parameters):
        children = families.members("social_security__child", period)
        return families.any(children, role=entities.Family.CHILD)
