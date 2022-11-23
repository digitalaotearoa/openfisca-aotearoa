"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.demographics import housing


class accommodation_supplement__accommodation_costs(variables.Variable):
    label = "Accommodation costs"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783241"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, _parameters):
        accommodation_type = people("accommodation_type", period)
        accommodation_costs = people("accommodation_costs", period)

        accommodation_costs_principal_tenant = people.tenancy.sum(
            accommodation_costs,
            role = entities.Tenancy.PRINCIPAL,
            )

        accommodation_costs_other_tenants = people.tenancy.sum(
            accommodation_costs,
            role = entities.Tenancy.TENANT,
            )

        accommodation_costs_tenancy = (
            + accommodation_costs_principal_tenant
            + accommodation_costs_other_tenants
            )

        accommodation_costs_principal_owner = people.ownership.sum(
            accommodation_costs,
            role = entities.Ownership.PRINCIPAL,
            )

        accommodation_costs_other_owners = people.ownership.sum(
            accommodation_costs,
            role = entities.Ownership.OWNER,
            )

        accommodation_costs_ownership = (
            + accommodation_costs_principal_owner
            + accommodation_costs_other_owners
            )

        ssa2018_65_2_a = (
            + (accommodation_costs > 0)
            * (accommodation_type == housing.AccommodationType.rent)
            )

        ssa2018_65_2_b = (
            + (accommodation_costs > 0)
            * (accommodation_type == housing.AccommodationType.mortgage)
            )

        ssa2018_65_2_c = (
            + (accommodation_costs > 0)
            * (
                + (accommodation_type == housing.AccommodationType.board)
                + (accommodation_type == housing.AccommodationType.lodging)
                )
            )

        ssa2018_65_2_d = (
            + (
                + (accommodation_costs_tenancy > 0)
                * (accommodation_type == housing.AccommodationType.rent)
                )
            + (
                + (accommodation_costs_ownership > 0)
                * (accommodation_type == housing.AccommodationType.mortgage)
                )
            )

        return (
            + ssa2018_65_2_a
            + ssa2018_65_2_b
            + ssa2018_65_2_c
            + ssa2018_65_2_d
            )
