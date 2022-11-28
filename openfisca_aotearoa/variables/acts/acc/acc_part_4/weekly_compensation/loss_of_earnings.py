"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class weekly_compensation__loss_of_earnings_payable(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Engaged in full-time study or training, does not include full-time study or training in living or social skills"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104891.html"
