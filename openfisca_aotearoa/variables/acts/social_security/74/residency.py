"""TODO: Add missing doctring."""

from openfisca_core.holders import set_input_dispatch_by_period
from openfisca_core.periods import ETERNITY, MONTH
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Person


class social_security__meets_residential_requirements_for_certain_benefits(Variable):
    value_type = bool
    entity = Person
    label = "Residential requirements for certain benefits"
    definition_period = MONTH
    reference = "http://www.legislation.govt.nz/act/public/1964/0136/latest/DLM363796.html"

    # Note this is the date the 1964 act commenced, but jobseeker came later
    def formula_1964_12_04(persons, period, parameters):
        # (a) is a New Zealand citizen, or is a person who holds a residence
        # class visa under the Immigration Act 2009
        is_citizen_or_resident = persons("is_citizen_or_resident", period)

        # (b) is ordinarily resident in New Zealand when he or she first
        # applies for the benefit; and
        ordinarily_lives_in_nz = persons(
            "social_security__is_ordinarily_resident_in_new_zealand", period)

        # (c) except in the case of a person who is recognised as a refugee or
        #     a protected person in New Zealand under
        #     the Immigration Act 2009, has resided continuously in New Zealand
        #     for a period of at least 2 years at any one time,
        is_refugee_or_protected = \
            persons("immigration__is_recognised_refugee", period) \
            + persons("immigration__is_protected_person", period)

        enough_years_in_nz = persons(
            "social_security__has_resided_continuously_in_nz_for_a_period_of_at_least_2_years_at_any_one_time",
            period)

        return (is_citizen_or_resident * ordinarily_lives_in_nz) \
            + (is_refugee_or_protected * enough_years_in_nz)

    # https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138
    # 16 Residential requirement
    # (1) This section sets out the residential requirement that must be met by applicants for certain types of assistance under this Part.
    # (2) A person (P) meets the residential requirement if—
    #     (a) P is a New Zealand citizen or holds a residence class visa under the Immigration Act 2009, and is ordinarily resident in New Zealand when P
    #  first applies for the benefit, and—
    #         (i) has resided continuously in New Zealand for a period of at least 2 years at any one time after becoming a citizen or resident; or
    #         (ii) is recognised as a refugee or a protected person in New Zealand under the Immigration Act 2009; or
    #    (b) P is ordinarily resident in a country with which New Zealand has a reciprocity agreement, and P has resided continuously in New Zealand for a period of at least 2 years before applying for the benefit or before a decision on P’s claim for the benefit is made.
    # (3) For the purposes of subsection (2)(b), New Zealand has a reciprocity agreement with another country if there is in force under
    #  section 380 an order declaring that the provisions contained in an agreement
    #  (for example, a convention) signed by New Zealand and the Government of that country set out in a schedule of the order have force
    #   and effect so far as they relate to New Zealand."
    #

    #  (c) except in the case of a person who is recognised as a refugee or
    #      a protected person in New Zealand under
    #      the Immigration Act 2009, has resided continuously in New Zealand
    #      for a period of at least 2 years at any one time,
    def formula_2018_11_26(persons, period, parameters):

        has_eligible_residency_class = persons("is_citizen_or_resident", period) + \
            persons("immigration__is_recognised_refugee", period) + \
            persons("immigration__is_protected_person", period)

        nz_eligible = persons("social_security__is_ordinarily_resident_in_new_zealand", period) * persons("social_security__has_resided_continuously_in_nz_for_a_period_of_at_least_2_years_at_any_one_time", period)
        reciprocal_eligible = persons("social_security__is_ordinarily_resident_in_country_with_reciprocity_agreement", period) * (persons("years_resided_continuously_in_new_zealand", period) > 2)

        return has_eligible_residency_class * (nz_eligible + reciprocal_eligible)


# TODO: Review against the new 2018 act
class social_security__is_ordinarily_resident_in_new_zealand(Variable):
    value_type = bool
    entity = Person
    label = "is ordinarily resident in New Zealand"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = "http://www.legislation.govt.nz/act/public/1964/0136/latest/DLM363772.html"


# TODO: Review against the new 2018 act
class social_security__has_resided_continuously_in_nz_for_a_period_of_at_least_2_years_at_any_one_time(Variable):
    value_type = bool
    entity = Person
    label = "has resided continuously in New Zealand for a period of at least 2 years at any one time"
    definition_period = ETERNITY


class social_security__is_ordinarily_resident_in_country_with_reciprocity_agreement(Variable):
    value_type = bool
    entity = Person
    label = "is ordinarily resident in a country with which New Zealand has a reciprocity agreement"
    definition_period = ETERNITY


class years_resided_continuously_in_new_zealand(Variable):
    value_type = int
    entity = Person
    label = "has resided continuously in New Zealand for a period of at least 2 years before applying for the benefit or before a decision on P’s claim for the benefit is made"
    definition_period = MONTH
