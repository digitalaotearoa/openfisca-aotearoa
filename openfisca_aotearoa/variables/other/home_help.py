"""TODO: Add missing doctring."""

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Family, Person


class home_help__had_multiple_birth(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Had a multiple birth from the same pregnancy"
    reference = "https://www.workandincome.govt.nz/map/legislation/welfare-programmes/home-help-programme/index.html"


class home_help__adopted_2_or_more_children(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Have or adopted twins, and already has another child under 5."
    reference = "https://www.workandincome.govt.nz/map/legislation/welfare-programmes/home-help-programme/index.html"


class home_help__has_no_immediate_family(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Has no immediate family or anyone else living with you who can help"
    reference = "https://www.workandincome.govt.nz/map/legislation/welfare-programmes/home-help-programme/index.html"


class home_help__eligible_for_home_help(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Eligible for Home Help"
    reference = "https://www.workandincome.govt.nz/map/legislation/welfare-programmes/home-help-programme/index.html"

    def formula(persons, period, parameters):
        resident_or_citizen = persons("is_citizen_or_resident", period)
        in_nz = persons("social_security__is_ordinarily_resident_in_new_zealand", period)

        return resident_or_citizen * in_nz * persons.has_role(Family.PRINCIPAL_CAREGIVER) *\
            (
                persons("home_help__had_multiple_birth", period)
                + persons("home_help__adopted_2_or_more_children", period)
                + (
                    persons("dependent_child", period) * persons("home_help__has_no_immediate_family", period)
                    * (persons("has_community_services_card", period) + persons("social_security__eligible_for_community_services_card", period))
                    )
                )
