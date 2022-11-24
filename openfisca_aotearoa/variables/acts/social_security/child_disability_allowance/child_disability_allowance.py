"""This module provides eligibility for Child Disability Allowance."""
# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html

from openfisca_core import periods, variables

from openfisca_aotearoa import entities

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html

# We define the `child_disability_allowance` variable.
#
# Please note that by itself a `variable` is not a rule but just a
# specification of such a rule.
#
# A `variable` can contain several rules, otherwise called `formulas`, that is,
# several ways it can be calculated, depending on ther date at which we want to
# calculate it. Said otherwise, as a `concept`, any modelled benefit like
# `jobseeker_support` exist since big bang until big crunch, yet the way of
#  calculating it depends on the applicable law at the requested `period`.
#
# For more information on OpenFisca's `variables`:
# https://openfisca.org/doc/key-concepts/variables.html


class child_disability_allowance__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Eligible for Child Disability Allowance"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783266.html"
    default_value = False

    def formula_2018_11_26(persons, period, parameters):
        # ssa2018_78_1_a --> covered in ssa2018_79
        ssa2018_78_1_b_i = (persons("child_disability_allowance__residing_in_principal_home", period)
            + persons("child_disability_allowance__residing_in_temp_orphan_benefit_caregiver", period)
            + persons("child_disability_allowance__residing_with_unsupported_child_benefit_caregiver", period)) * persons.has_role(entities.Family.CHILD)
        ssa2018_78_2_a = persons("child_disability_allowance__residing_in_approved_voluntary_organisation", period) * persons.has_role(entities.Family.CHILD)
        # ssa2018_78_2_b --> Accommodation required to be contributed by parents) can be covered as a general note.
        ssa2018_79 = persons.family("child_disability_allowance__eligible_child", period)
        ssa2018_83 = persons("social_security__beneficiary_except_benefit_exempt_for_childcare_disability_allowance", period) * persons.has_role(entities.Family.CHILD)

        return ssa2018_78_1_b_i * ssa2018_78_2_a * ssa2018_79 * ssa2018_83


class child_disability_allowance__benefit(variables.Variable):
    value_type = float
    default_value = -9999
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Child disability allowance amount that a person is eligible for"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784880.html"

    def formula_2018_11_26(persons, period, parameters):

        return persons("child_disability_allowance__entitled", period) * parameters(period).social_security.child_disability_allowance.weekly_benefit


