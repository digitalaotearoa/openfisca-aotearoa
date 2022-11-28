"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class student_allowance__partner_or_person_receiving_certain_allowances(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    reference = "http://www.legislation.govt.nz/regulation/public/1998/0277/latest/DLM260340.html"
    label = "Student not eligible for certain allowances where student or spouse or partner receiving social security payments, New Zealand superannuation, or veteran’s pension"

# not using social_security__received_income_tested_benefit here because
# a) student allowances eligibility also apply to spouse
# b) the "orphan's benefit" and "unsupported child’s benefit" appear to be excluded
