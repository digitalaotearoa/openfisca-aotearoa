"""TODO: Add missing doctring."""

from numpy import logical_not as not_

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_aotearoa.entities import Family, Person


class attending_school(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Is child attending school"
    reference = "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/DLM282545.html"


class will_be_enrolled_in_school(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Child will be enrolled in a school that has a cohort entry policy in place"
    # (ba) who is 5, whose parent, principal caregiver, or guardian intends to enrol
    # the child in a school that has a cohort entry policy in place, and who
    # (under section 5B(2) of the Education Act 1989) may not be enrolled in that
    # school until the term start date of the next term;"""
    reference = "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/DLM282545.html"


class social_security_regulation__eligible_for_childcare_subsidy(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Eligibility of child for payment of childcare subsidy"
    reference = "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/DLM282545.html"

    def formula(persons, period, parameters):
        immigration__citizen_or_resident = persons("immigration__citizen_or_resident", period)
        normally_in_nz = persons("social_security__ordinarily_resident_in_new_zealand", period)
        income_below_threshold = persons.family("social_security_regulation__household_income_below_childcare_subsidy_threshold", period)

        is_principal_carer = persons.has_role(Family.PRINCIPAL_CAREGIVER)

        under_5_years_28_days_not_attending_school = persons.family(
            "social_security_regulation__family_has_resident_child_under_5_not_in_school", period)
        is_5_and_will_be_enrolled = persons.family(
            "social_security_regulation__family_has_resident_child_aged_5_who_will_be_enrolled_in_school", period)
        under_6_with_disability_allowance = persons.family(
            "social_security_regulation__family_has_child_eligible_for_disability_allowance_child_under_6", period)
        return immigration__citizen_or_resident * normally_in_nz * is_principal_carer * income_below_threshold * \
            (under_5_years_28_days_not_attending_school
                + is_5_and_will_be_enrolled + under_6_with_disability_allowance)


class early_childcare_hours_participation_per_week(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Number of hours per week person is participating in approved early-childhood education programmes"
    reference = "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282547"


class social_security_regulation__family_has_resident_child_under_5_not_in_school(Variable):
    value_type = bool
    entity = Family
    definition_period = MONTH
    label = "Family has a resident child who is under 5 years old, not in school and in minimum childcare hours per week"
    reference = "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282544"

    def formula(families, period, parameters):
        minimum_hours_participating = parameters(period).entitlements.social_security.childcare_subsidy.minimum_hours_in_childcare

        dependent_children = families.members(
            "social_security__dependent_child", period)
        not_in_school = not_(families.members(
            "attending_school", period))
        under_5 = families.members("age", period.start) < 5
        citizens_and_residents = families.members(
            "immigration__citizen_or_resident", period)
        meets_early_childcare_hours_threshold = families.members("early_childcare_hours_participation_per_week", period) >= minimum_hours_participating
        return families.any((dependent_children * citizens_and_residents * not_in_school * under_5 * meets_early_childcare_hours_threshold), role=Family.CHILD)


class social_security_regulation__family_has_resident_child_aged_5_who_will_be_enrolled_in_school(Variable):
    value_type = bool
    entity = Family
    definition_period = MONTH
    label = "Family has resident child aged 5 who will be enrolled in school and in minimum childcare hours per week"
    reference = "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282544"

    def formula(families, period, parameters):
        minimum_hours_participating = parameters(period).entitlements.social_security.childcare_subsidy.minimum_hours_in_childcare

        dependent_children = families.members(
            "social_security__dependent_child", period)
        children_to_be_enrolled = families.members(
            "will_be_enrolled_in_school", period)
        aged_5 = (families.members("age", period.start) == 5)
        citizens_and_residents = families.members(
            "immigration__citizen_or_resident", period)
        meets_early_childcare_hours_threshold = families.members("early_childcare_hours_participation_per_week", period) >= minimum_hours_participating
        return families.any((dependent_children * citizens_and_residents * children_to_be_enrolled * aged_5 * meets_early_childcare_hours_threshold), role=Family.CHILD)


class social_security_regulation__family_has_child_eligible_for_disability_allowance_child_under_6(Variable):
    value_type = bool
    entity = Family
    definition_period = MONTH
    label = "Family has a child under 6 years old and eligible for Disability Allowance and in minimum childcare hours per week"
    reference = "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282544"

    def formula(families, period, parameters):
        minimum_hours_participating = parameters(period).entitlements.social_security.childcare_subsidy.minimum_hours_in_childcare

        dependent_children = families.members(
            "social_security__dependent_child", period)
        eligible_children = families(
            "child_disability_allowance__family_has_eligible_child", period)
        under_6 = families.members("age", period.start) < 6
        citizens_and_residents = families.members(
            "immigration__citizen_or_resident", period)
        meets_early_childcare_hours_threshold = families.members("early_childcare_hours_participation_per_week", period) >= minimum_hours_participating
        return families.any((dependent_children * citizens_and_residents * eligible_children * under_6 * meets_early_childcare_hours_threshold), role=Family.CHILD)


class social_security_regulation__household_income_below_childcare_subsidy_threshold(Variable):
    value_type = bool
    default_value = True
    entity = Family
    label = "Household income is below Childcare Subsidy threshold"
    definition_period = MONTH
