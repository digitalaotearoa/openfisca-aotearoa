"""TODO: Add missing doctring."""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


# TODO: Review against the new 2018 act
class child_disability_allowance__eligible(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
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


class child_disability_allowance__family_has_eligible_child(variables.Variable):
    value_type = bool
    entity = entities.Family
    definition_period = periods.DateUnit.MONTH
    label = "Does the family have a child who meets the criteria for disabled"
    reference = "http://legislation.govt.nz/bill/government/2017/0004/15.0/DLM7512349.html"

    def formula(families, period, parameters):
        has_disability = families.members("child_disability_allowance__allowance_criteria", period)
        child_age_threshold = parameters(period).entitlements.social_security.child_disability_allowance.child_age_threshold
        children = families.members("age", period.start) <= child_age_threshold
        disabled_children = has_disability * children
        return families.any(disabled_children, role = entities.Family.CHILD)


# TODO: Review against the new 2018 act
class child_disability_allowance__allowance_criteria(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Has serious disability"
    definition_period = periods.DateUnit.MONTH

    def formula(persons, period, parameters):
        med_cert_required_months = parameters(period).entitlements.social_security.child_disability_allowance.medical_certification_required_months

        return persons("social_security__child_with_serious_disability", period) * \
            persons("social_security__requires_constant_care_and_attention", period) * \
            (persons("social_security__medical_certification_months", period) >= med_cert_required_months)


# TODO: Review against the new 2018 act
class social_security__medical_certification_months(variables.Variable):
    value_type = int
    entity = entities.Person
    label = "Number of future months the disability is expected to last for, in months"
    definition_period = periods.DateUnit.MONTH


# TODO: Review against the new 2018 act
class social_security__requires_constant_care_and_attention(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Requires constant care and attention"
    definition_period = periods.DateUnit.MONTH
