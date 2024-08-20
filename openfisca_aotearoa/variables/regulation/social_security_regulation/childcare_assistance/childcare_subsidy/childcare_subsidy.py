"""Formula for establishing eligibility for the childcare subsidy and the possibly hours payable for said subsidy."""

import numpy

# We import the required OpenFisca modules needed to define a formula.
#
# For more information on OpenFisca's available modules:
# https://openfisca.org/doc/openfisca-python-api/index.html
from openfisca_core import periods, variables

# We import the required `entities` corresponding to our formulas.
#
# Entities are an OpenFisca abstraction that allows us to model legislation's
# `subjects of law`: person, couple, family, household, and so on.
#
# For more information on OpenFisca's `entities`:
# https://openfisca.org/doc/key-concepts/person,_entities,_role.html
from openfisca_aotearoa import entities


class childcare_subsidy__eligible(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Eligibility of child for payment of childcare subsidy"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96309"  # 2018
        "https://ref.synco.pt/nz/ssa/230/en#P2-S12-s77"  # 2018 alt
        "https://ref.synco.pt/nz/ssar/171/en#P2-S6-s30"  # 2018 alt
        "https://www.workandincome.govt.nz/map/income-support/extra-help/childcare-assistance-programme/qualifications-01.html"  # MSD Interpretation
        "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/DLM282545.html",  # 2004
        ]

    def formula_2004_10_04(persons, period, parameters):
        immigration__citizen_or_resident = persons("immigration__citizen_or_resident", period.first_month)
        normally_in_nz = persons("social_security__ordinarily_resident_in_new_zealand", period)

        is_principal_carer = persons("social_security__principal_caregiver", period.first_month)

        under_5_years_28_days_not_attending_school = persons.family(
            "childcare_subsidy__family_has_resident_child_under_5_not_in_school", period)
        is_5_and_will_be_enrolled = persons.family(
            "childcare_subsidy__resident_child_aged_5_intend_enrol_in_school", period)
        under_6_with_disability_allowance = persons.family(
            "childcare_subsidy__family_with_disability_allowance_child_under_6", period)
        return immigration__citizen_or_resident * normally_in_nz * is_principal_carer * \
            (under_5_years_28_days_not_attending_school
                + is_5_and_will_be_enrolled + under_6_with_disability_allowance)

    def formula_2018_11_26(persons, period, parameters):
        principal_carer = persons("social_security__principal_caregiver", period.first_month)
        temporary_ob_or_ucb_caregiver = persons("social_security__temporary_ob_or_ucb_caregiver", period)
        parent = persons.has_role(entities.Family.PARENT)  # this creates a tenuous link between the surprising use of "parent" in the act and the use of the Role named parent in OpenFisca
        is_parent_carer_etc = temporary_ob_or_ucb_caregiver + principal_carer + parent

        general_limitation = persons("social_security__general_limitation", period)  # Regulation does not specify the residential requirement so general limitation is assumed...
        ssar30_1_a = persons.family("childcare_subsidy__family_has_resident_child_under_5_not_in_school", period)
        ssar30_1_b = persons.family("childcare_subsidy__resident_child_aged_5_intend_enrol_in_school", period)
        ssar30_1_c = persons.family("childcare_subsidy__family_with_disability_allowance_child_under_6", period)

        # ssar30_2  first term start date or mid-term start date dependant
        # ssar30_3  see section 5B of the Education Act 1989

        return general_limitation * is_parent_carer_etc * (ssar30_1_a + ssar30_1_b + ssar30_1_c)


class childcare_subsidy__granted(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    default_value = False
    label = "Are payments under the childcare subsidy granted for this child"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/14.0/whole.html#LMS96299"  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s21"  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282529"  # 2004
        ]


class childcare_subsidy__receiving(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Is the child recieving the childcare subsidy"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/14.0/whole.html#LMS96299"  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s21"  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282529"  # 2004
        ]


