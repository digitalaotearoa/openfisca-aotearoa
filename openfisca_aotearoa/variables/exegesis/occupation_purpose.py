"""Exegesis — Occupation type.

The purpose of the occupation of a premise by a person.

Can be either residential or non-residential.

"""

from openfisca_core import indexed_enums, periods, variables

from openfisca_aotearoa import entities


class OccupationPurpose(indexed_enums.Enum):
    unknown = "Unknown"
    residential = "Residential"
    non_residential = "Non-residential"


class occupation_purpose(variables.Variable):
    label = "Exegesis — Occupation purpose"
    reference = "https://en.wiktionary.org/wiki/occupation#English"
    documentation = """Can be either residential or non-residential."""
    entity = entities.Premise
    value_type = indexed_enums.Enum
    possible_values = OccupationPurpose
    default_value = OccupationPurpose.unknown
    definition_period = periods.DateUnit.WEEK
