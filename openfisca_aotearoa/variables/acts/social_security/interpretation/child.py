"""TODO: Add missing doctring."""

import numpy

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable
from openfisca_core import holders

from openfisca_aotearoa.entities import Family, Person


class social_security__person_has_dependant_child(Variable):
    value_type = bool
    entity = Person
    label = "has a dependent child (or children)"
    definition_period = MONTH
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS7234"
    set_input = holders.set_input_dispatch_by_period


class social_security__child(Variable):
    value_type = bool
    entity = Person
    label = "Is a child as defined in Schedule 2, Dictionary"
    definition_period = MONTH
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS6902"

    def formula(persons, period, parameters):
        under_16 = persons("age", period.start) < 16
        under_18 = persons("age", period.start) < 18

        financially_independent = persons(
            "social_security__financially_independent", period)

        return under_16 + (under_18 * numpy.logical_not(financially_independent))


class social_security__dependent_child(Variable):
    value_type = bool
    entity = Person
    label = "Is a dependent child as defined in Schedule 2, Dictionary"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS7234"
    definition_period = MONTH

    def formula(persons, period, parameters):
        return persons("social_security__child", period) * persons("dependent_child", period)


# TODO: Review against the new 2018 act, not referenced anywhere
class social_security__child_in_family(Variable):
    value_type = bool
    entity = Family
    definition_period = MONTH
    label = "Family has a child"

    def formula(families, period, parameters):
        children = families.members("social_security__child", period)
        return families.any(children, role=Family.CHILD)