class childcare_subsidy__hours_payable(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Childcare subsidy payable"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96310",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s31",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282546"  # 2004
        ]

    def formula_2018_11_26(persons, period, parameters):
        ssar32 = persons("childcare_subsidy__caregiver_approved_activity", period) * persons("childcare_subsidy__caregiver_approved_activity_hours", period)
        ssar34 = persons("childcare_subsidy__caregiver_serious_disability", period) * persons("childcare_subsidy__caregiver_serious_disability_hours", period)
        ssar35 = persons("childcare_subsidy__caregiver_other_hours", period)

        ssar31 = ssar32 + ssar34 + ssar35
        return persons("childcare_subsidy__eligible", period) * ssar31


class childcare_subsidy__caregiver_approved_activity(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Payable hours for childcare subsidy with caregiver engaged in approved activity"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96310",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s32",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282546"  # 2004
        ]

    def formula_2018_11_26(persons, period, parameters):
        is_principal_carer = persons("social_security__principal_caregiver", period.first_month)
        # ssar32_p1_a  describes the logic in the last line of this formula
        ssar32_p1_b = persons.family.any(persons.family.members("child_disability_allowance__payable", period))
        ssar32_p1_c = persons("childcare_subsidy__other_child_in_hospital_or_disability_allowance", period)
        # ssar32_p1_d  is included in variable in line above
        ssar32_p2_a = persons("childcare_subsidy__no_other_caregiver", period)
        ssar32_p2_b = persons("childcare_subsidy__other_caregiver_appproved_activity", period)
        ssar32_p2 = ssar32_p2_a + ssar32_p2_b
        # ssar32_p2_c  could be added in future for clarity
        ssar32_p3 = persons("childcare_subsidy__engaged_in_approved_activity", period)
        # ssar32_p3_a  could be added in future for clarity
        # ssar32_p3_b  could be added in future for clarity
        ssar32_p4 = persons("childcare_subsidy__shift_work", period)
        # ssar32_p4_a  could be added in future for clarity
        # ssar32_p4_b  could be added in future for clarity
        ssar32 = (ssar32_p2 * (ssar32_p3 + ssar32_p4)) + ssar32_p1_b + ssar32_p1_c
        return is_principal_carer * ssar32


class childcare_subsidy__caregiver_approved_activity_hours(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Payable hours for childcare subsidy with caregiver engaged in approved activity"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96310",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s32",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282546"  # 2004
        ]

    def formula_2018_11_26(persons, period, parameters):
        hours_payable_approved_activity = parameters(period).social_security.childcare_assistance.childcare_subsidy.hours_payable_caregiver_approved_activity
        ssar32_hours = persons("childcare_subsidy__caregiver_approved_activity", period) * hours_payable_approved_activity

        return ssar32_hours


class childcare_subsidy__caregiver_serious_disability(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Childcare subsidy payable with caregiver with serious disability or illness"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96310",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s32",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282546"  # 2004
        ]

    def formula_2018_11_26(persons, period, parameters):
        minimum_hours_participating = parameters(period).social_security.childcare_assistance.childcare_subsidy.minimum_hours_in_childcare
        needs_childcare_minimum = parameters(period).social_security.childcare_assistance.childcare_subsidy.needs_childcare_minimum_with_serious_disability
        not_engaged_in_approved_activity = numpy.logical_not(persons("childcare_subsidy__caregiver_approved_activity", period))
        s34_l1_a = persons.family.any(persons.family.members("early_childcare_hours_participation_per_week", period) >= minimum_hours_participating)
        s34_l1_b_i = persons("childcare_subsidy__caregiver_serious_disability_illness", period)
        s34_l1_b_ii = persons("childcare_subsidy__caregiver_serious_disability_illness_hours_needed", period) >= needs_childcare_minimum
        s34_l1_b = s34_l1_b_i * s34_l1_b_ii

        s34_l1_c_i = persons("childcare_subsidy__no_other_caregiver", period)
        s34_l1_c_ii = persons("childcare_subsidy__other_caregiver_appproved_activity", period)
        # s34_l1_c_iii  wrapped up in line above
        s34_l1_c_iv = persons.family.any(persons.family.members("child_disability_allowance__payable", period))
        s34_l1_c = s34_l1_c_i + s34_l1_c_ii + s34_l1_c_iv

        ssar34 = not_engaged_in_approved_activity * s34_l1_a * s34_l1_b * s34_l1_c

        return persons("childcare_subsidy__eligible", period) * ssar34


