"""TODO: Add missing doctring."""

import numpy

from openfisca_core import holders, periods, variables

from openfisca_aotearoa import entities


class child_disability_allowance__eligible(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Eligible for Child Disability Allowance discretionary grant"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783266", "ssa/221/en#P2-S13", "http://www.legislation.govt.nz/act/public/1964/0136/latest/DLM361659.html"
    set_input = holders.set_input_dispatch_by_period

    def formula_1964_12_04(persons, period, parameters):
        # This 1964 section was reviewed when writing the 2018 version and it is likely insufficient
        resident_or_citizen = persons("immigration__citizen_or_resident", period)

        is_principal_carer = persons("social_security__principal_caregiver", period.first_month)
        has_eligible_disabled_child = persons.family("child_disability_allowance__family_has_eligible_child", period)

        # this is possible not correct, in 2018 the general limitation applies
        resides_in_nz = persons(
            "social_security__ordinarily_resident_in_new_zealand", period)

        return resident_or_citizen * \
            resides_in_nz * \
            is_principal_carer * \
            has_eligible_disabled_child

    # Note this is the date the 2018 act commenced
    def formula_2018_11_26(persons, period, parameters):
        ssa78 = persons.family("child_disability_allowance__family_has_eligible_child", period)
        # Note 80, 81 - MSD "may require" points (not coded)

        ssa82 = persons("child_disability_allowance__payment_to", period)
        # 83 - test for other benefits, Veteran's Support Act and ACC compensation

        return ssa78 * ssa82


class child_disability_allowance__payment_to(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Manages who is elegible to recieve the payment"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783275", "ssa/221/en#s82"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        general_limitation = persons("social_security__general_limitation", period)

        # 82 - the allowance is payable to the principal caregiver, temporary OB or UCB caregiver of the child. Or the person "for the time being"
        ssa82 = general_limitation * persons("social_security__principal_caregiver", period.first_month)
        principals = persons.family.any(general_limitation * persons("social_security__principal_caregiver", period.first_month))
        ssa82 = ssa82 + (numpy.logical_not(principals) * general_limitation * persons("social_security__temporary_ob_or_ucb_caregiver", period))
        ucb = persons.family.any(general_limitation * persons("social_security__temporary_ob_or_ucb_caregiver", period))
        ssa82 = ssa82 + (numpy.logical_not(ucb) * general_limitation * persons("social_security__care_and_control", period))

        return ssa82


class child_disability_allowance__child_with_serious_disability(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Child with a serious disability"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783270", "ssa/221/en#s79-p1", "https://www.legislation.govt.nz/act/public/1964/0136/latest/DLM361659.html"
    set_input = holders.set_input_dispatch_by_period

    def formula_2018_11_26(persons, period, parameters):
        ssa79_1 = persons("social_security__dependent_child", period)
        ssa79_1_a = persons("has_disability", period.first_month)
        ssa79_1_b = persons("child_disability_allowance__constant_care_exceeding_12_months", period)

        # ssa79_1_c wrapped up in ssa79_1_b for simplicity

        # ssa79_2 What MSD must consider if discretionary conditions met
        # ssa79_2_a
        # ssa79_2_b
        # ssa79_2_c

        return ssa79_1 * ssa79_1_a * ssa79_1_b


class child_disability_allowance__care_in_home(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Cared for in the home of C’s principal caregiver or temporary OB or UCB caregiver"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783267", "ssa/221/en#s78-p1-b-i"
    set_input = holders.set_input_dispatch_by_period


class child_disability_allowance__approved_weekly_accomodation(variables.Variable):
    value_type = bool
    entity = entities.Person
    definition_period = periods.WEEK
    label = "Child disability allowance -> approved_weekly_accomodation"
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783269", "ssa/221/en#s78-p1-b-ii"
    set_input = holders.set_input_dispatch_by_period


class child_disability_allowance__family_has_eligible_child(variables.Variable):
    value_type = bool
    entity = entities.Family
    definition_period = periods.WEEK
    label = "Does the family have a child who meets the criteria for the child disability allowance"

    def formula(families, period, parameters):
        hd = families.members("child_disability_allowance__allowance_criteria", period)
        return families.any(hd, role=entities.Family.CHILD)


class child_disability_allowance__allowance_criteria(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Has serious disability"
    definition_period = periods.WEEK
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783267", "ssa/221/en#s78", "http://www.legislation.govt.nz/act/public/1964/0136/latest/DLM361659.html"
    set_input = holders.set_input_dispatch_by_period

    def formula_1964_12_04(persons, period, parameters):

        return persons("child_disability_allowance__child_with_serious_disability", period)

    # Note this is the date the 2018 act commenced
    def formula_2018_11_26(persons, period, parameters):
        ssa78_1a = persons("child_disability_allowance__child_with_serious_disability", period)
        ssa78_1b_i = persons.family.members("child_disability_allowance__care_in_home", period)
        ssa78_1b_ii = persons.family.members("child_disability_allowance__approved_weekly_accomodation", period)

        return ssa78_1a * (ssa78_1b_i + ssa78_1b_ii)


class child_disability_allowance__constant_care_exceeding_12_months(variables.Variable):
    value_type = bool
    entity = entities.Person
    label = "Requires constant care and attention"
    definition_period = periods.ETERNITY
    reference = "https://www.legislation.govt.nz/act/public/2018/0032/latest/whole.html#DLM6783270", "ssa/221/en#s79-p1-c"


class child_disability_allowance__granted(variables.Variable):
    value_type = bool
    default_value = False
    entity = entities.Person
    label = "Person is currently granted the Child Disability Allowace"
    definition_period = periods.WEEK
    reference = "Variable is useful for checking: 'granted a main benefit'"
