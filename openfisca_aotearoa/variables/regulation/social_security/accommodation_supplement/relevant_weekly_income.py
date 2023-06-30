"""Accommodation support's relevant weekly income.

The relevant weekly income is, if the applicant is not a community
spouse or partner, their combined weekly income; and it is, the weekly
income of the applicant.

"""
import numpy
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

    def formula_2018_11_26(people, period, _parameters):
        principal = people.has_role(entities.Family.PRINCIPAL)
        partner = people.has_role(entities.Family.PARTNER)
        family = people.family

        csp = family.sum(
            family.members(
                "social_security__community_spouse_or_partner",
                period
                )
            )

        beneficiary_income = family.sum(
            family.members("social_security__income", period),
            role = entities.Family.PRINCIPAL,
            )

        spouse_or_partner_income = family.sum(
            family.members("social_security__income", period),
            role = entities.Family.PARTNER,
            )

        return (
            + numpy.logical_not(csp)
            * (beneficiary_income + spouse_or_partner_income)
            + csp
            * principal
            * beneficiary_income
            + partner
            * csp
            * spouse_or_partner_income
        )
