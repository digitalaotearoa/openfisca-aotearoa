"""This module refers to Social Security Act's "Residential requirement"."""

import datetime

import numpy

from openfisca_core import holders
from openfisca_core.periods import DateUnit
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class residential_requirement(Variable):
    value_type = bool
    entity = Person
    definition_period = DateUnit.DAY
    reference = "https://www.legislation.govt.nz/act/public/1964/0136/latest/DLM363796.html"
    label = "Residential requirement"
    documentation = """
        16 Residential requirement

        (1) This section sets out the residential requirement that must be met
            by applicants for certain types of assistance under this Part.

        (2) A person (P) meets the residential requirement if—
            (a) P is a New Zealand citizen or holds a residence class visa
                under the Immigration Act 2009, and is ordinarily resident in
                New Zealand when P first applies for the benefit, and—
                (i)  has resided continuously in New Zealand for a period of at
                     least 2 years at any one time after becoming a citizen or
                     resident; or
                (ii) is recognised as a refugee or a protected person in New
                     Zealand under the Immigration Act 2009; or
            (b) P is ordinarily resident in a country with which New Zealand
                has a reciprocity agreement, and P has resided continuously in
                New Zealand for a period of at least 2 years before applying
                for the benefit or before a decision on P’s claim for the
                benefit is made.

        (3) For the purposes of subsection (2)(b), New Zealand has a
            reciprocity agreement with another country if there is in force
            under section 380 an order declaring that the provisions contained
            in an agreement (for example, a convention) signed by New Zealand
            and the Government of that country set out in a schedule of the
            order have force and effect so far as they relate to New Zealand.

        (4) This section does not limit section 204 (MSD may refuse or cancel
            benefit if person not ordinarily resident in New Zealand), and is
            subject to section 205 (refugee or protected person status).

        (5) This section is also subject to any regulations made under section
            421 that specify circumstances in which a person—
            (a) is taken to meet the residential requirement; or
            (b) must be treated, for the purposes of satisfying the residential
                requirement, as being resident and present in New Zealand; or
            (c) must not be required to comply with the residential
                requirement.

    """

    def formula_2018_11_26(persons, period, parameters):
        citizen = persons("citizen", period)
        residence_visa = persons("residence_visa", period)
        ordinarily_resident = persons("ordinarily_resident", period)
        first_application = persons("first_application", period)
        continuously_resided_at_any_one_time = persons(
            "continuously_resided_at_any_one_time",
            period,
            )
        refugee = persons("refugee", period)
        protected = persons("protected", period)
        reciprocity_resident = persons("reciprocity_resident", period)
        continuously_resided_before_application = persons(
            "continuously_resided_before_application",
            period,
            )

        return (
            + (citizen + residence_visa)
            * (
                + ordinarily_resident * first_application
                + numpy.logical_not(first_application)
                )
            * (
                + continuously_resided_at_any_one_time
                + refugee
                + protected
                )
            + (
                + reciprocity_resident
                * continuously_resided_before_application
                )
            )

        # has_eligible_residency_class = persons("is_citizen_or_resident", period) + \
        #     persons("immigration__is_recognised_refugee", period) + \
        #     persons("immigration__is_protected_person", period)

        # nz_eligible = persons("social_security__is_ordinarily_resident_in_new_zealand", period) * persons("social_security__has_resided_continuously_in_nz_for_a_period_of_at_least_2_years_at_any_one_time", period)
        # reciprocal_eligible = persons("social_security__is_ordinarily_resident_in_country_with_reciprocity_agreement", period) * (persons("years_resided_continuously_in_new_zealand", period) > 2)

        # return has_eligible_residency_class * (nz_eligible + reciprocal_eligible)

    # https://www.legislation.govt.nz/act/public/1964/0136/latest/DLM363796.html
    #
    # 74AA Residential requirements for certain benefits
    #
    # (1)  A person who applies for a benefit of a kind stated in subsection
    #      (2) after 27 May 2007 is not eligible for it unless he or she—
    #      (a) is a New Zealand citizen, or is a person who holds a residence
    #      class visa under the Immigration Act 2009; and
    #      (b) is ordinarily resident in New Zealand when he or she first
    #          applies for the benefit; and
    #      (c) except in the case of a person who is recognised as a refugee or
    #          a protected person in New Zealand under the Immigration Act
    #          2009, has resided continuously in New Zealand for a period of
    #          at least 2 years at any one time,—
    #          (i)  if subsection (1A) applies to the person,—
    #               (A) before he or she applies for the benefit; or
    #               (B) before a decision on his or her claim for the benefit
    #                   is made under section 12; and
    #          (ii) in any other case, after the day on which paragraph (a)
    #               first applied to him or her.
    #
    # (1A) Subsection (1)(a) and (b) do not apply to a person at a time when—
    #      (a) there is in force under section 19(1) of the Social Welfare
    #          (Reciprocity Agreements, and New Zealand Artificial Limb
    #          Service) Act 1990 an order declaring that the provisions
    #          contained in an agreement or convention with the government of
    #          another country set out in a schedule to the order have force
    #          and effect so far as they relate to New Zealand; and
    #      (b) he or she is ordinarily resident in that country.
    #
    # (2)  The benefits referred to in subsection (1) are a youth payment, a
    #      young parent payment, a supported living payment, jobseeker support,
    #      and sole parent support.
    #
    def formula_2007_05_27(persons, period, parameters):
        is_citizen_or_resident = persons("is_citizen_or_resident", period)
        ordinarily_lives_in_nz = persons(
            "social_security__is_ordinarily_resident_in_new_zealand", period)

        is_refugee_or_protected = \
            persons("immigration__is_recognised_refugee", period) \
            + persons("immigration__is_protected_person", period)

        enough_years_in_nz = persons(
            "social_security__has_resided_continuously_in_nz_for_a_period_of_at_least_2_years_at_any_one_time",
            period)

        return (is_citizen_or_resident * ordinarily_lives_in_nz) \
            + (is_refugee_or_protected * enough_years_in_nz)


