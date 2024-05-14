"""This module provides eligibility and amount for Supported Living Payment."""
import numpy

from openfisca_core import holders, periods, variables

from openfisca_aotearoa import entities


class supported_living_payment__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period
    label = "Eligible for Supported Living Payment."
    reference = [
        "https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783175",
        "http://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM5468367",
        ]

    def formula_2013_07_15(persons, period, parameters):
        """
        For the 1964 version of the act (final version), this is split into two sections:
            40B on ground of sickness, injury, disability, or total blindness
            40D on ground of caring for patient requiring care
        """
        ssa40B = persons("supported_living_payment__disabled_or_blind__entitled", period, parameters)
        ssa40D = persons("supported_living_payment__carer__entitled", period, parameters)
        return ssa40B + ssa40D

    def formula_2018_11_26(persons, period, parameters):
        """
        For the 2018 version of the act, this is split into two sections:
            34 - 39 on ground of restricted work capacity or total blindness
            40 - 42 on ground of caring for another person
        """
        ssa34 = persons("supported_living_payment__disabled_or_blind__entitled", period, parameters)
        ssa40 = persons("supported_living_payment__carer__entitled", period, parameters)

        # ssa116 - must undergo work ability assessment

        # ssa117 - unless they are terminally ill or their condition will not "improve"

        # ssa121_e - spouse must undertake work-preparation obligations

        # ssa128 - children must atend school & healthcare, person required to attend interviews

        # ssa140 - spouse must be available to work

        # ssa170 - person or spouse must work with service providers

        return ssa34 + ssa40


class supported_living_payment__disabled_or_blind__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Eligible for Supported Living Payment, on ground of restricted work capacity or total blindness."
    reference = [
        "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783174",
        ]

    def formula_2018_11_26(persons, period, parameters):
        # person P has restricted work capacity or is totally blind
        ssa34_a = persons("supported_living_payment__restricted_work_capacity", period.first_week) + persons("totally_blind", period.start)

        # person P meets the residential requirement
        ssa34_b = persons("social_security__residential_requirement", period.first_week)

        # person P is 16 or older
        ssa34_c = persons("age", period.start) >= 16

        # ssa35 specifies requirements for restricted work capacity status

        # person P is ineligible if the disability was self-inflicted to gain benefits
        ssa36 = numpy.logical_not(persons("supported_living_payment__disability_self_inflicted", period))

        # ssa37 specifies medical examination for reassessment of work capacity

        # ssa38 specifies payment rates for person P and partner / spouse S if applicable

        # ssa39 specifies open employment is permitted for reassessment of work capacity

        return ssa34_a * ssa34_b * ssa34_c * ssa36

    def formula(persons, period, parameters):
        # person P has restricted work capacity
        ssa40B_1_a = persons("supported_living_payment__restricted_work_capacity", period.first_week)

        # person P is totally blind
        ssa40B_1_b = persons("totally_blind", period)

        # person P is 16 or older
        ssa40B_1A = persons("age", period.start) >= 16

        # person P meets the residential requirement
        ssa40B_1B = persons("social_security__residential_requirement", period.first_week)

        ssa40B_1 = ssa40B_1A * ssa40B_1B * (ssa40B_1_a + ssa40B_1_b)

        # 40B_2 specifies requirements for restricted work capacity status

        # 40B_3 specifies requirements for restricted work capacity status

        # 40B_4 (redundantly?) states that person P must be either totally blind or permanently disabled

        # person P is ineligible if the disability was self-inflicted to gain benefits
        ssa40B_5 = numpy.logical_not(persons("supported_living_payment__disability_self_inflicted", period))

        return ssa40B_1 * ssa40B_5


class supported_living_payment__carer__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Eligible for Supported Living Payment, on grounds of caring for another person."
    reference = [
        "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783187",
        ]

    def formula_2013_07_15(persons, period, parameters):
        # person C is caring for person P
        ssa40D_1 = persons("supported_living_payment__caring_for_another_person", period.first_week)

        # person C is at least 18 years old if they have no dependent children
        ssa40D_2_a = (persons("age", period.start) >= 18) * (persons("social_security__dependent_children", period.first_week) == 0)

        # person C is at least 19 years old otherwise (i.e.: they have dependent children)
        ssa40D_2_b = persons("age", period.start) >= 19

        ssa40D_2 = ssa40D_2_a + ssa40D_2_b

        # person C meets the residential requirement
        ssa40D_3 = persons("social_security__residential_requirement", period.first_week)

        # ssa40D_4 allows for payment to continue if not caring for 28 days

        return ssa40D_1 * ssa40D_2 * ssa40D_3

    def formula_2016_10_25(persons, period, parameters):
        # person C is caring for person P
        ssa40D_1 = persons("supported_living_payment__caring_for_another_person", period.first_week)

        # person C is at least 18 years old if they have no dependent children
        ssa40D_2_a = (persons("age", period.start) >= 18) * (persons("social_security__dependent_children", period.first_week) == 0)

        # person C is at least 20 years old otherwise (i.e.: they have dependent children)
        ssa40D_2_b = persons("age", period.start) >= 20

        ssa40D_2 = ssa40D_2_a + ssa40D_2_b

        # person C meets the residential requirement
        ssa40D_3 = persons("social_security__residential_requirement", period.first_week)

        # ssa40D_4 allows for payment to continue if not caring for 28 days

        return ssa40D_1 * ssa40D_2 * ssa40D_3

    def formula_2018_11_26(persons, period, parameters):
        # person C is caring for person P
        ssa40_1_a = persons("supported_living_payment__caring_for_another_person", period.first_week)

        # person C meets the residential requirement
        ssa40_1_b = persons("social_security__residential_requirement", period.first_week)

        # person C is at least 18 years old if they have no dependent children
        ssa40_1_c_i = (persons("age", period.start) >= 18) * (persons("social_security__dependent_children", period.first_week) == 0)

        # person C is at least 20 years old otherwise (i.e.: they have dependent children)
        ssa40_1_c_ii = persons("age", period.start) >= 20

        ssa40_1_c = ssa40_1_c_i + ssa40_1_c_ii

        # ssa40_2 allows for payment to continue if not caring for 28 days

        # ssa40_3 defines "institutional care"

        # ssa41 requires a certificate when applying for supported living payment as a carer

        # ssa42 specifies requirements for medical examination

        # ssa54_5_d person C is ineligible if receiving youth payment

        # ssa61_5_d person C is ineligible if receiving young parent payment

        return ssa40_1_a * ssa40_1_b * ssa40_1_c


class supported_living_payment__restricted_work_capacity(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Is incapable of regularly working 15 or more hours a week in open employment"
    reference = [
        "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783176",
        "http://legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM5468367",
        ]
    set_input = holders.set_input_dispatch_by_period


class supported_living_payment__granted(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person is currently granted the supported living benefit"
    definition_period = periods.WEEK
    reference = "Reference is unclear, but variable is utilised by the phrase: 'granted a main benefit'"


class supported_living_payment__receiving(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person is currently recieving/being paid the supported living payment"
    definition_period = periods.WEEK
    reference = "Reference is unclear, but concept underpinning the variable assumes it covers both: 'being paid a main benefit' or 'recieving a benefit'"


class supported_living_payment__caring_for_another_person(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Eligible for Supported Living Payment."
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783187"
    set_input = holders.set_input_dispatch_by_period


class supported_living_payment__disability_self_inflicted(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.ETERNITY
    label = "The person's restricted capacity for work, or total blindness, was self-inflicted and brought about by the person with a view to qualifying for a benefit"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783178", "s36"
