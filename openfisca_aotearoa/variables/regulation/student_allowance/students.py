"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class student_allowance__tertiary_student(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "is a tertiary student"
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM259980"
    definition_period = periods.DateUnit.MONTH
    default_value = False


class student_allowance__secondary_student(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "is a secondary student"
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM259943"
    definition_period = periods.DateUnit.MONTH
    default_value = False
