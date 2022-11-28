"""TODO: Add missing doctring."""

import datetime

import numpy

from openfisca_core import holders, periods, variables

# Import the entities specifically defined for this tax and benefit system
from openfisca_aotearoa import entities


# This variable is a pure input: it doesn't have a formula
class date_of_birth(variables.Variable):
    # base_function = missing_value # missing_value removed from model_api
    value_type = datetime.date
    entity = entities.Person
    label = "Birth date"
    definition_period = periods.DateUnit.ETERNITY  # This variable cannot change over time.
    reference = "https://en.wiktionary.org/wiki/birthdate"


# This variable is a pure input: it doesn't have a formula
class due_date_of_birth(variables.Variable):
    value_type = datetime.date
    entity = entities.Person
    label = "Birth due date"
    definition_period = periods.DateUnit.ETERNITY  # This variable cannot change over time.
    reference = ""


class age(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.DateUnit.DAY
    label = "The age of a Person (in years)"
    unit = "years"
    default_value = -9999
    set_input = holders.set_input_dispatch_by_period
    # A person's age is computed according to their birth date.

    def formula(persons, period, parameters):
        birth = persons("date_of_birth", period)
        birth_year = birth.astype("datetime64[Y]").astype(int) + 1970
        birth_month = birth.astype("datetime64[M]").astype(int) % 12 + 1
        birth_day = (birth - birth.astype("datetime64[M]") + 1).astype(int)

        is_birthday_past = (birth_month < period.start.month) + (birth_month == period.start.month) * (birth_day <= period.start.day)
        # If the birthday is not passed
        # this year, substract one year
        return (period.start.year - birth_year) - numpy.where(is_birthday_past, 0, 1)



class age_of_youngest(variables.Variable):
    value_type = int
    entity = entities.Family
    definition_period = periods.DateUnit.DAY
    unit = "years"
    label = "The age of the youngest member of a family"
    # A person's age is computed according to their birth date.

    def formula(families, period, parameters):
        return families.min(families.members("age", period))


class age_of_partner(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.DateUnit.DAY
    unit = "years"
    label = "The maximum age of partner in a family"

    def formula(persons, period, parameters):
        return persons.family.max(persons.family.members("age", period), role = entities.Family.PARTNER)
