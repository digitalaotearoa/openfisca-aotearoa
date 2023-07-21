"""Residential tenancies — Tenancy.

A tenancy is the right to rent (and occupy) a residential premise.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.exegesis.occupation_lawfulness import (
    OccupationLawfulness,
    )
from openfisca_aotearoa.variables.exegesis.occupation_type import (
    OccupationType,
    )


class residential_tenancies__tenancy(variables.Variable):
    label = "Residential tenancies — Tenancy"
    reference = "https://www.legislation.govt.nz/act/public/1986/0120/latest/DLM94283.html"
    documentation = """Right to rent (and occupy) a residential premise."""
    entity = entities.Premise
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula_1987_02_01(premises, period, _params):
        # tenancy,

        # in relation to any residential premises,
        residential = premises(
            "residential_tenancies__residential_premise",
            period,
            )

        # means the right to occupy the premises (whether exclusively or
        # otherwise)
        occupation_lawfulness = premises("occupation_lawfulness", period)
        legal_occupation = occupation_lawfulness == OccupationLawfulness.legal

        # in consideration for rent;
        occupation_type = premises("occupation_type", period)
        rent_occupation = occupation_type == OccupationType.rent

        # and includes any tenancy of residential premises implied or created
        # by any enactment; and, where appropriate, also includes a former
        # tenancy

        return residential * legal_occupation * rent_occupation
