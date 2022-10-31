"""MSD Policy (retrieved August 2018 from https://www.workandincome.govt.nz/products/a-z-benefits/sole-parent-support.html).

You may get Sole Parent Support if you are:

    * aged 20 or older
    * a single parent or caregiver with one or more dependent children under 14
    * not in a relationship
    * without adequate financial support
    * a New Zealand citizen or permanent resident who has been here for at least two years
    at any one time since becoming a citizen or permanent resident, and who normally lives here.
"""
from numpy import where, logical_not

from openfisca_core import periods, variables

from openfisca_aotearoa import entities
from openfisca_core import holders


# TODO: Review against the new 2018 act,  also assess utilising the test for dependent child: https://www.workandincome.govt.nz/map/income-support/main-benefits/sole-parent-support/dependent-child-01.html
# social_security__dependent_child appears to describe the origins of the above workandincome definition of dependent child.
class sole_parent_support__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Eligible for Sole Parent Support"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783165", "https://www.workandincome.govt.nz/map/income-support/main-benefits/sole-parent-support/qualifications.html"

    def formula(persons, period, parameters):
        # The applicant
        resides_in_nz = persons("social_security__residential_requirement", period)
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


    def formula_2018_11_26(persons, period, parameters):
        ssa29_a = persons("sole_parent_support__requirement", period)

        ssa29_b = persons("sole_parent_support__split_care", period)

        ssa29_c = persons("social_security__residential_requirement", period)

        ssa29_d = persons("sole_parent_support__age_threshold", period)

        return ssa29_a * ssa29_b * ssa29_c * ssa29_d


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
    definition_period = periods.WEEK
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
    definition_period = periods.WEEK
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
    definition_period = periods.WEEK
    reference = "https://www.workandincome.govt.nz/products/a-z-benefits/sole-parent-support.html"
    set_input = holders.set_input_divide_by_period

    def formula(persons, period, parameters):
        # old enough?
        age_threshold = parameters(period).entitlements.social_security.sole_parent_support.age_threshold
        return persons("age", period.start) >= age_threshold


class sole_parent_support__years_in_nz_requirement(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Has lived continuously in New Zealand for 2 years or more at any one time since becoming a New Zealand citizen or permanent resident?"
    definition_period = periods.WEEK
    reference = "TODO"

    def formula(persons, period, parameters):
        # been in NZ log enough?
        min_years = parameters(period).entitlements.social_security.sole_parent_support.minumum_continuous_time_in_nz
        years_in_nz = persons("number_of_years_lived_in_nz", period.first_month)
        return years_in_nz >= min_years


class sole_parent_support__below_income_threshold(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Income is below Sole Parent Support threshold?"
    definition_period = periods.WEEK
    set_input = holders.set_input_divide_by_period


### New 2018 Act Updates https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783165
class sole_parent_support__requirement(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Meets the sole parent requirement?"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783167"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        # TODO: A person (P) meets the sole parent requirement if P is the mother or father of, and caring for, at least 1 dependent child aged under 14 years and
        # ssa30_person_is_parent = persons("person_is_parent", period.first_month)
        # ssa30_person_has_dependent_child = persons("social_security__dependent_children", period.first_month) > 0
        # #TODO: How do we get dependent child age? Does it matter is there are some children over the age
        # ssa30_dependent_child_under_14 = persons("sole_parent_support__dependent_child_requirement", period.first_week)
        # ssa30 = ssa30_person_is_parent * ssa30_person_has_dependent_child * ssa30_dependent_child_under_14

        ssa30_a = logical_not(persons("social_security__in_a_relationship", period))

        ssa30_b = persons("sole_parent_support__spouse_or_partner_died", period)

        ssa30_c = persons("sole_parent_support__marriage_or_civil_union_dissolved", period)

        ssa30_d = persons("sole_parent_support__living_apart_and_lost_support", period)

        ssa30_e = persons("sole_parent_support__lost_regular_support", period)

        return ssa30_a + ssa30_b + ssa30_c + ssa30_d + ssa30_e


class sole_parent_support__dependent_child_requirement(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Atleast one dependent child meets age requirement"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        # TODO: Create parameter for min age
        child_age_threshold = 14

        return persons.family.members("age", period.first_day) < child_age_threshold


class sole_parent_support__spouse_or_partner_died(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Spouse or partner died?"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period


class sole_parent_support__marriage_or_civil_union_dissolved(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Marriage or civil union has been dissolved"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period


class sole_parent_support__living_apart_and_lost_support(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Living apart from, and has lost the support of or is being inadequately maintained spouse or partner"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period


class sole_parent_support__lost_regular_support(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Lost regular support from spouse or partner"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        ssa30_e_i = persons('sole_parent_support__partner_imprisoned', period)
        ssa30_e_ii = persons('sole_parent_support__partner_supervision', period)

        return ssa30_e_i + ssa30_e_ii


class sole_parent_support__partner_imprisoned(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Partner sentenced to imprisonment and is serving the sentence in a prison"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period


class sole_parent_support__partner_supervision(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Partner sentenced to supervision, intensive supervision, or home detention"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period


class sole_parent_support__split_care(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Is sole parent situation in split care?"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS6632"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        ssa32 = persons('sole_parent_support__dependent_children', period)

        # This section applies to the parents of 2 or more dependent children
        ssa32_1_a = persons('sole_parent_support__parents_living_apart', period)
        ssa32_1_b = persons('sole_parent_support__each_parent_is_principal_caregiver', period)
        #  both parents would be entitled to sole parent support.
        ssa32_1 = where(ssa32 > 2,True, False) * ssa32_1_a * ssa32_1_b

        # Only 1 of the 2 parents is entitled to sole parent support, and the parent who is entitled to sole parent support must be
        ssa32_2_a = persons('sole_parent_support__TODO', period)
        ssa32_2_b = persons('sole_parent_support__TODO', period)
        ssa32_2_c = persons('sole_parent_support__TODO', period)
        ssa32_2 = ssa32_2_a + ssa32_2_b + ssa32_2_c

        # This section does not apply if each parent has become the principal caregiver in respect of at least 1 child under 1 or more orders
        ssa32_3_a = persons('sole_parent_support__TODO', period)
        ssa32_3_b = persons('sole_parent_support__TODO', period)
        ssa32_3 = ssa32_3_a * ssa32_3_b

        # In this section, child means a dependent child of the parents
        ssa32_4_a = persons('sole_parent_support__TODO', period)
        ssa32_4_b = persons('sole_parent_support__TODO', period)
        ssa32_4 = ssa32_4_a + ssa32_4_b



        return ssa32_1 + ssa32_2 + ssa32_3 + ssa32_4



class sole_parent_support__dependent_children(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Number of dependent children"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period


class sole_parent_support__parents_living_apart(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Parents are living apart"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period


class sole_parent_support__each_parent_is_principal_caregiver(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Each parent is the principal caregiver of 1 or more of the children"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period


class sole_parent_support__TODO(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "TODO"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period