class childcare_subsidy__caregiver_serious_disability_hours(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Payable hours for childcare subsidy with caregiver with serious disability or illness"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96310",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s32",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282546"  # 2004
        ]

    def formula_2018_11_26(persons, period, parameters):
        hours_payable_serious_disability = parameters(period).social_security.childcare_assistance.childcare_subsidy.hours_payable_caregiver_serious_disability
        ssar34_hours = persons("childcare_subsidy__caregiver_serious_disability", period) * hours_payable_serious_disability

        return ssar34_hours


class childcare_subsidy__caregiver_other_hours(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Payable hours for childcare subsidy with caregiver not engaged in approved activity and not with serious disability or illness"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96310",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s32",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282546"  # 2004
        ]

    def formula_2018_11_26(persons, period, parameters):
        minimum_hours_participating = parameters(period).social_security.childcare_assistance.childcare_subsidy.minimum_hours_in_childcare
        hours_payable_other = parameters(period).social_security.childcare_assistance.childcare_subsidy.hours_payable_caregiver_other
        s35_l1_a = persons.family.any(persons.family.members("early_childcare_hours_participation_per_week", period) >= minimum_hours_participating)
        s35_l1_b = numpy.logical_not(persons("childcare_subsidy__caregiver_approved_activity", period))
        s35_l1_c = numpy.logical_not(persons("childcare_subsidy__caregiver_serious_disability", period))
        s35 = s35_l1_a * s35_l1_b * s35_l1_c
        ssar35_hours = s35 * hours_payable_other

        return persons("childcare_subsidy__eligible", period) * ssar35_hours


class childcare_subsidy__caregiver_serious_disability_illness(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    default_value = False
    label = "Caregiver has serious disability or illness as per regulation definition"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96291",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s20-p1-d14",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282521"  # 2004
        ]


class childcare_subsidy__caregiver_serious_disability_illness_hours_needed(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.WEEK
    default_value = 0
    label = "Number of hours MSD is satisfied a caregiver with a serious disability or illness needs childcare"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96310",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s34",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282546"  # 2004
        ]


class childcare_subsidy__no_other_caregiver(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Child has not other caregiver"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/14.0/whole.html#LMS96313",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s34-l1-c-i",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282549"  # 2004
        ]


class childcare_subsidy__other_child_in_hospital_or_disability_allowance(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "The child’s principal caregiver, temporary OB or UCB caregiver has other child who is either in hospital or is a child for whom a child disability allowance is payable"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/14.0/whole.html#LMS96313",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s34-l1-c-i",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282549"  # 2004
        ]


class childcare_subsidy__other_caregiver_appproved_activity(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    default_value = False
    label = "Child has another caregiver engaged in an approved activity or MSD is satisfied... the other caregiver cannot care for the child"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/14.0/whole.html#LMS96313",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s34-l1-c-i",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282549"  # 2004
        ]


class childcare_subsidy__engaged_in_approved_activity(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    default_value = False
    label = "Caregiver is engaged in approved activity as per clause 32 subclause 3"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/14.0/whole.html#LMS96311",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s32-p3",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282547"  # 2004
        ]


