"""Residential tenancies — Residential premise.

Residential premise is a premise used or intended for occupation by any person
as a place of residence, unlawfully or not.

"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities
from openfisca_aotearoa.variables.exegesis.occupation_type import OccupationType


class residential_tenancies__residential_premise(variables.Variable):
    label = "Residential tenancies — Residential premise"
    reference = "https://www.legislation.govt.nz/act/public/1986/0120/latest/DLM94283.html"
    documentation = """a premise occupied for residence unlawfully or not."""
    entity = entities.Premise
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK

    def formula_1987_02_01(premises, period, _params):
        # residential premises means

        # any premises used or intended for occupation by any person
        occupant = premises.members("occupant", period)

        # as a place of residence
        occupation_type = premises.members("occupation_type", period)
        residence = occupation_type == OccupationType.residential

        # whether or not the occupation or intended occupation for residential
        # purposes is or would be unlawful

        return premises.sum(occupant * residence)
