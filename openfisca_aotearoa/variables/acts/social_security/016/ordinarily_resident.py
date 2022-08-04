"""This module refers to Social Security Act's "Residential requirement"."""

from openfisca_core import holders, populations
from openfisca_core.periods import DateUnit, Period
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class ordinarily_resident(Variable):
    label = "Ordinarily resident in New Zealand"
    reference = "https://www.legislation.govt.nz/act/public/2001/0049/latest/DLM100661.html"
    documentation = """
        17 Ordinarily resident in New Zealand

        (1) A person is ordinarily resident in New Zealand if he or she—
            (a) has New Zealand as his or her permanent place of residence,
                whether or not he or she also has a place of residence outside
                New Zealand; and
            (b) is in one of the following categories:
                (i)   a New Zealand citizen:
                (ii)  a holder of a residence class visa granted under the
                      Immigration Act 2009:
                (iii) a person who is a spouse or a partner, child, or other
                      dependant of any person referred to in subparagraph (i)
                      or (ii), and who generally accompanies the person
                      referred to in the subparagraph.

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
    set_input = holders.set_input_dispatch_by_period

    def formula_2001_09_19(persons, period, parameters):
        this_month = period.first_month
        place_of_residence = persons("permanent_place_of_residence", this_month)
        citizen = persons("citizen", period)
        residence_visa = persons("residence_visa", period)

        return place_of_residence * (citizen + residence_visa)
