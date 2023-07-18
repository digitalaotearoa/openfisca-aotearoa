"""Residential tenancies' rent.

Rent is any valuable, including money, goods, services, and excluding bond, to
be paid under a tenancy agreement by the tenant.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class residential_tenancies__rent(variables.Variable):
    label = "Residential tenancies' rent"
    reference = "https://www.legislation.govt.nz/act/public/1986/0120/latest/DLM94283.html"
    documentation = """
        Rent is any valuable, including money, goods, services, and excluding
        bond, to be paid under a tenancy agreement by the tenant.
        """
    entity = entities.Tenancy
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_1987_02_01(tenancy, period, _params):
        tenant = tenancy("residential_tenancies__tenant", period)

        # rent means any money, goods, services, or other valuable
        # consideration in the nature of rent to be paid or supplied under a
        # tenancy agreement by the tenant;
        housing_costs = tenancy.members("housing_costs", period)
        rta1986_2_rent_a = housing_costs * tenant

        # but does not include any sum of money payable or paid by way of bond
        bond = tenancy("residential_tenancies__bond", period)
        rta1986_2_rent_b = bond * tenant

        return rta1986_2_rent_a - rta1986_2_rent_b
