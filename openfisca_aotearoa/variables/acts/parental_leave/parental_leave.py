"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class parental_leave__primary_carer(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Is primary carer, as per Parental Leave and Employment Protection Act 1987"
    reference = "http://www.legislation.govt.nz/act/public/1987/0129/latest/DLM120458.html"

    def formula_2002(persons, period, parameters):
        biological_mother = persons("parental_leave__biological_mother", period)

        her_spouse = persons("parental_leave__spouse_or_partner_of_biological_mother", period)
        received_transferred_entitlement = persons("parental_leave__spouse_who_transferred_her_entitlement", period)

        other = persons("parental_leave__a_person_other_than_biological_mother_or_her_spouse", period)
        permanent = persons("parental_leave__taking_permanent_primary_responsibility_for_child", period)

        # Mark who is the principal caregiver, as there may be >1 eligible
        # PPL Section 7 (2)
        nominated = persons("income_tax__principal_caregiver", period)

        return nominated * (biological_mother + (her_spouse * received_transferred_entitlement) + (other * permanent))


class parental_leave__biological_mother(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.ETERNITY
    label = "a female (the biological mother) who is pregnant or has given birth to a child"
    reference = "http://www.legislation.govt.nz/act/public/1987/0129/latest/DLM120458.html"


class parental_leave__spouse_or_partner_of_biological_mother(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "the spouse or partner of the biological mother"
    reference = "http://www.legislation.govt.nz/act/public/1987/0129/latest/DLM120458.html"

    def formula_2002(persons, period, parameters):
        # true for people who are not the biological mother, but the biological mother is in their family with role of partner
        return persons.family("parental_leave__family_includes_biological_mother_as_partner", period) * \
            numpy.logical_not(persons("parental_leave__biological_mother", period))


class parental_leave__family_includes_biological_mother_as_partner(variables.Variable):
    value_type = bool
    entity = entities.Family
    definition_period = periods.DateUnit.MONTH
    reference = "http://www.legislation.govt.nz/act/public/1987/0129/latest/DLM120458.html"

    def formula(families, period, parameters):
        biological_mothers = families.members("parental_leave__biological_mother", period)
        return families.any(biological_mothers, role = entities.Family.PARTNER)


class parental_leave__transferred_her_entitlement_to_spouse(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "has transferred all or part of her entitlement to a parental leave payment to that spouse or partner"
    reference = "http://www.legislation.govt.nz/act/public/1987/0129/latest/DLM120458.html"


class parental_leave__spouse_who_transferred_her_entitlement(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "is the spouse of the biological mother, and she transferred her entitlement to this spouse"
    reference = "http://www.legislation.govt.nz/act/public/1987/0129/latest/DLM120458.html"

    def formula_2002(persons, period, parameters):
        is_spouse = persons("parental_leave__spouse_or_partner_of_biological_mother", period)
        family_has_transferring_entitlement = persons.family.members("parental_leave__transferred_her_entitlement_to_spouse", period)

        return persons.family.any(family_has_transferring_entitlement) * is_spouse


class parental_leave__a_person_other_than_biological_mother_or_her_spouse(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "a person, other than the biological mother or her spouse or partner"
    reference = "http://www.legislation.govt.nz/act/public/1987/0129/latest/DLM120458.html"

    def formula_2002(persons, period, parameters):
        biological_mother = persons.family.members("parental_leave__biological_mother", period)
        partner_is_biological_mother = persons.family.any(biological_mother, role = entities.Family.PARTNER)

        return numpy.logical_not(biological_mother) * numpy.logical_not(partner_is_biological_mother)


class parental_leave__taking_permanent_primary_responsibility_for_child(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "taking permanent primary responsibility for the care, development, and upbringing of a child who is under the age of 6 years (and if there is more than 1 such person, the person nominated in accordance with subsection (2))."
    reference = "http://www.legislation.govt.nz/act/public/1987/0129/latest/DLM120458.html"


class parental_leave__applied_for_leave_or_stopped_working(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Has applied for/taken leave or stopped working immediately"
    reference = "http://www.legislation.govt.nz/act/public/1987/0129/latest/DLM121773.html"


class parental_leave__threshold_tests(variables.Variable):
    value_type = int
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "satisfies Parental Leave Threshold Tests (tests are used to determine an employee's entitlements to parental leave)"
    reference = "http://www.legislation.govt.nz/act/public/1987/0129/latest/DLM6810651.html"


class parental_leave__had_previous_parental_leave_in_last_six_months(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Had previous parental leave in last six months"
    reference = "http://www.legislation.govt.nz/act/public/1987/0129/latest/DLM120450.html"


# TODO - Confirm that citizenship is a valid eligibility test here, the referenced act doesn't mention it
class parental_leave__eligible_employee(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Eligible employee"
    reference = "http://www.legislation.govt.nz/act/public/1987/0129/latest/DLM121539.html"

    def formula(persons, period, parameters):
        is_citizen = persons("citizenship__citizen", period)

        return is_citizen * persons("parental_leave__primary_carer", period) * \
            persons("parental_leave__applied_for_leave_or_stopped_working", period) * \
            (persons("parental_leave__threshold_tests", period) >= 6) * \
            numpy.logical_not(persons("parental_leave__had_previous_parental_leave_in_last_six_months", period))
