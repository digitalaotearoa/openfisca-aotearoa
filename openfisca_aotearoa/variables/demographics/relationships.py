"""TODO: Add missing doctring."""

from openfisca_core import holders, periods, variables

from openfisca_aotearoa import entities

# Re-usable variable for having a partner


class in_a_relationship(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Common definition of 'in a relationship', note can also be set to true through use of the partner role in a family"
    definition_period = periods.WEEK  # This variables.variable changes over time.
    reference = "This is a common definition utilsed in at least both the Social Security Act 2018 and the Income Tax Act 2007"
    set_input = holders.set_input_dispatch_by_period

    def formula(people, period, _params):
        married = people("marriage__married", period.first_month)
        civil_union = people("civil_union__civil_union", period.first_month)
        de_facto_rel = people("property_relationships__de_facto_relationship", period.first_month)
        relationship = people.family.nb_persons(entities.Family.PARTNER) > 0

        return (
            + people.has_role(entities.Family.PRINCIPAL)
            * (married + civil_union + de_facto_rel + relationship)
            )


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
