"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class home_help__multiple_birth(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Had a multiple birth from the same pregnancy"
    reference = "https://www.workandincome.govt.nz/map/legislation/welfare-programmes/home-help-programme/index.html"


class home_help__adopted_2_or_more_children(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Have or adopted twins, and already has another child under 5."
    reference = "https://www.workandincome.govt.nz/map/legislation/welfare-programmes/home-help-programme/index.html"


class home_help__no_immediate_family(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Has no immediate family or anyone else living with you who can help"
    reference = "https://www.workandincome.govt.nz/map/legislation/welfare-programmes/home-help-programme/index.html"


class home_help__eligible_for_home_help(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Eligible for Home Help"
    reference = "https://www.workandincome.govt.nz/map/legislation/welfare-programmes/home-help-programme/index.html"

    def formula(persons, period, parameters):
        resident_or_citizen = persons("immigration__citizen_or_resident", period)
        in_nz = persons("social_security__ordinarily_resident_in_new_zealand", period)

        # TODO this formula needs review as it lacks age requirements
        return resident_or_citizen * in_nz * persons.has_role(entities.Family.PRINCIPAL) *\
            (
                persons("home_help__multiple_birth", period)
                + persons("home_help__adopted_2_or_more_children", period)
                + (
                    (persons("social_security__dependent_children", period.first_week) > 0) * persons("home_help__no_immediate_family", period)
                    * (persons("community_services_card", period) + persons("social_security__eligible_for_community_services_card", period))
                    )
                )