class childcare_disability_allowance__child_with_serious_disability(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Child has serious disability"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783270.html"

    def formula_2018_11_26(persons, period, parameters):
        med_cert_required_months = parameters(period).entitlements.social_security.child_disability_allowance.medical_certification_required_months
        # ssa2018_79_1_a can be covered by a note describing disability
        ssa2018_79_1_b = persons("social_security__requires_constant_care", period)
        ssa2018_79_1_c = (persons("social_security__medical_certificate_months", period) >= med_cert_required_months)
        return ssa2018_79_1_b * ssa2018_79_1_c


class child_disability_allowance__residing_in_principal_home(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Is the child being cared for at the home of their principal caregiver?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783267.html"


class child_disability_allowance__residing_in_temp_orphan_benefit_caregiver(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Is the child being cared for at the home of the temporary Orphan's benefit caregiver?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783267.html"


class child_disability_allowance__residing_with_unsupported_child_benefit_caregiver(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Is the child being cared for at the home of the child benefit caregiver?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783267.html"


class child_disability_allowance__residing_in_approved_voluntary_organisation(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Is the child being cared for in an approved weekly accommodation operated by a voluntary organisation?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783267.html"


class child_disability_allowance__eligible_child(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Family
    definition_period = periods.WEEK
    label = "Does the family have a child who meets the criteria for disabled"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783267.html"

    def formula(families, period, parameters):
        child_age_threshold = parameters(period).entitlements.social_security.child_disability_allowance.child_age_threshold
        children = families.members("age", period.start) <= child_age_threshold
        disabled = families.members("childcare_disability_allowance__child_with_serious_disability", period)
        disabled_children = disabled * children
        return families.any(disabled_children, role=entities.Family.CHILD)


class social_security__beneficiary_except_benefit_exempt_for_childcare_disability_allowance(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Is the person granted any benefit under the Act (except Orphan's benefit, unsupported child's benefit, \
    disability allowance, any Veteran's pension or allowance (Except children's pension) or any \
    weekly accident compensation?"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783276.html"


class social_security__medical_certificate_months(variables.Variable):
    value_type = int
    default_value = -9999
    entity = entities.Person
    label = "Number of future months the disability is expected to last for, in months"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783270.html"


class social_security__requires_constant_care(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Requires constant care and attention"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6783270.html"


# Variables used in 1964 Act calculations are below:
# Month based variable for 1964 Act
class child_disability_allowance__eligible(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.MONTH
    label = "Eligible for Child Disability Allowance"
    reference = "http://www.legislation.govt.nz/act/public/1964/0136/latest/DLM361659.html"

    def formula(persons, period, parameters):
        # The applicant
        resident_or_citizen = persons("immigration__citizen_or_resident", period)
        is_principal_carer = persons("income_tax__principal_caregiver", period)
        has_eligible_disabled_child = persons.family("child_disability_allowance__family_has_eligible_child", period)

        # http://www.legislation.govt.nz/act/public/1964/0136/latest/DLM363772.html
        # Notwithstanding anything to the contrary in this Act or Part 6 of the Veterans’
        # Support Act 2014 or the New Zealand Superannuation and Retirement Income Act 2001,
        # the chief executive may, in the chief executive’s discretion, refuse to grant any
        # benefit or may terminate or reduce any benefit already granted or may grant a
        # benefit at a reduced rate in any case where the chief executive is satisfied—
        # (a) that the applicant, or the spouse or partner of the applicant or any person
        # in respect of whom the benefit or any part of the benefit is or would be payable,
        # is not ordinarily resident in New Zealand;

        resides_in_nz = persons(
            "social_security__ordinarily_resident_in_new_zealand", period)

        return resident_or_citizen * \
            resides_in_nz * \
            is_principal_carer * \
            has_eligible_disabled_child


# Month based variable for 1964 Act
class child_disability_allowance__family_has_eligible_child(variables.Variable):
    value_type = bool
    entity = entities.Family
    definition_period = periods.MONTH
    label = "Does the family have a child who meets the criteria for disabled"
    reference = "http://legislation.govt.nz/bill/government/2017/0004/15.0/DLM7512349.html"

    def formula(families, period, parameters):
        has_disability = families.members("child_disability_allowance__allowance_criteria", period)
        child_age_threshold = parameters(period).entitlements.social_security.child_disability_allowance.child_age_threshold
        children = families.members("age", period.start) <= child_age_threshold
        disabled_children = has_disability * children
        return families.any(disabled_children, role=entities.Family.CHILD)


# Month based variable for 1964 Act
class child_disability_allowance__allowance_criteria(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Has serious disability"
    definition_period = periods.MONTH

    def formula(persons, period, parameters):
        med_cert_required_months = parameters(period).entitlements.social_security.child_disability_allowance.medical_certification_required_months

        return persons("social_security__child_with_serious_disability", period) * \
            persons("social_security__requires_constant_care_and_attention", period) * \
            (persons("social_security__medical_certification_months", period) >= med_cert_required_months)


# Month based variable for 1964 Act
class social_security__medical_certification_months(variables.Variable):
    value_type = int
    entity = entities.Person
    label = "Number of future months the disability is expected to last for, in months"
    definition_period = periods.MONTH


# Month based variable for 1964 Act
class social_security__requires_constant_care_and_attention(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Requires constant care and attention"
    definition_period = periods.MONTH
