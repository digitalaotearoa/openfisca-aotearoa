"""This module provides amounts for Supported Living Payment."""
import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class schedule_4__part3_1_a(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(a)"

    def formula_2018_11_26(persons, period, parameters):
        single = numpy.logical_not(persons("social_security__in_a_relationship", period))
        under_18 = persons("age", period.first_day) < 18
        no_children = persons("social_security__dependent_children", period.first_week) == 0
        return single * under_18 * no_children


class schedule_4__part3_1_b(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(b)"

    def formula_2018_11_26(persons, period, parameters):
        single = numpy.logical_not(persons("social_security__in_a_relationship", period))
        no_children = persons("social_security__dependent_children", period.first_week) == 0
        not_1a = numpy.logical_not(persons("schedule_4__part3_1_a", period))
        return single * no_children * not_1a


class schedule_4__part3_1_c(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(c)"

    def formula_2018_11_26(persons, period, parameters):
        single = numpy.logical_not(persons("social_security__in_a_relationship", period))
        has_children = persons("social_security__dependent_children", period.first_week) > 0
        return single * has_children


class schedule_4__part3_1_d(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(d)"

    def formula_2018_11_26(people, period, parameters):
        in_relationship = people("social_security__in_a_relationship", period)
        partner_granted_main_benefit = people.family.any(
            people.family.members("social_security__granted_main_benefit", period),
            role=entities.Family.PARTNER)
        return in_relationship * partner_granted_main_benefit



class schedule_4__part3_1_d_i(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(d)(i)"

    def formula_2018_11_26(people, period, parameters):
        base = people("schedule_4__part3_1_d", period)
        no_children = people("social_security__dependent_children", period) < 1
        return base * no_children


class schedule_4__part3_1_d_ii(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(d)(ii)"

    def formula_2018_11_26(people, period, parameters):
        base = people("schedule_4__part3_1_d", period)
        has_children = people("social_security__dependent_children", period) < 1
        return base * has_children


class schedule_4__part3_1_e(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(e)"

    def formula_2018_11_26(people, period, parameters):
        in_relationship = people("social_security__in_a_relationship", period)
        partner_has_super = people.family.any(
            people.family.members("super__being_paid_nz_superannuation", period.first_month),
            role=entities.Family.PARTNER)
        return in_relationship * partner_has_super

    def formula_2020_11_09(people, period, parameters):
        in_relationship = people("social_security__in_a_relationship", period)
        partner_has_super = people.family.any(
            people.family.members("super__being_paid_nz_superannuation", period.first_month),
            role=entities.Family.PARTNER)
        partner_has_veterans_pension = people.family.any(
            people.family.members("veterans_support__being_paid_a_veterans_pension", period.first_month),
            role=entities.Family.PARTNER)
        return in_relationship * (partner_has_super + partner_has_veterans_pension)


class schedule_4__part3_1_e_i(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(e)(i)"

    def formula_2018_11_26(people, period, parameters):
        base = people("schedule_4__part3_1_e", period)
        no_children = people("social_security__dependent_children", period) < 1
        return base * no_children


class schedule_4__part3_1_e_ii(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(e)(ii)"

    def formula_2018_11_26(people, period, parameters):
        base = people("schedule_4__part3_1_e", period)
        has_children = people("social_security__dependent_children", period) > 0
        return base * has_children


# n.b.: this clause was repealed 2020-11-09 & folded into part3_1_e.
class schedule_4__part3_1_f(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(f)"
    end = "2020-11-09"

    def formula_2018_11_26(people, period, parameters):
        in_relationship = people("social_security__in_a_relationship", period)
        partner_has_veterans_pension = people.family.any(
            people.family.members("veterans_support__being_paid_a_veterans_pension", period.first_month),
            role=entities.Family.PARTNER)
        return in_relationship * partner_has_veterans_pension


class schedule_4__part3_1_f_i(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(f)(i)"
    end = "2020-11-09"

    def formula_2018_11_26(people, period, parameters):
        base = people("schedule_4__part3_1_f", period)
        no_children = people("social_security__dependent_children", period) < 1
        return base * no_children


class schedule_4__part3_1_f_ii(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(f)(ii)"
    end = "2020-11-09"

    def formula_2018_11_26(people, period, parameters):
        base = people("schedule_4__part3_1_f", period)
        has_children = people("social_security__dependent_children", period) > 0
        return base * has_children


class schedule_4__part3_1_g(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(g)"

    def formula_2018_11_26(people, period, parameters):
        disabled_or_blind = people("supported_living_payment__disabled_or_blind__entitled", period)
        in_relationship = people("social_security__in_a_relationship", period)
        partner_has_benefit = people.family.any(
            people.family.members("social_security__granted_main_benefit", period),
            role=entities.Family.PARTNER)
        partner_has_super = people.family.any(
            people.family.members("super__being_paid_nz_superannuation", period.first_month),
            role=entities.Family.PARTNER)
        return disabled_or_blind * in_relationship * numpy.logical_not(partner_has_benefit + partner_has_super)

    def formula_2020_11_09(people, period, parameters):
        disabled_or_blind__entitled = people("supported_living_payment__disabled_or_blind__entitled", period)
        in_relationship = people("social_security__in_a_relationship", period)
        partner_has_benefit = people.family.any(
            people.family.members("social_security__granted_main_benefit", period),
            role=entities.Family.PARTNER)
        partner_has_super = people.family.any(
            people.family.members("super__being_paid_nz_superannuation", period.first_month),
            role=entities.Family.PARTNER)
        partner_has_veterans_pension = people.family.any(
            people.family.members("veterans_support__being_paid_a_veterans_pension", period.first_month),
            role=entities.Family.PARTNER)
        return disabled_or_blind__entitled * in_relationship * numpy.logical_not(partner_has_benefit + partner_has_super + partner_has_veterans_pension)


class schedule_4__part3_1_g_i(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(g)(i)"

    def formula_2018_11_26(people, period, parameters):
        base = people("schedule_4__part3_1_g", period)
        no_children = people("social_security__dependent_children", period) < 1
        return base * no_children


class schedule_4__part3_1_g_ii(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(g)(ii)"

    def formula_2018_11_26(people, period, parameters):
        base = people("schedule_4__part3_1_g", period)
        has_children = people("social_security__dependent_children", period) > 0
        return base * has_children


class schedule_4__part3_1_h(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(h)"

    def formula_2018_11_26(people, period, parameters):
        carer__entitled = people("supported_living_payment__carer__entitled", period)
        in_relationship = people("social_security__in_a_relationship", period)
        partner_has_benefit = people.family.any(
            people.family.members("social_security__granted_main_benefit", period),
            role=entities.Family.PARTNER)
        partner_has_super = people.family.any(
            people.family.members("super__being_paid_nz_superannuation", period.first_month),
            role=entities.Family.PARTNER)
        return carer__entitled * in_relationship * numpy.logical_not(partner_has_benefit + partner_has_super)

    def formula_2020_11_09(people, period, parameters):
        carer__entitled = people("supported_living_payment__carer__entitled", period)
        in_relationship = people("social_security__in_a_relationship", period)
        partner_has_benefit = people.family.any(
            people.family.members("social_security__granted_main_benefit", period),
            role=entities.Family.PARTNER)
        partner_has_super = people.family.any(
            people.family.members("super__being_paid_nz_superannuation", period.first_month),
            role=entities.Family.PARTNER)
        partner_has_veterans_pension = people.family.any(
            people.family.members("veterans_support__being_paid_a_veterans_pension", period.first_month),
            role=entities.Family.PARTNER)
        return carer__entitled * in_relationship * numpy.logical_not(partner_has_benefit + partner_has_super + partner_has_veterans_pension)


class schedule_4__part3_1_h_i(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(h)(i)"

    def formula_2018_11_26(people, period, parameters):
        base = people("schedule_4__part3_1_g", period)
        no_children = people("social_security__dependent_children", period) < 1
        return base * no_children


class schedule_4__part3_1_h_ii(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/DLM6784861.html"
    label = "Part 3 Supported Living Payment - Clause 1(g)(ii)"

    def formula_2018_11_26(people, period, parameters):
        base = people("schedule_4__part3_1_h", period)
        has_children = people("social_security__dependent_children", period) > 0
        return base * has_children


class schedule_4__part3_5(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = """Shortcut to indicate beneficiary meets the following from clause 5:
        (a) has a psychiatric, intellectual, physical, or mental disability; and
        (b) is receiving long-term residential care in a hospital or rest home because of that disability; and
        (c) has not been means assessed under Part 6 of the Residential Care and Disability Support Services Act 2018.
    """
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784861"


class schedule_4__part3_6(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = """Shortcut to indicate beneficiary meets the following from clause 6:
        if that spouse or partner is not receiving long-term residential care in a hospital or rest home.
    """
    reference = "https://legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6784861"
