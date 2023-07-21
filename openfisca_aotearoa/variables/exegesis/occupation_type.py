"""Exegesis — Occupation type.

The type of occupation of a premise.

Can be either rent, board, or ownership.

"""

from openfisca_core import indexed_enums, periods, variables

from openfisca_aotearoa import entities


class OccupationType(indexed_enums.Enum):
    unknown = "Unknown"
    rent = "Rent"
    board = "Board"
    ownership = "Ownership"


class occupation_type(variables.Variable):
    label = "Exegesis — Occupation type"
    reference = "https://en.wiktionary.org/wiki/occupation#English"
    documentation = """Can be rent, board, or ownership."""
    entity = entities.Premise
    value_type = indexed_enums.Enum
    possible_values = OccupationType
    default_value = OccupationType.unknown
    definition_period = periods.DateUnit.WEEK
