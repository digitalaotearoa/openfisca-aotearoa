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


class social_security__residential_requirements(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Residential requirements for certain benefits"
    definition_period = periods.MONTH
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138", "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796"

    # Note this is the date the 1964 act commenced, but jobseeker came later
    # This encompassing variable was called social_security__meets_residential_requirements_for_certain_benefits but was renamed to better suit the 2018 Social Security Act
    # Ref: https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796
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

    # Note this is the date the 2018 act commenced
    def formula_2018_11_26(persons, period, parameters):

        # ssa16_1 -

        ssa16_2_a = persons("immigration__citizen_or_resident", period) * \
            persons("social_security__ordinarily_resident_in_new_zealand", period)

        ssa16_2_a_i = persons("social_security__resided_continuously_in_nz_at_least_2_years_after_becoming_citizen_or_resident", periods.ETERNITY)

        ssa16_2_a_ii = persons("immigration__recognised_refugee", period) + \
            persons("immigration__protected_person", period)

        ssa16_2_b = persons("social_security__ordinarily_resident_in_country_with_reciprocity_agreement", period) * (persons("years_resided_continuously_in_new_zealand", period) >= 2)

        # ssa16_3 - Useful would be a list of countrys this applies to...
        # ssa16_4 - MSD can refuse or cancel benefit if person not ordinarily in NZ...
        # ssa16_5 - Note the content of the list in this section is identical to the list in 421_1_c

        return (ssa16_2_a * (ssa16_2_a_i + ssa16_2_a_ii)) + ssa16_2_b


class social_security__ordinarily_resident_in_new_zealand(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "is ordinarily resident in New Zealand"
    definition_period = periods.MONTH
    set_input = set_input_dispatch_by_period
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138"


class social_security__resided_continuously_in_nz_at_least_2_years_after_becoming_citizen_or_resident(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "has resided continuously in New Zealand for a period of at least 2 years after becoming a citizen, 16 2(a)i"
    definition_period = periods.ETERNITY
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138"


class social_security__resided_continuously_in_nz_for_at_least_2_years_at_any_one_time(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "has resided continuously in New Zealand for a period of at least 2 years at any one time, 74AA 1(c)"
    definition_period = periods.ETERNITY
    reference = "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796"


class social_security__ordinarily_resident_in_country_with_reciprocity_agreement(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "is ordinarily resident in a country with which New Zealand has a reciprocity agreement"
    definition_period = periods.ETERNITY
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138"