class childcare_subsidy__shift_work(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    default_value = False
    label = "Caregiver is undertaking shift work as per clause 32 subclause 4"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/14.0/whole.html#LMS96311",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s32-p4",  # 2018 alt
        "https://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282547"  # 2004
        ]


class childcare_subsidy__family_has_resident_child_under_5_not_in_school(variables.Variable):
    value_type = bool
    entity = entities.Family
    definition_period = periods.WEEK
    label = "Family has a resident child who is under 5 years old, not in school and in minimum childcare hours per week"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96309",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s30-p1-a",  # 2018 alt
        "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282544"  # 2004
        ]

    def formula_2004_10_04(families, period, parameters):
        dependent_children = families.members(
            "social_security__dependent_child", period)
        not_in_school = numpy.logical_not(families.members(
            "attending_school", period))
        under_5 = families.members("age", period.start) < 5
        citizens_and_residents = families.members(
            "immigration__citizen_or_resident", period.first_month)
        oscar_subsidy_granted_for_child = numpy.logical_not(families.members("oscar_subsidy__granted", period))
        return families.any((dependent_children * citizens_and_residents * not_in_school * under_5 * oscar_subsidy_granted_for_child), role=entities.Family.CHILD)

    def formula_2018_11_26(families, period, parameters):
        criteria = families.members("childcare_subsidy__child_under_5_not_in_school", period)
        dependent_children = families.members("social_security__dependent_child", period)

        return families.any((dependent_children * criteria), role=entities.Family.CHILD)


class childcare_subsidy__resident_child_aged_5_intend_enrol_in_school(variables.Variable):
    value_type = bool
    entity = entities.Family
    definition_period = periods.WEEK
    label = "Family has resident child aged 5 who will be enrolled in school and in minimum childcare hours per week"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96309",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s30-p1-b",  # 2018 alt
        "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282544"  # 2004
        ]

    def formula_2004_10_04(families, period, parameters):
        dependent_children = families.members("social_security__dependent_child", period)
        children_to_be_enrolled = families.members("intends_to_enroll_in_school", period)
        aged_5 = families.members("age", period.start) == 5
        citizens_and_residents = families.members("immigration__citizen_or_resident", period.first_month)
        oscar_subsidy_granted_for_child = numpy.logical_not(families.members("oscar_subsidy__granted", period))
        return families.any((dependent_children * citizens_and_residents * children_to_be_enrolled * aged_5 * oscar_subsidy_granted_for_child), role=entities.Family.CHILD)

    def formula_2018_11_26(families, period, parameters):
        criteria = families.members("childcare_subsidy__child_aged_5_intend_enrol_in_school", period)
        dependent_children = families.members("social_security__dependent_child", period)

        return families.any(dependent_children * criteria, role=entities.Family.CHILD)


class childcare_subsidy__family_with_disability_allowance_child_under_6(variables.Variable):
    value_type = bool
    entity = entities.Family
    definition_period = periods.WEEK
    label = "Family has a child under 6 years old and eligible for Disability Allowance and in minimum childcare hours per week"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96308",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/#P2-S6-s30-p1-c",  # 2018 alt
        "https://www.workandincome.govt.nz/map/income-support/extra-help/childcare-assistance-programme/qualifications-01.html",
        "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282544"  # 2004
        ]

    def formula_2004_10_04(families, period, parameters):
        dependent_children = families.members(
            "social_security__dependent_child", period)
        eligible_children = families(
            "child_disability_allowance__family_has_eligible_child", period)
        under_6 = families.members("age", period.start) < 6
        citizens_and_residents = families.members(
            "immigration__citizen_or_resident", period.first_month)
        oscar_subsidy_granted_for_child = numpy.logical_not(families.members("oscar_subsidy__granted", period))
        return families.any((dependent_children * citizens_and_residents * eligible_children * under_6 * oscar_subsidy_granted_for_child), role=entities.Family.CHILD)

    def formula_2018_11_26(families, period, parameters):
        criteria = families.members("childcare_subsidy__child_meets_criteria_with_disability_allowance_under_6", period)
        dependent_children = families.members("social_security__dependent_child", period)

        return families.any(dependent_children * criteria, role=entities.Family.CHILD)


