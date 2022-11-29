"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities

# Re-usable variable for having a partner


# Likely to be removed/renamed, needs to be tied to a definition
class is_adequately_supported_by_partner(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = """Is adequately supported by their partner? (false if lost the regular support of
    their partner as their partner has been imprisoned or is subject to release or detention conditions that prevent employment)
    """
    definition_period = periods.MONTH
    reference = "https://www.workandincome.govt.nz/map/income-support/main-benefits/sole-parent-support/qualifications.html"
    default_value = True


# Likely to be removed/renamed, needs to be tied to a definition
class person_is_step_parent(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Is a step-parent?"
