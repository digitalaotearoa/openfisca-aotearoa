"""TODO: Add missing doctring."""

from openfisca_core import periods, variables
from openfisca_aotearoa import entities


class social_security__granted_main_benefit(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Person is granted a main benefit"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784575"

    def formula(persons, period, parameters):
        a = persons("jobseeker_support__granted", period) + \
            persons("sole_parent_support__granted", period) + \
            (persons("supported_living_payment__granted", period) * (persons("supported_living_payment__restricted_work_capacity", period) + persons("totally_blind", period))) + \
            (persons("supported_living_payment__granted", period) * persons("supported_living_payment__caring_for_another_person", period)) + \
            persons("youth_payment__granted", period) + \
            persons("young_parent_payment__granted", period) + \
            persons("emergency_benefit__granted", period)
        # b - is defined in section 349 for the purposes of sections 349 to 352
        return a


class social_security__receiving_main_benefit(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Person is recieving/being paid a main benefit"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784575"

    def formula(persons, period, parameters):
        a = persons("jobseeker_support__receiving", period) + \
            persons("sole_parent_support__receiving", period) + \
            persons("supported_living_payment__receiving", period) + \
            persons("youth_payment__receiving", period) + \
            persons("young_parent_payment__receiving", period) + \
            persons("emergency_benefit__receiving", period)
        # b - is defined in section 349 for the purposes of sections 349 to 352
        return a


class social_security__beneficiary(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Person who has been granted a benefit"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784416"


# This only applies to 1964 ACT, DO NOT USE FOR 2018 - instead refer to either social_security__beneficiary or social_security__granted_main_benefit
# Is this also main benefits only?
# jobseeker, youth payment, young parent payment, emergency benefit,
class social_security__a_beneficiary(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Person is a beneficiary"
    definition_period = periods.MONTH
    reference = "http://www.legislation.govt.nz/act/public/1964/0136/latest/DLM362802.html#DLM362810"

    def formula(persons, period, parameters):
        return persons("social_security__paid_jobseeker_benefit", period) + \
            persons("social_security__paid_sole_parent_support", period) + \
            persons("social_security__paid_a_supported_living_payment", period) + \
            persons("social_security__paid_a_youth_payment", period) + \
            persons("social_security__paid_a_young_parent_payment", period) + \
            persons("social_security__paid_an_emergency_benefit", period) + \
            persons("super__being_paid_nz_superannuation", period) + \
            persons("veterans_support__being_paid_a_veterans_pension", period)


# This only applies to 1964 ACT, DO NOT USE FOR 2018
class social_security__paid_jobseeker_benefit(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is being paid Jobseeker"
    definition_period = periods.MONTH


# This only applies to 1964 ACT, DO NOT USE FOR 2018
class social_security__paid_sole_parent_support(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is being paid sole parent support"
    definition_period = periods.MONTH


# This only applies to 1964 ACT, DO NOT USE FOR 2018
class social_security__paid_a_supported_living_payment(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is being paid a supported living payment"
    definition_period = periods.MONTH


# This only applies to 1964 ACT, DO NOT USE FOR 2018
class social_security__paid_a_youth_payment(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is being paid a a youth payment"
    definition_period = periods.MONTH


# This only applies to 1964 ACT, DO NOT USE FOR 2018
class social_security__paid_a_young_parent_payment(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is being paid a a young parent payment"
    definition_period = periods.MONTH


# This only applies to 1964 ACT, DO NOT USE FOR 2018
class social_security__paid_an_emergency_benefit(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Is being paid a young parent payment"
    definition_period = periods.MONTH
