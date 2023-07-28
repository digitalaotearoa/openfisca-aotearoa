"""Residential tenancies — Tenant.

Tenant is the grantee of a tenancy of a premise under a tenancy agreement.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class residential_tenancies__tenant(variables.Variable):
    label = "Residential tenancies — Tenant"
    reference = "https://www.legislation.govt.nz/act/public/1986/0120/latest/DLM94283.html"
    documentation = """Grantee of a tenancy of a premise under agreement."""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK
