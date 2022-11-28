"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class veterans_support__received_parents_allowance(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Is classified as receiving a parent's allowance"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/whole.html#DLM1518484"


class veterans_support__received_childrens_pension(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Is classified as receiving a children's pension"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/whole.html#DLM1518484"


class veterans_support__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.WEEK
    label = "Applicant is a entitled to be paid veterans pension in a Pacific country"
    reference = "http://www.legislation.govt.nz/act/public/2014/0056/latest/DLM5537707.html"


class veterans_support__being_paid_a_veterans_pension(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is being paid a Veteran's Pension"
    definition_period = periods.DateUnit.MONTH


class veterans_pension__entitled(variables.Variable):
    label = "TODO"
    reference = "TODO"
    documentation = """TODO"""
    entity = entities.Person
    value_type = bool
    default_value = False
    definition_period = periods.DateUnit.WEEK


class veterans_pension__base(variables.Variable):
    label = "TODO"
    reference = "TODO"
    documentation = """TODO"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK
