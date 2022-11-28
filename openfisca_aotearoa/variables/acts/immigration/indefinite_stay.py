"""TODO: Add missing doctring."""

from openfisca_core import periods, variables
from openfisca_core.holders import set_input_dispatch_by_period

from openfisca_aotearoa.entities import Person


class immigration__entitled_to_indefinite_stay(variables.Variable):
    value_type = bool
    entity = Person
    definition_period = periods.DAY
    label = "is entitled in terms of the Immigration Act 2009 to be in New Zealand indefinitely"
    reference = "http://www.legislation.govt.nz/act/public/2009/0051/latest/DLM1440303.html"
    set_input = set_input_dispatch_by_period
