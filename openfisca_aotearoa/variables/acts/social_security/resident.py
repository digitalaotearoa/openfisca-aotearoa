"""This module provides eligibility and amount for Jobseeker Support."""

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from openfisca_core import periods, variables
from openfisca_core.holders import set_input_dispatch_by_period

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities


# TODO this was added but is it the same as the one below
class social_security__residential_requirement(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DAY
    label = "Calculates if a the person meets the Residential Requirement of the Social Security Act 2018"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138"


class social_security__meets_residential_requirements_for_certain_benefits(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Residential requirements for certain benefits"
    definition_period = periods.MONTH
    reference = "http://www.legislation.govt.nz/act/public/1964/0136/latest/DLM363796.html"

    # Note this is the date the 1964 act commenced, but jobseeker came later
    def formula_1964_12_04(persons, period, parameters):
        # (a) is a New Zealand citizen, or is a person who holds a residence
        # class visa under the Immigration Act 2009
        citizen_or_resident = persons("immigration__citizen_or_resident", period)

        # (b) is ordinarily resident in New Zealand when he or she first
        # applies for the benefit; and
        ordinarily_lives_in_nz = persons(
            "social_security__ordinarily_resident_in_new_zealand", period)

        # (c) except in the case of a person who is recognised as a refugee or
        #     a protected person in New Zealand under
        #     the Immigration Act 2009, has resided continuously in New Zealand
        #     for a period of at least 2 years at any one time,
        is_refugee_or_protected = \
            persons("immigration__recognised_refugee", period) \
            + persons("immigration__protected_person", period)

        enough_years_in_nz = persons(
            "social_security__resided_continuously_in_nz_for_at_least_2_years_at_any_one_time",
            period)

        return (citizen_or_resident * ordinarily_lives_in_nz) \
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

        has_eligible_residency_class = persons("immigration__citizen_or_resident", period) + \
            persons("immigration__recognised_refugee", period) + \
            persons("immigration__protected_person", period)

        nz_eligible = persons("social_security__ordinarily_resident_in_new_zealand", period) * persons("social_security__resided_continuously_in_nz_for_at_least_2_years_at_any_one_time", period)
        reciprocal_eligible = persons("social_security__ordinarily_resident_in_country_with_reciprocity_agreement", period) * (persons("years_resided_continuously_in_new_zealand", period) >= 2)

        return has_eligible_residency_class * (nz_eligible + reciprocal_eligible)


# TODO: Review against the new 2018 act
class social_security__ordinarily_resident_in_new_zealand(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "is ordinarily resident in New Zealand"
    definition_period = periods.MONTH
    set_input = set_input_dispatch_by_period
    reference = "http://www.legislation.govt.nz/act/public/1964/0136/latest/DLM363772.html"


# TODO: Review against the new 2018 act
class social_security__resided_continuously_in_nz_for_at_least_2_years_at_any_one_time(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "has resided continuously in New Zealand for a period of at least 2 years at any one time"
    definition_period = periods.ETERNITY


class social_security__ordinarily_resident_in_country_with_reciprocity_agreement(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "is ordinarily resident in a country with which New Zealand has a reciprocity agreement"
    definition_period = periods.ETERNITY


# TODO: move to demographics
class years_resided_continuously_in_new_zealand(variables.Variable):
    value_type = int
    entity = entities.Person
    label = "has resided continuously in New Zealand for a period of at least 2 years before applying for the benefit or before a decision on P’s claim for the benefit is made"
    definition_period = periods.MONTH
