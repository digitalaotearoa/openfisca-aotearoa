"""MSD Policy (retrieved August 2018 from https://www.workandincome.govt.nz/products/a-z-benefits/sole-parent-support.html).

You may get Sole Parent Support if you are:

    * aged 20 or older
    * a single parent or caregiver with one or more dependent children under 14
    * not in a relationship
    * without adequate financial support
    * a New Zealand citizen or permanent resident who has been here for at least two years
    at any one time since becoming a citizen or permanent resident, and who normally lives here.
"""

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


# TODO: Review against the new 2018 act,  also assess utilising the test for dependent child: https://www.workandincome.govt.nz/map/income-support/main-benefits/sole-parent-support/dependent-child-01.html
# social_security__dependent_child appears to describe the origins of the above workandincome definition of dependent child.
class sole_parent_support__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.DateUnit.MONTH
    label = "Eligible for Sole Parent Support"
    reference = "https://www.workandincome.govt.nz/map/income-support/main-benefits/sole-parent-support/qualifications.html"

    def formula(persons, period, parameters):
        # The applicant
        resides_in_nz = persons("social_security__residential_requirement", period.first_week)
        resident_or_citizen = persons("immigration__citizen_or_resident", period)

        years_in_nz = persons("sole_parent_support__years_in_nz_requirement", period)
        age_requirement = persons("sole_parent_support__age_threshold", period)
        child_age_requirement = persons.family("sole_parent_support__family_has_child_under_age_limit", period)

        relationship_test = persons("sole_parent_support__meets_relationship_qualification", period)
        # TODO isInadequatelySupportedByPartner
        # TODO isMaintainingChild

        # income low enough?
        low_income = persons("sole_parent_support__below_income_threshold", period)

        return resides_in_nz * resident_or_citizen * years_in_nz *\
            age_requirement * child_age_requirement * \
            relationship_test * low_income


class sole_parent_support__granted(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person is currently granted the Sole Parent Support benefit"
    definition_period = periods.DateUnit.WEEK
    reference = "Reference is unclear, but variable is utilised by the phrase: 'granted a main benefit'"


class sole_parent_support__receiving(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person is currently recieving/being paid sole parent support"
    definition_period = periods.DateUnit.WEEK
    reference = "Reference is unclear, but concept underpinning the variable assumes it covers both: 'being paid a main benefit' or 'recieving a benefit'"


class sole_parent_support__base(variables.Variable):
    value_type = float
    default_value = 0
    entity = entities.Person
    label = "TODO"
    definition_period = periods.DateUnit.WEEK
    reference = "TODO"


class sole_parent_support__meets_relationship_qualification(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Meets the sole parent support test for not being in a relationship"
    definition_period = periods.DateUnit.MONTH
    reference = "https://www.workandincome.govt.nz/map/income-support/main-benefits/sole-parent-support/qualifications.html"

    """
     be one of the following:
        * living apart from their partner and lost the support or being inadequately
            maintained by the spouse or partner
        * divorced or had their civil union dissolved
        * single (never had a partner)
        * has lost the regular support of their partner as their partner has been imprisoned or
            is subject to release or detention conditions that prevent employment or
        * their spouse or partner has died
    """
    def formula(persons, period, parameters):
        # Do they have a partner
        no_partners = (persons("social_security__in_a_relationship", period.first_week) == 0)
        not_supported = (persons("is_adequately_supported_by_partner", period) == 0)
        # no partner, OR not supported by partner
        return no_partners + not_supported


class sole_parent_support__family_has_child_under_age_limit(variables.Variable):
    value_type = bool
    entity = entities.Family
    definition_period = periods.DateUnit.MONTH
    label = "Does the family have a child who meets the criteria for disabled"

    def formula(families, period, parameters):
        youngest_child_age_threshold = parameters(period).entitlements.social_security.sole_parent_support.youngest_child_age_threshold
        youngest_ages = families("age_of_youngest", period.start)
        return youngest_ages < youngest_child_age_threshold


class sole_parent_support__age_threshold(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Meets the age test for sole parent support?"
    definition_period = periods.DateUnit.MONTH
    reference = "https://www.workandincome.govt.nz/products/a-z-benefits/sole-parent-support.html"

    def formula(persons, period, parameters):
        # old enough?
        age_threshold = parameters(period).entitlements.social_security.sole_parent_support.age_threshold
        return persons("age", period.start) >= age_threshold


class sole_parent_support__years_in_nz_requirement(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Has lived continuously in New Zealand for 2 years or more at any one time since becoming a New Zealand citizen or permanent resident?"
    definition_period = periods.DateUnit.MONTH
    reference = "TODO"

    def formula(persons, period, parameters):
        # been in NZ log enough?
        min_years = parameters(period).entitlements.social_security.sole_parent_support.minumum_continuous_time_in_nz
        years_in_nz = persons("number_of_years_lived_in_nz", period)
        return years_in_nz >= min_years


class sole_parent_support__below_income_threshold(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Income is below Sole Parent Support threshold?"
    definition_period = periods.DateUnit.MONTH
