"""This module provides eligibility and amount for Jobseeker Support."""

import numpy

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from openfisca_core import holders, periods, variables

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities


class social_security__residential_requirement(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Residential requirements for certain benefits, calculates for the 1964 and the 2018 Social Security Acts"
    definition_period = periods.WEEK
    reference = [
        "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138",
        "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796"
    ]
    set_input = holders.set_input_dispatch_by_period

    # Note this is the date the 1964 act commenced, but jobseeker came later
    # This encompassing variable was called social_security__meets_residential_requirements_for_certain_benefits but was renamed to better suit the 2018 Social Security Act
    # Ref: https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796
    def formula_1964_12_04(persons, period, parameters):

        ssa64_74aa_1_a = persons("immigration__citizen_or_resident", period.first_month)

        ssa64_74aa_1_b = persons("social_security__ordinarily_resident_in_new_zealand", period.first_month)

        ssa64_74aa_1_c = persons("immigration__recognised_refugee", period.first_day) \
            + persons("immigration__protected_person", period.first_month) \
            + persons("social_security__resided_continuously_nz_2_years_citizen_or_resident", period)

        # ssa64_74aa_1_c_i  - this implied in variable: social_security__resided_continuously_nz_2_years_citizen_or_resident
        # ssa64_74aa_1_c_ii  - this implied in calculation

        ssa64_74aa_1A_a_and_b = persons("social_security__ordinarily_resident_in_country_with_reciprocity_agreement", periods.ETERNITY)

        # ssa64_74aa_2 - this calculation performed by only calling this function in relation to the benefits listed

        return ((ssa64_74aa_1_a * ssa64_74aa_1_b) + ssa64_74aa_1A_a_and_b) * ssa64_74aa_1_c

    # Note this is the date the 2018 act commenced
    def formula_2018_11_26(persons, period, parameters):

        # ssa16_1 - Descriptive, not requiring coding.

        ssa16_2_a = persons("immigration__citizen_or_resident", period.first_month) * \
            persons("social_security__ordinarily_resident_in_new_zealand", period.first_month)

        ssa16_2_a_i = persons("social_security__resided_continuously_nz_2_years_citizen_or_resident", periods.ETERNITY)

        ssa16_2_a_ii = persons("immigration__recognised_refugee", period.first_day) + \
            persons("immigration__protected_person", period.first_month)

        ssa16_2_b = persons("social_security__ordinarily_resident_in_country_with_reciprocity_agreement", period) * (persons("years_resided_continuously_in_new_zealand", period.first_month) >= 2)

        # ssa16_3 - TODO Useful would be a list of countrys this applies to... we could make country an input.
        # ssa16_4 - MSD can refuse or cancel benefit if person not ordinarily in NZ...
        # ssa16_5 - The Governer-General may by Order in Council make regulations for the purposes of section 16 that specify circumstances in which:...
        #           Note the content of the list in this section is identical to the list in 421_1_c

        return (ssa16_2_a * (ssa16_2_a_i + ssa16_2_a_ii)) + ssa16_2_b


class social_security__ordinarily_resident_in_new_zealand(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "is ordinarily resident in New Zealand"
    definition_period = periods.ETERNITY
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784616", "ssa/221/en#sd2-d134", "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM360407", "https://www.openlaw.nz/case/2014NZCA611"


class social_security__resided_continuously_nz_2_years_citizen_or_resident(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "has resided continuously in New Zealand for a period of at least 2 years after becoming a citizen, 16 2(a)i"
    definition_period = periods.ETERNITY
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138", "ssa/221/en#s16-p2-a-i", "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796"


class social_security__ordinarily_resident_in_country_with_reciprocity_agreement(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "is ordinarily resident in a country with which New Zealand has a reciprocity agreement"
    definition_period = periods.ETERNITY
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138", "ssa/221/en#s16-p2-b", "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796"


class social_security__general_limitation(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "persons unlawfully resident or temporary entry class visa generally not eligible"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783143", "ssa/221/en#s19"
    set_input = holders.set_input_dispatch_by_period

    # Note this is the date the 2018 act commenced
    def formula_2018_11_26(persons, period, parameters):

        ssa19_1_a = persons("social_security__unlawfully_resident_or_present", period)
        ssa19_1_b = persons("immigration__temporary_entry_class_visa", period.first_day)
        ssa19_2 = persons("immigration__recognised_refugee", period.first_day)

        return numpy.logical_not(ssa19_1_a + ssa19_1_b) + ssa19_2


class social_security__unlawfully_resident_or_present(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Unlawfully resident or present in New Zealand, this is a term not mentioned in the Immigration Act specifically"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138", "ssa/221/en#s19-p1-a", "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796"


class social_security__compelled_to_remain(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DAY
    label = "compelled to remain in New Zealand because of unforeseen circumstances, this is a term only found in the social security act and social security regulations, not the immigration act."
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783542", "ssa/221/en#s205-p1-c"


class social_security__refugee_or_protected_person(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Refugee or protected person status, Section 205, only to be utilised with emergency benefit and temporary additional support"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783542", "ssa/221/en#s205-p1"
    set_input = holders.set_input_dispatch_by_period

    # Note this is the date the 2018 act commenced
    def formula_2018_11_26(persons, period, parameters):

        ssa205_1_a = persons("social_security__awaiting_refugee", period.first_day) + persons("social_security__awaiting_protected_person", period.first_day)
        ssa205_1_b = persons("immigration__recognised_refugee", period.first_day) + persons("immigration__protected_person", period.first_month)
        ssa205_1_c = persons("social_security__compelled_to_remain", period)

        # ssa205_2_a refers to where this section is relevant
        # ssa205_2_b refers to where this section is relevant

        # ssa205_3 indications which section this section overrides

        return ssa205_1_a + ssa205_1_b + ssa205_1_c


class social_security__awaiting_refugee(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DAY
    label = " is awaiting the outcome of the person’s claim for recognition as a refugee"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783542", "ssa/221/en#s205-p1-a"


class social_security__awaiting_protected_person(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DAY
    label = " is awaiting the outcome of the person’s claim for recognition as a protected person"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783542", "ssa/221/en#s205-p1-a"
