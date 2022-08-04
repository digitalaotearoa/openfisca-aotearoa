"""This module refers to Social Security Act's "Residential requirement"."""

import numpy

from openfisca_core import holders, periods, populations
from openfisca_core.periods import DateUnit
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class continuously_resided_at_any_one_time(Variable):
    label = "Continuously resided in New Zealand at any one time"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783138.html"
    documentation = """
        (i)  has resided continuously in New Zealand for a period of at
             least 2 years at any one time after becoming a citizen or
             resident;
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.DAY
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        # We could calculate as far a we want, but for the current use case,
        # a couple of years is enough (we just want to be able to determine
        # physical presence in New Zealand during a period a Person obtains
        # citizenship or a residence class visa).

        # We move back 24 years in the past.
        last_24y = (
            periods
            .period(f"year:{period.start}:24")
            .offset(-24)
            .get_subperiods(DateUnit.YEAR)
            )

        # We calculate, for each year, if the person was more than 730 days
        # continuously in New Zealand.
        present = numpy.asarray([
            persons(
                "present",
                periods.period(f"year:{year.start}:2"),
                options = populations.ADD,
                ) >= periods.period(f"year:{year.start}:2").size_in_days
            for year in last_24y
            ])

        # We calculate, for each year, if the person was more than 730 days
        # citizen of New Zealand.
        citizen = numpy.asarray([
            persons(
                "citizen",
                periods.period(f"year:{year.start}:2"),
                options = populations.ADD,
                ) >= periods.period(f"year:{year.start}:2").size_in_days
            for year in last_24y
            ])

        # We calculate, for each year, if the person hold for more than 730
        # days a residence class visa.
        resident = numpy.asarray([
            persons(
                "residence_visa",
                periods.period(f"year:{year.start}:2"),
                options = populations.ADD,
                ) >= periods.period(f"year:{year.start}:2").size_in_days
            for year in last_24y
            ])

        # If presence and either citizen or resident numbers match, we can
        # conclude the person has resided continuously at least 2 years at any
        # one time since becoming a citizen and/or resident.
        #
        # Note: ``sum`` returns a vector here.
        return sum(present * (citizen + resident))


class continuously_resided_before_application(Variable):
    label = "Continuously resided in New Zealand before application"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783138.html"
    documentation = """
        (b) P is ordinarily resident in a country with which New Zealand
            has a reciprocity agreement, and P has resided continuously in
            New Zealand for a period of at least 2 years before applying
            for the benefit or before a decision on P’s claim for the
            benefit is made.
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.DAY
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        last_2y = (
            periods
            .period(f"year:{period.start}:2")
            .offset(-2)
            )

        # We calculate if the person has been more than 2 years continuously
        # in New Zealand.
        present = persons(
            "present",
            last_2y,
            options = populations.ADD,
            ) >= last_2y.size_in_days

        # We calculate if the person has been more than 2 years an overseas
        # reciprocal resident living in New Zealand.
        reciprocal = persons(
            "reciprocity_resident",
            last_2y,
            options = populations.ADD,
            ) >= last_2y.size_in_days

        # If presence and reciprocal residency numbers match, we can
        # conclude the person has resided continuously at least 2 years before
        # applying for the benefit.
        return present * reciprocal
