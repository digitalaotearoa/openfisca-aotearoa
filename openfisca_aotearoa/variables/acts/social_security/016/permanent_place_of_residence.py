"""This module refers to Social Security Act's "Residential requirement"."""

import numpy

from openfisca_core import holders, populations
from openfisca_core.periods import DateUnit, Period
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class permanent_place_of_residence(Variable):
    label = "Permance place of residence in New Zealand"
    documentation = """
        (2) A person does not have a permanent place of residence in New
            Zealand if he or she has been and remains absent from New Zealand
            for more than 6 months or intends to be absent from New Zealand
            for more than 6 months. This subsection overrides subsection (3)
            but is subject to subsection (4).

        (3) A person has a permanent place of residence in New Zealand if he
            or she, although absent from New Zealand, has been personally
            present in New Zealand for a period or periods exceeding in the
            aggregate 183 days in the 12-month period immediately before last
            becoming absent from New Zealand. (A person personally present
            in New Zealand for part of a day is treated as being personally
            present in New Zealand for the whole of that day.)

        (4) A person must be treated as having New Zealand as the person’s
            permanent place of residence if—
            (a) the person—
                (i)   intends to resume a place of residence in New Zealand;
                      and
                (ii)  is absent from New Zealand primarily in connection with
                      the person’s employment duties (the remuneration for
                      which is treated as income derived in New Zealand for New
                      Zealand income tax purposes) or for up to 6 months
                      following the completion of the person’s period of
                      employment outside New Zealand; or
            (b) the person—
                (i)   intends to resume (or assume) a place of residence in
                      New Zealand; and
                (ii)  is the spouse or partner, child, or other dependant of
                      a person described in paragraph (a) and generally
                      accompanies that person; and
                (iii) is outside New Zealand during the period of employment
                      of the person described in paragraph (a) or for up to 6
                      months following the completion of it.
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.MONTH

    def formula_2001_09_19(persons, period, parameters):
        last_6m = Period((DateUnit.MONTH, period.start, 6)).offset(-6)
        absence_last_6m = persons("absent", last_6m, options = [populations.ADD])
        absent_last_6m = absence_last_6m >= 6
        absent_today = persons("absent", period)

        # This is a simplification assuming presence over the last 12 months,
        # but should be corrected to add "since the last absence".
        last_12m = Period((DateUnit.MONTH, period.start, 12)).offset(-12)
        presence_last_12m = persons("present", last_12m, options = [populations.ADD])
        present_last_12m = presence_last_12m >= 183

        return numpy.logical_not(
            + absent_last_6m
            * absent_today
            * numpy.logical_not(present_last_12m),
            )


class absent(Variable):
    label = "Absent from New Zealand"
    documentation = """
        (2) A person does not have a permanent place of residence in New
            Zealand if he or she has been and remains absent from New Zealand
            for more than 6 months or intends to be absent from New Zealand
            for more than 6 months. This subsection overrides subsection (3)
            but is subject to subsection (4).
    """
    entity = Person
    value_type = bool
    default_value = True
    definition_period = DateUnit.MONTH
    set_input = holders.set_input_dispatch_by_period


class present(Variable):
    label = "Present in New Zealand"
    documentation = """
        (3) A person has a permanent place of residence in New Zealand if he
            or she, although absent from New Zealand, has been personally
            present in New Zealand for a period or periods exceeding in the
            aggregate 183 days in the 12-month period immediately before last
            becoming absent from New Zealand. (A person personally present
            in New Zealand for part of a day is treated as being personally
            present in New Zealand for the whole of that day.)
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.DAY
    set_input = holders.set_input_dispatch_by_period


class resumes_place_of_residence(Variable):
    label = "Intends to resume a place of residence in New Zealand"
    documentation = """
        (4) A person must be treated as having New Zealand as the person’s
            permanent place of residence if—
            (a) the person—
                (i)   intends to resume a place of residence in New Zealand;
                      and
                (ii)  is absent from New Zealand primarily in connection with
                      the person’s employment duties (the remuneration for
                      which is treated as income derived in New Zealand for New
                      Zealand income tax purposes) or for up to 6 months
                      following the completion of the person’s period of
                      employment outside New Zealand;
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.ETERNITY


class absent_for_work_duties(Variable):
    label = "Intends to resume a place of residence in New Zealand"
    documentation = """
        (4) A person must be treated as having New Zealand as the person’s
            permanent place of residence if—
            (a) the person—
                (i)   intends to resume a place of residence in New Zealand;
                      and
                (ii)  is absent from New Zealand primarily in connection with
                      the person’s employment duties (the remuneration for
                      which is treated as income derived in New Zealand for New
                      Zealand income tax purposes) or for up to 6 months
                      following the completion of the person’s period of
                      employment outside New Zealand;
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.MONTH
