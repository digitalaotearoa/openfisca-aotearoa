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

    def formula_2018_11_26(people, period, _params):
        cash_assets = people("accommodation_supplement__cash_assets", period)
        dependent_children = people("social_security__dependent_child", period)

        cash_assets_principal = people.family.sum(
            cash_assets,
            role = entities.Family.PRINCIPAL,
            )

        cash_assets_partners = people.family.sum(
            cash_assets,
            role = entities.Family.PARTNER,
            )

        total_cash_assets = cash_assets_principal + cash_assets_partners

        # TODO: move to parameter
        ssr2018_15_1_a_i = (
            + people.has_role(entities.Family.PRINCIPAL)
            * (people.family.nb_persons(entities.Family.PARTNER) >= 1)
            * (total_cash_assets <= 16200)
            )

        # TODO: move to parameter
        ssr2018_15_1_a_ii = (
            + people.has_role(entities.Family.PRINCIPAL)
            * (people.family.nb_persons(entities.Family.PARTNER) == 0)
            * (sum(dependent_children) >= 1)
            * (total_cash_assets <= 16200)
            )

        # TODO: move to parameter
        ssr2018_15_1_b = (
            + numpy.logical_not(people.has_role(entities.Family.PARTNER))
            * numpy.logical_not(people.has_role(entities.Family.CHILD))
            * numpy.logical_not(people.has_role(entities.Family.OTHER))
            * (people.family.nb_persons(entities.Family.PARTNER) == 0)
            * (sum(dependent_children) == 0)
            * (total_cash_assets <= 8100)
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