class childcare_subsidy__child_under_5_not_in_school(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Child who is under 5 years old, not in school and in minimum childcare hours per week"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96309",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s30-p1-a",  # 2018 alt
        "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282544"  # 2004
        ]

    def formula_2018_11_26(persons, period, parameters):
        minimum_hours_participating = parameters(period).social_security.childcare_assistance.childcare_subsidy.minimum_hours_in_childcare
        meeting_minimum_hours = persons("early_childcare_hours_participation_per_week", period) >= minimum_hours_participating
        not_in_school = numpy.logical_not(persons("attending_school", period))
        under_5 = persons("age", period.start) < 5
        oscar_subsidy_granted_for_child = numpy.logical_not(persons("oscar_subsidy__granted", period))
        return not_in_school * under_5 * meeting_minimum_hours * oscar_subsidy_granted_for_child


class childcare_subsidy__child_aged_5_intend_enrol_in_school(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Child aged 5 who will be enrolled in school and in minimum childcare hours per week"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96309",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/?#P2-S6-s30-p1-b",  # 2018 alt
        "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282544"  # 2004
        ]

    def formula_2018_11_26(persons, period, parameters):
        minimum_hours_participating = parameters(period).social_security.childcare_assistance.childcare_subsidy.minimum_hours_in_childcare
        meeting_minimum_hours = persons("early_childcare_hours_participation_per_week", period) >= minimum_hours_participating
        to_be_enrolled = persons("intends_to_enroll_in_school", period)
        aged_5 = persons("age", period.start) == 5
        oscar_subsidy_granted_for_child = numpy.logical_not(persons("oscar_subsidy__granted", period))
        return to_be_enrolled * aged_5 * meeting_minimum_hours * oscar_subsidy_granted_for_child


class childcare_subsidy__child_meets_criteria_with_disability_allowance_under_6(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Test to determine if a child meets the criteria for the caregiver to be eligible"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96308",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/#P2-S6-s30-p1-c",  # 2018 alt
        "https://www.workandincome.govt.nz/map/income-support/extra-help/childcare-assistance-programme/qualifications-01.html",
        "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282544"  # 2004
        ]

    def formula_2018_11_26(persons, period, parameters):
        minimum_hours_participating = parameters(period).social_security.childcare_assistance.childcare_subsidy.minimum_hours_in_childcare
        meeting_minimum_hours = persons("early_childcare_hours_participation_per_week", period) >= minimum_hours_participating

        disability_allowance = persons("child_disability_allowance__allowance_criteria", period)
        under_6 = persons("age", period.start) < 6
        oscar_subsidy_granted_for_child = numpy.logical_not(persons("oscar_subsidy__granted", period))

        return disability_allowance * under_6 * meeting_minimum_hours * oscar_subsidy_granted_for_child


class childcare_subsidy__child_meets_criteria(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Test to determine if a child meets the criteria for the caregiver to be eligible"
    reference = [
        "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/whole.html#LMS96308",  # 2018
        "https://ref.synco.pt/nz/ssar/171/en/#P2-S6-s30-p1-c",  # 2018 alt
        "https://www.workandincome.govt.nz/map/income-support/extra-help/childcare-assistance-programme/qualifications-01.html",
        "http://www.legislation.govt.nz/regulation/public/2004/0268/latest/whole.html#DLM282544"  # 2004
        ]

    def formula_2018_11_26(persons, period, parameters):
        return persons("childcare_subsidy__child_under_5_not_in_school", period) + persons("childcare_subsidy__child_aged_5_intend_enrol_in_school", period) + persons("childcare_subsidy__child_meets_criteria_with_disability_allowance_under_6", period)
