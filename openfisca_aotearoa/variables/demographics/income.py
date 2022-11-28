"""TODO: Add missing doctring."""

from openfisca_core import holders, periods, variables

from openfisca_aotearoa import entities


class yearly_income(variables.Variable):
    value_type = float
    entity = entities.Person
    label = "Yearly income of this person"
    definition_period = periods.DateUnit.YEAR
    reference = "TODO"
    unit = "NZD"
    set_input = holders.set_input_divide_by_period


class monthly_income(variables.Variable):
    value_type = float
    entity = entities.Person
    label = "Monthly income of this person"
    definition_period = periods.DateUnit.MONTH
    reference = "One twelfth of their yearly income"
    unit = "NZD"


class weekly_income(variables.Variable):
    value_type = float
    entity = entities.Person
    label = "Weekly income of this person"
    definition_period = periods.DateUnit.WEEK
    reference = "One 52th of their yearly income"
    unit = "NZD"
