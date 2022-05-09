"""TODO: Add missing doctring."""

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class student_allowance__is_tertiary_student(Variable):
    value_type = bool
    entity = Person
    label = "is a tertiary student"
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM259980"
    definition_period = MONTH
    default_value = False


class student_allowance__is_secondary_student(Variable):
    value_type = bool
    entity = Person
    label = "is a secondary student"
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM259943"
    definition_period = MONTH
    default_value = False
