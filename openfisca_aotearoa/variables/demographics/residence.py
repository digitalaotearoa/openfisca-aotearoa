"""This module provides eligibility and amount for Jobseeker Support."""

from datetime import timedelta

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from datetime import timedelta

from openfisca_core import periods, variables
from openfisca_core.holders import set_input_dispatch_by_period

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities


class number_of_years_lived_in_nz(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Number of years lived in NZ"


class total_number_of_years_lived_in_nz_since_age_20(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Total number of years lived in NZ since age 20"


class total_number_of_years_lived_in_nz_since_age_50(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Total number of years lived in NZ since age 50"


class days_present_in_new_zealand_in_preceeding_5_years(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.DAY
    default_value = 0

    def formula(persons, period, parameters):

        sum_ = 0

        for offset in range((days_since_n_years_ago(period.date, 5) * -1), 1):
            p = period.offset(offset)
            sum_ += (persons("was_present_in_nz_and_entitled_to_indefinite_stay", p) * 1)

        return sum_


def days_since_n_years_ago(day, n=1):
    """
    Note does not include the day itself.

    e.g. days since 1 years ago for
    1-June-2013 would count from 2-June-2012,
    to 1-June-2013, thus 365 days
    """
    try:
        date_n_years_ago = day.replace(year=day.year - n)
        # The days in that rolling year could  be 365 or 366
        return (day - date_n_years_ago).days
    except ValueError:
        # Usually means a leap day, so try from the next day (1 March)
        date_n_years_ago = (day + timedelta(days=1)).replace(year=day.year - n)
        return (day - date_n_years_ago).days


class days_present_in_new_zealand_in_preceeding_year(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.DAY
    label = "was present in New Zealand this many days in the last (rolling) year"
    reference = "Accumlative from `was_present_in_nz_and_entitled_to_indefinite_stay` variable`"
    default_value = 0

    def formula(persons, period, parameters):

        sum_ = 0

        start_date = days_since_n_years_ago(period.date)
        for p in [period.offset(offset) for offset in range((start_date * -1), 0)]:
            sum_ += (persons("was_present_in_nz_and_entitled_to_indefinite_stay", p) * 1)

        return sum_


class was_present_in_nz_and_entitled_to_indefinite_stay(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.DAY
    label = "was present in New Zealand and entitled to indefinite stay"
    reference = "Whether both `present_in_new_zealand` and `immigration__entitled_to_indefinite_stay` were true"

    def formula(persons, period, parameters):
        present = persons("present_in_new_zealand", period)
        entitled = persons("immigration__entitled_to_indefinite_stay", period)
        return present * entitled


class present_in_new_zealand(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DAY
    default_value = False
    label = "was present in New Zealand on this day"
    reference = "http://www.legislation.govt.nz/act/public/1977/0061/latest/DLM443855.html"
    set_input = set_input_dispatch_by_period


class years_resided_continuously_in_new_zealand(variables.Variable):
    value_type = int
    entity = entities.Person
    label = "number of years resided continuously in New Zealand"
    definition_period = periods.MONTH
