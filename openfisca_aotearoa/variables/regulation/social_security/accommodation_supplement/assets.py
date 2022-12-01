"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class accommodation_supplement__assets_requirement(variables.Variable):
    label = "Assets requirement"
    reference = "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/LMS96256.html"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, params):
        principal = people.has_role(entities.Family.PRINCIPAL)
        mingled = principal * people("social_security__in_a_relationship", period)
        singles = principal * numpy.logical_not(mingled)
        cash_assets = people("accommodation_supplement__cash_assets", period)
        children = people("social_security__dependent_children", period) >= 1
        no_child = numpy.logical_not(children)

        cash_assets_principal = people.family.sum(
            cash_assets,
            role = entities.Family.PRINCIPAL,
            )

        cash_assets_partners = people.family.sum(
            cash_assets,
            role = entities.Family.PARTNER,
            )

        total_cash_assets = (
            + cash_assets_principal
            + cash_assets_partners
            )

        threshold = (
            params(period)
            .social_security
            .accommodation_supplement
            .assets
            )

        ssr2018_15_1_a_i = (
            + mingled
            * (total_cash_assets <= threshold.ssa2018_15_1_a)
            )

        ssr2018_15_1_a_ii = (
            + singles
            * children
            * (total_cash_assets <= threshold.ssa2018_15_1_a)
            )

        ssr2018_15_1_b = (
            + singles
            * no_child
            * (total_cash_assets <= threshold.ssa2018_15_1_b)
            )

        return ssr2018_15_1_a_i + ssr2018_15_1_a_ii + ssr2018_15_1_b


class accommodation_supplement__cash_assets(variables.Variable):
    label = "Cash assets"
    reference = "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/LMS96256.html"
    documentation = """TODO"""
    entity = entities.Person
    value_type = int
    default_value = 0
    definition_period = periods.DateUnit.WEEK
