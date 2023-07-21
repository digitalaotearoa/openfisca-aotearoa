"""Residential tenancies — Residential premise.

Residential premise is a premise used or intended for occupation by any person
as a place of residence, unlawfully or not.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.exegesis.occupation_purpose import (
    OccupationPurpose,
    )


class residential_tenancies__residential_premise(variables.Variable):
    label = "Residential tenancies — Residential premise"
    reference = "https://www.legislation.govt.nz/act/public/1986/0120/latest/DLM94283.html"
    documentation = """Premise occupied for residence unlawfully or not."""
    entity = entities.Premise
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula_1987_02_01(premises, period, _params):
        # residential premises means any premises used or intended for
        # occupation by any person as a place of residence whether or not the
        # occupation or intended occupation for residential purposes is or
        # would be unlawful
        occupation_purpose = premises("occupation_purpose", period)

        return occupation_purpose == OccupationPurpose.residential
