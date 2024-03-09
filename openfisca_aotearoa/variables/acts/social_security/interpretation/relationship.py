"""This module provides eligibility and amount for Jobseeker Support."""

from openfisca_core import holders, periods, variables

from openfisca_aotearoa import entities


# TODO: Review against the new 2018 act
class social_security__been_married_or_civil_union_or_de_facto_relationship(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "Has been married or in a civil union or de facto relationship"
    reference = "https://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM4686082"


class social_security__parent(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Is a parent?"
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784624", "ssa/221/en#sd2-d138"


class social_security__principal_caregiver(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Principal Caregiver in relation to a dependent child"
    set_input = holders.set_input_dispatch_by_period
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784655", "ssa/221/en#sd2-d155", "https://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM360463"


class social_security__temporary_ob_or_ucb_caregiver(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Principal Temporary  Caregiver in relation to a child AND is entitled to and receiving an orphan’s benefit or an unsupported child’s benefit for the child"
    set_input = holders.set_input_dispatch_by_period
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS515263", "ssa/221/en#sd2-d216"


class social_security__care_and_control(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "The person for the time being having the care and control of the child"
    set_input = holders.set_input_dispatch_by_period
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783275", "ssa/221/en#s82-l1"
