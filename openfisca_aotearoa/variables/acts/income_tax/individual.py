"""TODO: Add missing doctring."""

from openfisca_core.holders import set_input_dispatch_by_period
from openfisca_core import periods, variables

# Import the entities specifically defined for this tax and benefit system
from openfisca_aotearoa import entities


class income_tax__residence(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    set_input = set_input_dispatch_by_period
    default_value = True
    label = "Boolean for if a Person is classified as meeting residence requirements"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1518482.html"


class income_tax__annual_gross_income(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.YEAR
    label = "Annual gross income"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1512333.html"


class income_tax__annual_total_deduction(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.YEAR
    label = "Annual total deduction"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1512336.html"


class income_tax__net_income(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.YEAR
    label = "Net income"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1512339.html"

    def formula(person, period, parameters):
        net_income = person("income_tax__annual_gross_income", period) - person("income_tax__annual_total_deduction", period)

        return (
            net_income * (net_income > 0)
            )


class income_tax__net_loss(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.YEAR
    label = "Net loss"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1512339.html"

    def formula(person, period, parameters):
        net_loss = person("income_tax__annual_gross_income", period) - person("income_tax__annual_total_deduction", period)

        return (
            net_loss * (net_loss < 0)
            )


class income_tax__available_tax_loss(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.YEAR
    label = "Available tax loss"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1520575.html#DLM1520774"


class income_tax__taxable_income(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.YEAR
    label = "A person's taxable income for a tax year"
    reference = "http://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1512344.html"

    def formula(person, period, parameters):
        taxable_income = (person("income_tax__net_income", period) - person("income_tax__available_tax_loss", period))

        return (
            taxable_income * (taxable_income > 0)
            )
