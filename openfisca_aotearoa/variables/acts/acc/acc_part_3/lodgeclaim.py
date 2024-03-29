"""TODO: Add missing doctring."""

from openfisca_core.periods import ETERNITY
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class acc_part_3__lodged_claim(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = "Has lodged a claim with the Corporation"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM100910.html"

    def formula(persons, period, parameters):
        return (
            persons("acc__lodged_claim_for_cover_for_personal_injury", period)
            + persons("acc__lodged_claim_for_cover_and_specified_entitlement_for_personal_injury", period)
            + persons("acc__assessed_as_having_a_need_caused_by_this_covered_injury", period)
            )

# Missing variables
# acc__lodged_claim_for_cover_and_specified_entitlement_for_personal_injury
# acc__assessed_as_having_a_need_caused_by_this_covered_injury
