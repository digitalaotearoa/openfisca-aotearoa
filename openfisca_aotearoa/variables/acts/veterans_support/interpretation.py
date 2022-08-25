"""TODO: Add missing doctring."""

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class veterans_support__received_parents_allowance(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Is classified as receiving a parent's allowance"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/whole.html#DLM1518484"


class veterans_support__received_childrens_pension(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Is classified as receiving a children's pension"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/whole.html#DLM1518484"


class veterans_support__entitled(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Applicant is a entitled to be paid veterans pension in a Pacific country"
    reference = "http://www.legislation.govt.nz/act/public/2014/0056/latest/DLM5537707.html"


class veterans_support__being_paid_a_veterans_pension(Variable):
    value_type = bool
    entity = Person
    label = "Is being paid a Veteran's Pension"
    definition_period = MONTH
