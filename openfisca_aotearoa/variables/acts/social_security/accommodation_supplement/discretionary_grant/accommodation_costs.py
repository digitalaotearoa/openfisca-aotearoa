"""Accommodation supplement's accommodation costs.

Accommodation costs are the amount payable by a person for rent, mortgage,
board, lodging, ownership, and tenancy.

"""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.demographics import housing


class accommodation_supplement__accommodation_costs(variables.Variable):
    label = "Accommodation costs"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """
        Accommodation costs are the amount payable by a person for rent,
        mortgage, board, lodging, ownership, and tenancy.
        """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _params):
        # (2) In this subpart, unless the context otherwise requires,—
        #     accommodation costs, in relation to any person for any given
        #     period, means,—

        #     (a) in relation to premises rented by the person, the amount
        #         payable by the person for rent of the premises, excluding any
        #         service costs included in that rent and any arrears:
        ssa2018_part_2_sub_10_65_2_a = people(
            "ssa2018_part_2_sub_10_65_2_a",
            period,
            )

        #     (b) in relation to premises that are owned by the person, the
        #         total amount of all payments (including essential repairs and
        #         maintenance, local authority rates, and house insurance
        #         premiums, but excluding any service costs and any arrears)
        #         that,—
        #        (i)  subject to clause 18 of Schedule 3, are required to be
        #             made under any mortgage security for money advanced under
        #             that security to acquire the premises, or to repay
        #             advances similarly secured; or
        #        (ii) MSD is satisfied are reasonably required to be made:
        ssa2018_part_2_sub_10_65_2_b = people(
            "ssa2018_part_2_sub_10_65_2_b",
            period,
            )

        #     (c) in relation to a person who is a boarder or lodger in any
        #         premises, 62% of the amount paid for board or lodging
        #         (excluding any arrears):
        ssa2018_part_2_sub_10_65_2_c = people(
            "ssa2018_part_2_sub_10_65_2_c",
            period,
            )

        #     (d) if a person is a joint tenant of, or an owner in common of,
        #         any premises with another person or other persons living in
        #         the premises, that applicant’s accommodation costs are the
        #         share of the total accommodation costs of the jointly
        #         tenanted, or commonly owned, premises that MSD is satisfied
        #         the person is paying
        ssa2018_part_2_sub_10_65_2_d = people(
            "ssa2018_part_2_sub_10_65_2_d",
            period,
            )

        return (
            + ssa2018_part_2_sub_10_65_2_a
            + ssa2018_part_2_sub_10_65_2_b
            + ssa2018_part_2_sub_10_65_2_c
            + ssa2018_part_2_sub_10_65_2_d
            )

