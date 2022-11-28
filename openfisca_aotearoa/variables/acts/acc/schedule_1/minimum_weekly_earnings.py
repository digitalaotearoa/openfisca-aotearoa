"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class acc_sched_1__minimum_weekly_earnings(variables.Variable):
    value_type = float
    entity = entities.Person
    definition_period = periods.DateUnit.DAY
    label = "Minimum weekly earnings"
    reference = "http://www.legislation.govt.nz/act/public/2001/0049/latest/DLM104874.html"
