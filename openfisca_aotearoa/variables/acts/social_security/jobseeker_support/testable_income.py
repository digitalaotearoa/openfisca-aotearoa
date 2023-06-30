"""Jobseeker support's testable income.

The testable income upon which the applicable rate of jobseeker support is
calculated and eventually reduced.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class jobseeker_support__testable_income(variables.Variable):
    label = "Jobseeker support's testable income"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784375"
    documentation = """
        Jobseeker support must be reduced of the total income of the
        beneficiary and the beneficiary’s spouse or partner.
    """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _parameters):
        family = people.family

        beneficiary_income = family.sum(
            family.members("social_security__income", period),
            role = entities.Family.PRINCIPAL,
            )

        spouse_or_partner_income = family.sum(
            family.members("social_security__income", period),
            role = entities.Family.PARTNER,
            )

        return beneficiary_income + spouse_or_partner_income