class citizen(Variable):
    label = "New Zealand citizen"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783138.html"
    documentation = """
        (a) P is a New Zealand citizen or holds a residence class visa
            under the Immigration Act 2009, and is ordinarily resident in
            New Zealand when P first applies for the benefit
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.DAY
    set_input = holders.set_input_dispatch_by_period


class residence_visa(Variable):
    label = "Holds a residence class visa"
    reference = "https://www.legislation.govt.nz/act/public/2009/0051/latest/DLM1440685.html"
    documentation = """
        (a) P is a New Zealand citizen or holds a residence class visa
            under the Immigration Act 2009, and is ordinarily resident in
            New Zealand when P first applies for the benefit
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.DAY
    set_input = holders.set_input_dispatch_by_period


class first_application(Variable):
    label = "First application for the benefit"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783138.html"
    documentation = """
        (a) P is a New Zealand citizen or holds a residence class visa
            under the Immigration Act 2009, and is ordinarily resident in
            New Zealand when P first applies for the benefit
    """
    entity = Person
    value_type = bool
    default_value = True
    definition_period = DateUnit.DAY


class continuously_resided_at_any_one_time(Variable):
    label = "Continuously resided in New Zealand at any one time"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783138.html"
    documentation = """
        (i)  has resided continuously in New Zealand for a period of at
             least 2 years at any one time after becoming a citizen or
             resident;
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.DAY


class refugee(Variable):
    label = "Refugee"
    reference = "https://www.legislation.govt.nz/act/public/2009/0051/latest/DLM1440774.html"
    documentation = """
        (ii) is recognised as a refugee or a protected person in New
             Zealand under the Immigration Act 2009;
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.DAY


class protected(Variable):
    label = "Protected person"
    reference = "https://www.legislation.govt.nz/act/public/2009/0051/latest/DLM1440774.html"
    documentation = """
        (ii) is recognised as a refugee or a protected person in New
             Zealand under the Immigration Act 2009;
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.DAY


class reciprocity_resident(Variable):
    label = "Ordinarily resident in country with reciprocity agreement"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783138.html"
    documentation = """
        (b) P is ordinarily resident in a country with which New Zealand
            has a reciprocity agreement, and P has resided continuously in
            New Zealand for a period of at least 2 years before applying
            for the benefit or before a decision on P’s claim for the
            benefit is made.
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.DAY


class continuously_resided_before_application(Variable):
    label = "Continuously resided in New Zealand before application"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783138.html"
    documentation = """
        (b) P is ordinarily resident in a country with which New Zealand
            has a reciprocity agreement, and P has resided continuously in
            New Zealand for a period of at least 2 years before applying
            for the benefit or before a decision on P’s claim for the
            benefit is made.
    """
    entity = Person
    value_type = bool
    default_value = False
    definition_period = DateUnit.DAY


class application(Variable):
    label = "Date of application for the benefit"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783138.html"
    documentation = """
        (b) P is ordinarily resident in a country with which New Zealand
            has a reciprocity agreement, and P has resided continuously in
            New Zealand for a period of at least 2 years before applying
            for the benefit or before a decision on P’s claim for the
            benefit is made.
    """
    entity = Person
    value_type = datetime.date
    definition_period = DateUnit.ETERNITY

    def formula_2018_11_26(persons, period, parameters):
        return period

    # (i)  if subsection (1A) applies to the person,—
    #      (A) before he or she applies for the benefit; or
    #      (B) before a decision on his or her claim for the benefit
    #          is made under section 12; and
    def formula_2007_05_27(persons, period, parameters):
        return period


class claim_decesion(Variable):
    label = "Date of decision on claim for the benefit"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783138.html"
    documentation = """
        (b) P is ordinarily resident in a country with which New Zealand
            has a reciprocity agreement, and P has resided continuously in
            New Zealand for a period of at least 2 years before applying
            for the benefit or before a decision on P’s claim for the
            benefit is made.
    """
    entity = Person
    value_type = datetime.date
    definition_period = DateUnit.ETERNITY

    def formula_2018_11_26(persons, period, parameters):
        return period

    # (i)  if subsection (1A) applies to the person,—
    #      (A) before he or she applies for the benefit; or
    #      (B) before a decision on his or her claim for the benefit
    #          is made under section 12; and
    def formula_2007_05_27(persons, period, parameters):
        return period
