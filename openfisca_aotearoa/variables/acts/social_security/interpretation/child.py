"""TODO: Add missing doctring."""

import numpy

from openfisca_core import holders
from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class social_security__child(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is a child as defined in Schedule 2, Dictionary"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS6902"

    def formula(persons, period, parameters):
        under_16 = persons("age", period.start) < 16
        under_18 = persons("age", period.start) < 18

        financially_independent = persons("social_security__financially_independent", period)

        return under_16 + (under_18 * numpy.logical_not(financially_independent))


class social_security__dependent_child(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is a dependent children as defined in Schedule 2, Dictionary in relation to a person in a family"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS7234", "https://www.workandincome.govt.nz/map/income-support/main-benefits/sole-parent-support/dependent-child-01.html"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period

    def formula(persons, period, parameters):
        def_a_i = persons("social_security__child", period)
        def_a_i_ABC = persons.has_role(entities.Family.CHILD) * numpy.logical_not(persons("social_security__financially_independent", period))
        # def_a_ii children placed in the custody under the age of 14 persons("oranga_tamariki__child", period)
        # def_a_iii - is not a child in respect of whom a young parent payment is being paid in relation to a person who is not the child’s parent or step-parent;
        # def_a_iv - is not a child in respect of whom an orphan’s benefit or an unsupported child’s benefit is being paid (but the exclusion in this paragraph applies only for the purposes of Parts 1, 2, 3, 6, 7, 11, and 12 of Schedule 4)
        return def_a_i * def_a_i_ABC


class social_security__dependent_children(variables.Variable):
    value_type = int
    entity = entities.Person
    label = "number a dependent child (or children)"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS7234"
    set_input = holders.set_input_dispatch_by_period

    def formula(persons, period, parameters):
        # children don't have dependant children, the principal might by definition be a child with dependeant children, they won't in that scenario have a role of child
        return sum(persons.has_role(entities.Family.CHILD) * persons.family.members("social_security__dependent_child", period)) * numpy.logical_not(persons.has_role(entities.Family.CHILD))


class social_security__age_youngest_dependant_child(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.DAY
    label = "As defined in Part 1 of Schedule 4 of the Social Security Act, Part 1, 1(c)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    set_input = holders.set_input_dispatch_by_period

    def formula(persons, period, parameters):
        youngest_age = numpy.min(persons.family.members("age", period.start))
        return persons.family.members("social_security__dependent_child", period.first_week) * youngest_age
