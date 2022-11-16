"""TODO: Add missing doctring."""

from numpy import logical_not as not_

from openfisca_core import periods, variables, holders
from openfisca_aotearoa import entities

# Benefit: Part 1E Supported Living Payment (eligible self applicant):
# If applicant.isNZResident
#     and 16 <= applicant.Age
#     and applicant.hasMedicalCertificate
#     and applicant.hasSeriousDisability
#     and threshold.income.SupportedLivingPayment
# then benefit.isSupportedLivingPayment is PERMITTED


class supported_living_payment__granted(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person is currently granted the supported living benefit"
    definition_period = periods.WEEK
    reference = "Reference is unclear, but variable is utilised by the phrase: 'granted a main benefit'"


class supported_living_payment__caring_for_another_person(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Eligible for Supported Living Payment."
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783187"
    set_input = holders.set_input_dispatch_by_period


class supported_living_payment__below_income_threshold(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Income below threshold for supported living payment"
    reference = "TODO"


class supported_living_payment__restricted_work_capacity(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Is incapable of regularly working 15 or more hours a week in open employment"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783176", "http://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM5468367"
    set_input = holders.set_input_dispatch_by_period


# TODO: Review against the new 2018 act
class supported_living_payment__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Eligible for Supported Living Payment."
    reference = """
        http://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM5468367
        40A Supported living payment: purpose
        (1) The purpose of the supported living payment is to provide income support
            to people because they are people who fall within any one of the following 3 categories:
        (a) people who have, and are likely to have in the future, a severely restricted
            capacity to support themselves through open employment because of sickness, injury, or disability:
        (b) people who are totally blind:
        (c) people who are required to give full-time care and attention at home to some
            other person (other than their spouse or partner) who is a patient requiring care.
    """

    def formula(persons, period, parameters):
        # The 3 ways of being eligible
        disabled = persons("supported_living_payment__restricted_work_capacity", period.first_week)
        blind = persons("totally_blind", period)
        carer = persons("supported_living_payment__caring_for_another_person", period.first_week)

        # 40B (4) A person who is not both permanently and severely restricted in his or her capacity for
        # work must not be granted a supported living payment under this section, unless he or she is totally blind.

        # 40B (5) A person must not be granted a supported living payment under this section if the chief
        # executive is satisfied that the person's restricted capacity for work, or total blindness, was
        # self-inflicted and brought about by the person with a view to qualifying for a benefit.
        not_self_inflicted = not_(persons("social_security__disability_self_inflicted", period))

        # 40B (1A) An applicant for the supported living payment under
        # this section must be aged at least 16 years.
        is_old_enough = persons("age", period.start) >= 16

        # 40B (1B) An applicant for the supported living payment under
        # this section must meet the residential requirements in section 74AA.
        immigration__resident_or_citizen = persons("immigration__citizen_or_resident", period)

        resides_in_nz = persons("social_security__residential_requirement", period.first_week)

        # # income low enough?
        income = persons("supported_living_payment__below_income_threshold", period)

        return resides_in_nz * (disabled + blind + carer) * not_self_inflicted * is_old_enough * immigration__resident_or_citizen * income
