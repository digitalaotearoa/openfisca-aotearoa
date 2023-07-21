"""Residential tenancies — Bond.

Bond is any money, excluding rent, to be paid under a tenancy agreement by the
tenant, as security for the observance and performance of the tenancy.

"""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class residential_tenancies__bond(variables.Variable):
    label = "Residential tenancies — Bond"
    reference = "https://www.legislation.govt.nz/act/public/1986/0120/latest/DLM94283.html"
    documentation = """
        Any money, excluding rent, to be paid under a tenancy agreement by the
        tenant, as security for the observance and performance of the tenancy.
        """
    entity = entities.Tenancy
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_1987_02_01(tenancy, period, _params):
        tenants = tenancy.members("residential_tenancies__tenant", period)

        # bond means any sum of money payable or paid under a tenancy agreement
        # as security for the observance and performance of the tenant’s
        # obligations under the agreement and this Act;
        housing_costs = tenancy.members("housing_costs", period)
        rta1986_2_bond_a = tenancy.sum(housing_costs * tenants)

        # but does not include any sum payable or paid by way of rent
        rent = tenancy("residential_tenancies__rent", period)
        rta1986_2_bond_b = rent * tenants.any()

        return numpy.maximum(rta1986_2_bond_a - rta1986_2_bond_b, 0)
