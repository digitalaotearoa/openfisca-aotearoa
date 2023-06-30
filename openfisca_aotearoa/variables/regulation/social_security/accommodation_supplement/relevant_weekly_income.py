"""Accommodation support's relevant weekly income.

The relevant weekly income is, if the applicant is not a community
spouse or partner, their combined weekly income; and it is, the weekly
income of the applicant.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class accommodation_supplement__relevant_weekly_income(variables.Variable):
    label = "Accommodation support's relevant weekly income"
    reference = "https://legislation.govt.nz/regulation/public/2018/0202/latest/LMS96265.html"
    documentation = """
        The relevant weekly income is, if the applicant is not a community
        spouse or partner, their combined weekly income; and it is, the weekly
        income of the applicant.
        """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK
