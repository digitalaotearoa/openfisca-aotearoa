"""TODO: Add missing doctring."""


from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class youth_payment__granted(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person is currently granted the youth payment benefit"
    definition_period = periods.WEEK
    reference = "Reference is unclear, but variable is utilised by the phrase: 'granted a main benefit'"


class youth_payment__receiving(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person is currently recieving/being paid the youth payment benefit"
    definition_period = periods.WEEK
    reference = "Reference is unclear, but concept underpinning the variable assumes it covers both: 'being paid a main benefit' or 'recieving a benefit'"


class youth_payment__single_young_person_exceptional_circumstances(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "a young person in exceptional circumstances"
    reference = """
    (2) For the purposes of subsection (1), a young person is in exceptional circumstances if—
        (a) each of his or her parents (and guardians (if any)) is unable to support
            him or her financially; or
        (b) his or her relationship with his or her parents (and guardians (if any)) has broken down,
            and none of them is prepared to support him or her financially; or
        (c) he or she has ceased to be subject to—
            (i) an agreement under section 140 of the Oranga Tamariki Act 1989; or
            (ii) an order under section 78, 101, or 283(n) of that Act; or
            (iii) a sole guardianship order under section 110 of that Act; or
        (d) the chief executive is satisfied that (for some other good and sufficient reason) the young person
            cannot reasonably be expected to be financially dependent on his or her parents or any other person.

    (3) However, a young person is not in exceptional circumstances if—
        (a) he or she has the option of living with a parent or guardian but chooses not to; and
        (b) the chief executive is not satisfied that there are good and sufficient reasons for the young person not to live with that parent or guardian.
    http://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM4686073
    """