class ssa2018_part_2_sub_10_65_2_a(variables.Variable):
    label = "Accommodation costs (a)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """
        In relation to premises rented by the person, accommodation costs are
        the amount payable by the person for rent of the premises, excluding
        any service costs included in that rent and any arrears.
        """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, params):
        # (2) In this subpart, unless the context otherwise requires,—
        #     accommodation costs, in relation to any person for any given
        #     period, means,—
        #     (a) in relation to premises rented by the person, the amount
        #         payable by the person for rent of the premises, excluding any
        #         service costs included in that rent and any arrears:

        # Whether each person is part of a tenancy.
        tenancy = (
            + people.has_role(entities.Tenancy.TENANT)
            + people.has_role(entities.Tenancy.OTHER)
            )

        # Accommodation type for the requested period.
        accommodation_type = people("accommodation_type", period)

        # Accommodation costs for the requested period.
        accommodation_costs = people("accommodation_costs", period)

        # Accommodation costs ratio to be considered as accommodation costs.
        costs_ratio = (
            params(period)
            .social_security
            .accommodation_supplement
            .accommodation_costs
            )

        return (
            + numpy.logical_not(tenancy)
            * (accommodation_costs > 0)
            * (accommodation_type == housing.AccommodationType.rent)
            * costs_ratio.rent
            )

class ssa2018_part_2_sub_10_65_2_b(variables.Variable):
    label = "Accommodation costs (b)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """
        In relation to premises owned by the person, accommodation costs are
        the total amount of all payments that are required to be made under any
        mortgage and MSD is satisfied are reasonably required to be made.
        """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, params):
        # (2) In this subpart, unless the context otherwise requires,—
        #     accommodation costs, in relation to any person for any given
        #     period, means,—
        #     (b) in relation to premises that are owned by the person, the
        #         total amount of all payments (including essential repairs and
        #         maintenance, local authority rates, and house insurance
        #         premiums, but excluding any service costs and any arrears)
        #         that,—
        #        (i)  subject to clause 18 of Schedule 3, are required to be
        #             made under any mortgage security for money advanced under
        #             that security to acquire the premises, or to repay
        #             advances similarly secured; or
        #        (ii) MSD is satisfied are reasonably required to be made:

        # Whether each person is part of a tenancy.
        ownership = (
            + people.has_role(entities.Ownership.OWNER)
            + people.has_role(entities.Ownership.OTHER)
            )

        # Accommodation type for the requested period.
        accommodation_type = people("accommodation_type", period)

        # Accommodation costs for the requested period.
        accommodation_costs = people("accommodation_costs", period)

        # Accommodation costs ratio to be considered as accommodation costs.
        costs_ratio = (
            params(period)
            .social_security
            .accommodation_supplement
            .accommodation_costs
            )

        return (
            + numpy.logical_not(ownership)
            * (accommodation_costs > 0)
            * (accommodation_type == housing.AccommodationType.mortgage)
            * costs_ratio.mortgage
            )

class ssa2018_part_2_sub_10_65_2_c(variables.Variable):
    label = "Accommodation costs (c)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """
        In relation to a person who is a boarder or lodger in any premises,
        accommodation costs are 62% of the amount paid for board or lodging
        (excluding any arrears):
        """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, params):
        # (2) In this subpart, unless the context otherwise requires,—
        #     accommodation costs, in relation to any person for any given
        #     period, means,—
        #     (c) in relation to a person who is a boarder or lodger in any
        #         premises, 62% of the amount paid for board or lodging
        #         (excluding any arrears):

        # Accommodation type for the requested period.
        accommodation_type = people("accommodation_type", period)

        # Accommodation costs for the requested period.
        accommodation_costs = people("accommodation_costs", period)

        # Accommodation costs ratio to be considered as accommodation costs.
        costs_ratio = (
            params(period)
            .social_security
            .accommodation_supplement
            .accommodation_costs
            )

        boarding_costs = (
            + (accommodation_costs > 0)
            * (accommodation_type == housing.AccommodationType.board)
            * costs_ratio.board
            )

        lodging_costs = (
            + (accommodation_costs > 0)
            * (accommodation_type == housing.AccommodationType.lodging)
            * costs_ratio.lodging
            )

        return boarding_costs + lodging_costs

class ssa2018_part_2_sub_10_65_2_d(variables.Variable):
    label = "Accommodation costs (d)"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """
        In relation to a joint tenant of, or an owner in common of, any
        premises with another person or other persons living in the premises,
        accommodation costs are the share of the total accommodation costs of
        the jointly tenanted, or commonly owned, premises.
        """
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, params):
        # (2) In this subpart, unless the context otherwise requires,—
        #     accommodation costs, in relation to any person for any given
        #     period, means,—
        #     (d) if a person is a joint tenant of, or an owner in common of,
        #         any premises with another person or other persons living in
        #         the premises, that applicant’s accommodation costs are the
        #         share of the total accommodation costs of the jointly
        #         tenanted, or commonly owned, premises that MSD is satisfied
        #         the person is paying

        # Whether each person is a tenancy's applicant.
        tenant = people.has_role(entities.Tenancy.PRINCIPAL)

        # Whether each person is an ownership's applicant.
        owner = people.has_role(entities.Ownership.PRINCIPAL)

        # Accommodation type for the requested period.
        accommodation_type = people("accommodation_type", period)

        # Accommodation costs for the requested period.
        accommodation_costs = people("accommodation_costs", period)

        # Total accommodation costs of principal tenants.
        accommodation_costs_principal_tenant = people.tenancy.sum(
            accommodation_costs,
            role = entities.Tenancy.PRINCIPAL,
            )

        # Total accommodation costs of other tenants.
        accommodation_costs_other_tenants = people.tenancy.sum(
            accommodation_costs,
            role = entities.Tenancy.TENANT,
            )

        # Total accommodation costs of each tenancy.
        accommodation_costs_tenancy = (
            + accommodation_costs_principal_tenant
            + accommodation_costs_other_tenants
            )

        # Total accommodation costs of principal owners.
        accommodation_costs_principal_owner = people.ownership.sum(
            accommodation_costs,
            role = entities.Ownership.PRINCIPAL,
            )

        # Total accommodation costs of other owners.
        accommodation_costs_other_owners = people.ownership.sum(
            accommodation_costs,
            role = entities.Ownership.OWNER,
            )

        # Total accommodation costs of each ownership.
        accommodation_costs_ownership = (
            + accommodation_costs_principal_owner
            + accommodation_costs_other_owners
            )

        # Accommodation costs ratio to be considered as accommodation costs.
        costs_ratio = (
            params(period)
            .social_security
            .accommodation_supplement
            .accommodation_costs
            )

        tenancy_costs = (
            + tenant
            * (accommodation_costs_tenancy > 0)
            * (accommodation_type == housing.AccommodationType.rent)
            * costs_ratio.rent
            )

        ownership_costs = (
            + owner
            * (accommodation_costs_ownership > 0)
            * (accommodation_type == housing.AccommodationType.mortgage)
            * costs_ratio.mortgage
            )

        return tenancy_costs + ownership_costs
