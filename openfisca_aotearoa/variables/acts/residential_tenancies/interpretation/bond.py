"""Residential tenancies' bond.

Bond is any money, excluding rent, to be paid under a tenancy agreement by the
tenant, as security for the observance and performance of the tenancy.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class residential_tenancies__bond(variables.Variable):
    label = "Residential tenancies' bond"
    reference = "https://www.legislation.govt.nz/act/public/1986/0120/latest/DLM94283.html"
    documentation = """
        Bond is any money, excluding rent, to be paid under a tenancy agreement
        by the tenant, as security for the observance and performance of the tenancy.
        """
    entity = entities.Tenancy
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK
