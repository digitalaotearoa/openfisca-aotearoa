"""Jobseeker Support — Income.

The income upon which the applicable rate of Jobseeker Support is calculated
and eventually reduced.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class jobseeker_support__income(variables.Variable):
    label = "Jobseeker support — Income"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784850.html"
    documentation = """Total income of people and their partners."""
    entity = entities.Family
    value_type = float
    default_value = 0
    definition_period = periods.WEEK

    def formula_2018_11_26(families, period, _params):
        people = families.members

        beneficiary_income = families.sum(
            people("social_security__income", period),
            role = entities.Family.PRINCIPAL,
            )

        spouse_or_partner_income = families.sum(
            people("social_security__income", period),
            role = entities.Family.PARTNER,
            )

        return beneficiary_income + spouse_or_partner_income
