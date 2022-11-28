"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


# TODO: Review against the new 2018 act
class orphans_benefit__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Eligible for Orphan's benefit"
    reference = """http://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM361606
        Orphans' benefits
        A person who is a principal caregiver in respect of a dependent child shall be entitled to receive an orphan's benefit in respect of that child if
        (a) each of the child's natural or adoptive parents is dead, or cannot be found, or suffers a serious long-term disablement which renders him or her unable to care for the child and
        (b) the applicant is likely to be the principal caregiver in respect of the child for at least 1 year from the date of application for the benefit; and
        (c) the applicant is aged 18 years or over; and
        (d) either
        (i) the child is both resident and present in New Zealand or
        (ii) the applicant has been both resident and present in New Zealand for a continuous period of 12 months at any time.
    """

    def formula(persons, period, parameters):
        resident_or_citizen = persons("immigration__citizen_or_resident", period)
        normally_in_nz = persons("social_security__ordinarily_resident_in_new_zealand", period)

        age_test = persons("age", period.start) >= 18

        not_the_parent = numpy.logical_not(
            persons("social_security__parent_of_dependent_child", period))
        one_year = persons(
            "social_security__principal_carer_for_one_year_from_application_date", period)

        is_principal_carer = persons("income_tax__principal_caregiver", period)

        has_orphaned_child_in_family = persons.family(
            "social_security__orphaned_child_in_family", period)

        return resident_or_citizen * normally_in_nz * age_test * not_the_parent * one_year * is_principal_carer * has_orphaned_child_in_family


# TODO: Review against the new 2018 act
class social_security__orphaned_child_in_family(variables.Variable):
    value_type = bool
    entity = entities.Family
    definition_period = periods.DateUnit.MONTH
    reference = "http://www.legislation.govt.nz/act/public/1964/0136/latest/whole.html#DLM361606"
    label = "Family is caring for an orphan as per Social Security Act 1964"

    def formula(families, period, parameters):
        children = families.members(
            "social_security__child", period.first_week)
        orphaned = families.members("social_security__orphaned", period)
        resident_or_citizen = families.members(
            "immigration__citizen_or_resident", period)

        return families.any((children * orphaned * resident_or_citizen), role = entities.Family.CHILD)


# TODO: Review against the new 2018 act, missing reference
class social_security__orphaned(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "each of the child's natural or adoptive parents is dead, or cannot be found, or suffers a serious long-term disablement which renders him or her unable to care for the child"
