"""This module refers to Social Security Act's "Residential requirement"."""

import numpy

from openfisca_core import holders, populations
from openfisca_core.periods import DateUnit, Period
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class permanent_place_of_residence(Variable):
    label = "Permance place of residence in New Zealand"
    reference = "https://www.legislation.govt.nz/act/public/2001/0049/latest/DLM100661.html"
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
    set_input = holders.set_input_dispatch_by_period

    def formula_2001_09_19(persons, period, parameters):
        last_6m = Period((DateUnit.MONTH, period.start, 6)).offset(-6)
        absence_last_6m = persons("absent", last_6m, options = [populations.ADD])
        absent_last_6m = absence_last_6m >= 6
        absent_today = persons("absent", period)
        section_2 = numpy.logical_not(absent_last_6m * absent_today)

        # This is a simplification assuming presence over the last 12 months,
        # but should be corrected to add "since the last absence".
        last_12m = Period((DateUnit.MONTH, period.start, 12)).offset(-12)
        presence_last_12m = persons("present", last_12m, options = [populations.ADD])
        present_last_12m = presence_last_12m >= 183
        section_3 = absent_last_6m * absent_today * present_last_12m

        # Here we assume that the person being overseas for work duties at the
        # 5th month suffices to fulfil both being and having been overseas for
        # work duties.
        resumes_place_of_residence = persons("resumes_place_of_residence", DateUnit.ETERNITY)
        five_months_ago = Period((DateUnit.MONTH, period.start, 1)).offset(-5)
        on_work_duties = persons("absent_for_work_duties", five_months_ago)
        section_4 = (
            + absent_last_6m
            * absent_today
            * resumes_place_of_residence
            * on_work_duties
            )

        unlawful_last_12m = persons("present_unlawfully", last_12m, options = [populations.ADD])
        lawful_last_12m = (presence_last_12m - unlawful_last_12m) >= 183
        section_5 = lawful_last_12m

        return section_2 + section_3 * section_5 + section_4


class absent(Variable):
    label = "Absent from New Zealand"
    reference = "https://www.legislation.govt.nz/act/public/2001/0049/latest/DLM100661.html"
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
    reference = "https://www.legislation.govt.nz/act/public/2001/0049/latest/DLM100661.html"
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
    reference = "https://www.legislation.govt.nz/act/public/2001/0049/latest/DLM100661.html"
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
    reference = "https://www.legislation.govt.nz/act/public/2001/0049/latest/DLM100661.html"
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


class present_unlawfully(Variable):
    label = "Present unlawfully in New Zealand"
    reference = "https://www.legislation.govt.nz/act/public/2001/0049/latest/DLM100661.html"
    documentation = """
        (5) A person is not ordinarily resident in New Zealand if he or she is
            in New Zealand unlawfully within the meaning of the Immigration Act
            2009. Any period during which a person is in New Zealand unlawfully
            is not counted as time spent in New Zealand for the purposes of
            subsection (3).
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.DAY
