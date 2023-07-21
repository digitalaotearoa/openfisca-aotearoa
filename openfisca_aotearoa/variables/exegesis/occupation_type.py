"""Exegesis — Occupation type.

The intended or actual occupation of a premise by a person.

Can be either residential or non-residential.

"""

from openfisca_core import indexed_enums, periods, variables

from openfisca_aotearoa import entities


class OccupationType(indexed_enums.Enum):
    unknown = "Unknown"
    residential = "Residential"
    non_residential = "Non-residential"


class occupation_type(variables.Variable):
    label = "Exegesis — Occupation type"
    reference = "https://en.wiktionary.org/wiki/occupation#English"
    documentation = """Can be either residential or non-residential."""
    entity = entities.Person
    value_type = indexed_enums.Enum
    possible_values = OccupationType
    default_value = OccupationType.unknown
    definition_period = periods.DateUnit.WEEK
