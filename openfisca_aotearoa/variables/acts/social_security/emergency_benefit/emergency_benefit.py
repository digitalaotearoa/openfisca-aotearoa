"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities

class emergency_benefit__entitled(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "TODO"
    definition_period = periods.DateUnit.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783236"


class emergency_benefit__granted(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person is currently granted the Emergency benefit"
    definition_period = periods.DateUnit.WEEK
    reference = "Reference is unclear, but variable is utilised by the phrase: 'granted a main benefit'"


class emergency_benefit__receiving(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person is currently recieving/being paid the emergency benefit"
    definition_period = periods.DateUnit.WEEK
    reference = "Reference is unclear, but concept underpinning the variable assumes it covers both: 'being paid a main benefit' or 'recieving a benefit'"


class emergency_benefit__base(variables.Variable):
    value_type = float
    default_value = 0
    entity = entities.Person
    label = "TODO"
    definition_period = periods.DateUnit.WEEK
    reference = "TODO"
