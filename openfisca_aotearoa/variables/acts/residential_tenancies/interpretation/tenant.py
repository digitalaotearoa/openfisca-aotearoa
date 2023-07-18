"""Residential tenancies' tenant.

Tenant is the grantee of a tenancy of a premise under a tenancy agreement.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class residential_tenancies__tenant(variables.Variable):
    label = "Residential tenancies' tenant"
    reference = "https://www.legislation.govt.nz/act/public/1986/0120/latest/DLM94283.html"
    documentation = """
        Tenant is the grantee of a tenancy of a premise under a tenancy
        agreement.
        """
    entity = entities.Tenancy
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula_1987_02_01(people, _period, _params):
        # tenant, in relation to any residential premises that are the subject
        # of a tenancy agreement, means the grantee of a tenancy of the
        # premises under the agreement; and, where appropriate, includes—
        # (a) a prospective tenant; and
        # (b) a former tenant; and
        # (c) a lawful successor in title of a tenant to the premises; and
        # (d) the personal representative of a deceased tenant; and
        # (e) an agent of a tenant
        return people.has_role(entities.Tenancy.TENANT)
