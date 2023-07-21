"""Exegesis — Occupation lawfulness.

The legality of the occupation of a premise.

Can be either legal, or illegal.

"""

from openfisca_core import indexed_enums, periods, variables

from openfisca_aotearoa import entities


class OccupationLawfulness(indexed_enums.Enum):
    unknown = "Unknown"
    legal = "Legal"
    illegal = "Illegal"


class occupation_lawfulness(variables.Variable):
    label = "Exegesis — Occupation lawfulness"
    reference = "https://en.wiktionary.org/wiki/occupation#English"
    documentation = """Can be legal, or illegal."""
    entity = entities.Premise
    value_type = indexed_enums.Enum
    possible_values = OccupationLawfulness
    default_value = OccupationLawfulness.unknown
    definition_period = periods.DateUnit.WEEK
