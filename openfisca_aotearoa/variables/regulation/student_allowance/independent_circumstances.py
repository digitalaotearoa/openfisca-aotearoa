"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class independent_circumstances_grant__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM260312"
    label = "Eligible for Student Allowance Independent Circumstances Grant"
    """
    8 Eligibility for independent circumstances grant
    (1) A single student without a supported child or children is eligible for an independent circumstances grant, if—
        (a) either—
            (i) the student is of or over 16 and younger than 24, and is undertaking a course at a tertiary provider; or
            (ii) is of or over 18 and younger than 24, and is undertaking a course at a secondary school; and
                (b) the student is neither living in a parental home nor receiving financial assistance from any parent of that student; and
                (c) the chief executive considers that it would, by reason of exceptional circumstances, be unreasonable
                    for the student to live with a parent and receive financial assistance from any parent of that student.
        (2) [Revoked]
        (3) Despite subclause (1), no student is eligible for an independent circumstances grant if the student receives
            a basic grant. (4) This regulation is subject to regulations 12 to 16, 20, 28 to 31, 34, 35, 40, and 44 to 48.
    """
    # Forumla todo


class independent_circumstances_grant__receiving(variables.Variable):
    label = "Already receiving independent circumstances grant"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK


class independent_circumstances_grant__would_be_entitled(variables.Variable):
    label = "Would be eligible for independent circumstances if less income"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK
