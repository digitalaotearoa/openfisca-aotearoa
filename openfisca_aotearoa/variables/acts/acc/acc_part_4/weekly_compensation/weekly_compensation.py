"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class weekly_compensation__lodges_a_claim(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "A claimant who has cover and who lodges a claim for weekly compensation"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM100910.html"
