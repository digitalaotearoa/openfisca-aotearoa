"""This module provides eligibility and amount for Jobseeker Support."""

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from openfisca_core import periods, variables
from openfisca_core import holders

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
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138", "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796"
    set_input = holders.set_input_dispatch_by_period

    # Note this is the date the 1964 act commenced, but jobseeker came later
    # This encompassing variable was called social_security__meets_residential_requirements_for_certain_benefits but was renamed to better suit the 2018 Social Security Act
    # Ref: https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796
    def formula_1964_12_04(persons, period, parameters):

        ssa64_74aa_1_a = persons("immigration__citizen_or_resident", period.first_month)

        ssa64_74aa_1_b = persons("social_security__ordinarily_resident_in_new_zealand", period.first_month)

        ssa64_74aa_1_c = persons("immigration__recognised_refugee", period.first_month) \
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

        ssa16_2_a_ii = persons("immigration__recognised_refugee", period.first_month) + \
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
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784616", "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM360407", "https://www.openlaw.nz/case/2014NZCA611"


class social_security__resided_continuously_nz_2_years_citizen_or_resident(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "has resided continuously in New Zealand for a period of at least 2 years after becoming a citizen, 16 2(a)i"
    definition_period = periods.ETERNITY
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138", "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796"


class social_security__ordinarily_resident_in_country_with_reciprocity_agreement(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "is ordinarily resident in a country with which New Zealand has a reciprocity agreement"
    definition_period = periods.ETERNITY
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783138", "https://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM363796"
