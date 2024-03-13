"""TODO: Add missing doctring."""

from openfisca_core import holders
from openfisca_core.periods import DAY, MONTH
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class student_allowance__childless(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "childless means not having a supported child or children"
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM259374"


class student_allowance__combined_income(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "the personal income of that student; and the spousal or partner’s income of that student"
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM259377"


class student_allowance__dependent_student(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "is a dependent student"
    """dependent student, in relation to a parent whose income is being assessed, means a child of that parent—
    (a) who is attending a full-time course at a tertiary provider or a secondary school; and
    (b) who is not younger than 16 on 31 December in the year before the year of application
        and is not older than 23 on 1 January in the year of application; and
    (c) who has not been awarded an independent circumstances grant; and
    (d) in respect of whom an orphan’s benefit is not paid; and
    (e) in respect of whom an unsupported child’s benefit is not paid; and
    (f) who receives financial support from that parent"""
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM259381"


class student_allowance__income_before_tax(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = """income before tax includes gains before tax and profits before tax"""


class student_allowance__living_with_a_parent(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = """living with a parent has the same meaning as in section 3(1) of the Social Security Act 1964"""
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM259900"


class student_allowance__married_or_partnered(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "married or partnered as per Student Allowances Regulations 1998"
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM259902"
    set_input = holders.set_input_dispatch_by_period

    def formula(persons, period, parameters):
        return persons("student_allowance__person_has_spouse", period)


class student_allowance__supported_child(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "has a supported child as per Student Allowances Regulations 1998"
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM259968"
    set_input = holders.set_input_dispatch_by_period


class student_allowance__partner_has_a_supported_child(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "their spouse has a supported child, as per Student Allowances Regulations 1998"
    reference = "www.legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM6530648"


class student_allowance__person_has_spouse(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = "Has spouse as per Student Allowances Regulations 1998"
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM259958"
    set_input = holders.set_input_dispatch_by_period
    def formula(persons, period, parameters):
        # NOTE: using the age at the start of the month
        # Age changes on a DAY, but this calculation only has a granularity of MONTH
        part_a = (persons("age", period) >= 24) * (persons("age_of_partner", period) >= 24)
        part_b = ((persons("age", period) >= 24) + (persons("age_of_partner", period) >= 24)) * \
            (persons("student_allowance__supported_child", period.start) + persons("student_allowance__partner_has_a_supported_child", period))

        return part_a + part_b


class student_allowance__student(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "student means a person who is enrolled or intends to enrol in a recognised course of study"
    reference = "http://legislation.govt.nz/regulation/public/1998/0277/latest/whole.html#DLM259958"

    def formula(persons, period, parameters):
        return persons("student_allowance__tertiary_student", period) + persons("student_allowance__secondary_student", period)
