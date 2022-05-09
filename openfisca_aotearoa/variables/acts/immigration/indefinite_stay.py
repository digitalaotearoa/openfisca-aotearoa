"""TODO: Add missing doctring."""

from openfisca_core.periods import DAY
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class immigration__entitled_to_indefinite_stay(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "is entitled in terms of the Immigration Act 2009 to be in New Zealand indefinitely"
    reference = "http://www.legislation.govt.nz/act/public/2009/0051/latest/DLM1440303.html"
