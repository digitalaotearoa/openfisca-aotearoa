"""MSD Policy (retrieved August 2018 from https://www.workandincome.govt.nz/products/a-z-benefits/sole-parent-support.html).

You may get Sole Parent Support if you are:

    * aged 20 or older
    * a single parent or caregiver with one or more dependent children under 14
    * not in a relationship
    * without adequate financial support
    * a New Zealand citizen or permanent resident who has been here for at least two years
        at any one time since becoming a citizen or permanent resident, and who normally lives here.

"""

from numpy import logical_not

from openfisca_core import holders, periods, variables

from openfisca_aotearoa import entities


# TODO: Review against the new 2018 act,  also assess utilising the test for dependent child: https://www.workandincome.govt.nz/map/income-support/main-benefits/sole-parent-support/dependent-child-01.html
# social_security__dependent_child appears to describe the origins of the above workandincome definition of dependent child.
class sole_parent_support__entitled(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Entitled for Sole Parent Support"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783165", "https://www.workandincome.govt.nz/map/income-support/main-benefits/sole-parent-support/qualifications.html"

    def formula_2018_11_26(persons, period, parameters):
        ssa29_a = persons("sole_parent_support__requirement", period)

        ssa29_b = persons("sole_parent_support__split_care", period)

        ssa29_c = persons("social_security__residential_requirement", period)

        ssa29_d = persons("sole_parent_support__age_threshold", period)

        return ssa29_a * ssa29_b * ssa29_c * ssa29_d


class sole_parent_support__entitled_without_split_care_requirement(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Eligible for Sole Parent Support minus the split care requirement (needed to calculate the split care requirement"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS6632"

    def formula_2018_11_26(persons, period, parameters):
        ssa29_a = persons("sole_parent_support__requirement", period)

        # ssa29_b = persons("sole_parent_support__split_care", period) purposfully excluded see 32 (1)(c)

        ssa29_c = persons("social_security__residential_requirement", period)

        ssa29_d = persons("sole_parent_support__age_threshold", period)

        return ssa29_a * ssa29_c * ssa29_d


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
        no_partners = (persons("person_has_partner", period.first_week) == 0)
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
        return persons("age", period.first_day) >= age_threshold


class sole_parent_support__below_income_threshold(variables.Variable):
    value_type = bool
    default_value = True
    entity = entities.Person
    label = "Income is below Sole Parent Support threshold?"
    definition_period = periods.WEEK
    set_input = holders.set_input_divide_by_period


class sole_parent_support__requirement(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Meets the sole parent requirement?"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783167"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):

        ssa30_dependent_child_under_14 = persons("sole_parent_support__dependent_child_requirement", period, "add")
        # ssa30 = ssa30_person_is_parent * ssa30_person_has_dependent_child * ssa30_dependent_child_under_14

        ssa30_a = logical_not(persons("social_security__in_a_relationship", period))

        ssa30_b = persons("sole_parent_support__spouse_or_partner_died", period)

        ssa30_c = persons("sole_parent_support__marriage_or_civil_union_dissolved", period)

        ssa30_d = persons("sole_parent_support__living_apart_and_lost_support", period)

        ssa30_e = persons("sole_parent_support__lost_regular_support", period)

        return ssa30_dependent_child_under_14 * (ssa30_a + ssa30_b + ssa30_c + ssa30_d + ssa30_e)


class sole_parent_support__dependent_child_requirement(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "At least one dependent child meets age requirement"
    definition_period = periods.WEEKDAY
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783167"

    def formula_2018_11_26(persons, period, parameters):
        child_age_threshold = parameters(period).social_security.sole_parent_support.child_age_threshold

        ssa30 = persons.family.members("social_security__dependent_child", period.first_week) * \
            persons.family.members("age", period.first_day) < child_age_threshold

        principal = persons("social_security__principal_caregiver", period.first_month)
        children = persons.family.any(ssa30, role=entities.Family.CHILD)
        parent = persons.has_role(entities.Family.PARENT)

        return children * (principal + parent)


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
    default_value = False
    entity = entities.Person
    label = "Lost regular support from spouse or partner"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        ssa30_e_i = persons("sole_parent_support__partner_imprisoned", period)
        ssa30_e_ii = persons("sole_parent_support__partner_supervision", period)

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
        ssa32_y = persons("social_security__dependent_children", period) >= 2
        ssa32_z = (persons.has_role(entities.Family.PARENT) + persons.has_role(entities.Family.PRINCIPAL))
        ssa32 = ssa32_y * ssa32_z

        # This section applies to the parents of 2 or more dependent children
        ssa32_1_a = persons("sole_parent_support__parents_living_apart", period)
        ssa32_1_b = persons("social_security__principal_caregiver", period.first_month) * \
            persons.family.sum(persons.family.members("social_security__principal_caregiver", period.first_month), role=entities.Family.PARENT)
        ssa32_1_c = persons("sole_parent_support__entitled_without_split_care_requirement", period) * persons.family.sum(persons.family.members("sole_parent_support__entitled_without_split_care_requirement", period), role=entities.Family.PARENT)
        ssa32_1 = ssa32 * ssa32_1_a * ssa32_1_b * ssa32_1_c

        # Only 1 of the 2 parents is entitled to sole parent support, and the parent who is entitled to sole parent support must be
        ssa32_2_a = persons("sole_parent_support__receiving", period)
        ssa32_2_b = logical_not(persons("sole_parent_support__receiving", period)) * \
            logical_not(persons.family.sum(persons.family.members("sole_parent_support__receiving", period), role=entities.Family.PARENT)) * \
            persons("sole_parent_support__principal_caregiver_before_apart", period)
        ssa32_2_c = persons("sole_parent_support__principal_caregiver_of_youngest", period)
        ssa32_2 = ssa32 * (ssa32_2_a + ssa32_2_b + ssa32_2_c)

        # This section does not apply if each parent has become the principal caregiver in respect of at least 1 child under 1 or more orders
        # So we return true
        ssa32_3 = (persons.has_role(entities.Family.PRINCIPAL) + persons.has_role(entities.Family.PARENT)) * \
            (
                persons("sole_parent_support__both_primary_caregiver_by_order", period)
                + persons.family.sum(persons.family.members("sole_parent_support__both_primary_caregiver_by_order", period), role=entities.Family.PRINCIPAL)
                + persons.family.sum(persons.family.members("sole_parent_support__both_primary_caregiver_by_order", period), role=entities.Family.PARENT)
            )
        # ssa32_3 = ssa32_3_a * ssa32_3_b

        # In this section, child means a dependent child of the parents
        # ssa32_4_a = persons('sole_parent_support__TODO', period)
        # ssa32_4_b = persons('sole_parent_support__TODO', period)
        # ssa32_4 = ssa32_4_a + ssa32_4_b

        return (logical_not(ssa32_y) * ssa32_z) + ssa32_1 + ssa32_2 + ssa32_3


class sole_parent_support__parents_living_apart(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Parents are living apart"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS6632"


class sole_parent_support__principal_caregiver_before_apart(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "The parent who MSD considers was the principal caregiver in respect of the children immediately before the parents began living apart"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS6632"


class sole_parent_support__principal_caregiver_of_youngest(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "The parent who is the principal caregiver in respect of the youngest child"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS6632"


class sole_parent_support__both_primary_caregiver_by_order(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Both parents are primary care givers by order of a court of competent jurisdiction bout the role of providing day-to-day care"
    definition_period = periods.WEEK
    set_input = holders.set_input_dispatch_by_period
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#LMS6632"
