"""TODO: Add missing doctring."""

import numpy

from openfisca_core import periods, variables

from openfisca_aotearoa import entities


class accommodation_supplement__base(variables.Variable):
    label = "Social Security Regulations 2018 §17 Base rate"
    reference = "https://www.legislation.govt.nz/regulation/public/2018/0202/latest/LMS96264.html"
    documentation = """TODO"""
    entity = entities.Person
    value_type = float
    default_value = 0
    definition_period = periods.DateUnit.WEEK

    def formula_2018_11_26(people, period, params):
        # We assume age on Monday
        monday = period.first_day

        # We need to create a new simulation to calculate a benefit, where
        # people would be 25 years by Monday this week.
        simulation = people.simulation.clone()
        simulation.delete_arrays("age", monday)
        simulation.set_input("age", monday, numpy.repeat(25, len(people.ids)))

        # (2) The base rate is as follows:
        #
        # Beneficiaries
        beneficiaries = people("accommodation_supplement__beneficiary", period)

        # Who are single
        principal = people.has_role(entities.Family.PRINCIPAL)
        mingled = principal * people("social_security__in_a_relationship", period)
        singles = principal * numpy.logical_not(mingled)

        # We have no dependent children
        children = people("social_security__dependent_children", period) >= 1
        no_child = numpy.logical_not(children)

        # (a) for a single beneficiary under the age of 25 years, the maximum
        #     weekly rate of a benefit that the beneficiary would have been
        #     entitled to receive, before any abatement or deduction, if the
        #     beneficiary had attained the age of 25 years:

        # We assume under 25 years by Monday
        age = people("age", monday)
        under25y = age < 25

        # We determine the list of benefits the person could be receiving now.
        receiving = (
            people("emergency_benefit__receiving", period),
            people("jobseeker_support__receiving", period),
            people("sole_parent_support__receiving", period),
            people("super__receiving", period),
            people("supported_living_payment__receiving", period),
            people("veterans_pension__receiving", period),
            people("young_parent_payment__receiving", period),
            people("youth_payment__receiving", period),
            )

        # We calculate the eligibility and base rate as if having 25 years.
        rate25y = (
            simulation.calculate("emergency_benefit__base", period),
            simulation.calculate("jobseeker_support__base", period),
            simulation.calculate("sole_parent_support__base", period),
            simulation.calculate("super__base", period),
            simulation.calculate("supported_living_payment__base", period),
            simulation.calculate("veterans_pension__base", period),
            simulation.calculate("young_parent_payment__base", period),
            simulation.calculate("youth_payment__base", period),
            )

        # And apply all the conditions.
        ssr2018_17_2_a = (
            + singles
            * beneficiaries
            * no_child
            * under25y
            * numpy.select(receiving, rate25y)
            )

        # (b) for a single beneficiary with 1 or more dependent children,—
        #     (i)   the maximum weekly rate of a benefit that the beneficiary
        #           is entitled to receive, before any abatement or deduction;
        #           plus
        #     (ii)  the maximum annual rate of family tax credit (divided by
        #           52) that is payable in respect of an eldest dependent child
        #           who is under 16 years old under subparts MA to MF and MZ of
        #           the Income Tax Act 2007:

        # We calculate the base base rate of the receiving benefit.
        rates = (
            people("emergency_benefit__base", period),
            people("jobseeker_support__base", period),
            people("sole_parent_support__base", period),
            people("super__base", period),
            people("supported_living_payment__base", period),
            people("veterans_pension__base", period),
            people("young_parent_payment__base", period),
            people("youth_payment__base", period),
            )

        # We calculate the maximum amount of tax credit for the eldest.
        this_year = period.this_year
        tax_credit = people("family_tax_credit__eldest", this_year, "add") / 52

        # And apply all the conditions.
        ssr2018_17_2_b = (
            + singles
            * beneficiaries
            * children
            * (numpy.select(receiving, rates) + tax_credit)
            )

        # (c) for any other single beneficiary, the maximum weekly rate of a
        #     benefit that the beneficiary would be entitled to receive before
        #     any abatement or deduction:

        # We get the reminder of the beneficiaries.
        leastwise25y = numpy.logical_not(under25y)

        # And apply all the conditions.
        ssr2018_17_2_c = (
            + singles
            * beneficiaries
            * no_child
            * leastwise25y
            * numpy.select(receiving, rates)
            )

        # Who are in a relationship

        # (d) for a beneficiary who is in a relationship and is not a
        #     beneficiary to whom paragraph (e) applies,—
        #     (i)   the maximum weekly rate of a benefit that the beneficiary
        #           is entitled to receive, before any abatement or deduction;
        #           plus
        #     (ii)  if the beneficiary has 1 or more dependent children, the
        #           maximum annual rate of family tax credit (divided by 52)
        #           that is paid in respect of an eldest dependent child who is
        #           under 16 years (if any) under subparts MA to MF and MZ of
        #           the Income Tax Act 2007; plus
        #     (iii) the maximum weekly rate of a benefit paid in respect of the
        #           beneficiary’s spouse or partner:
        receive_partners = numpy.sum([
            + people.has_role(entities.Family.PARTNER)
            * numpy.select(receiving, rates),
            ])

        ssr2018_17_2_d_i_iii = (
            + mingled
            * beneficiaries
            * no_child
            * (numpy.select(receiving, rates) + receive_partners)
            )

        ssr2018_17_2_d_ii_iii = (
            + mingled
            * beneficiaries
            * children
            * (numpy.select(receiving, rates) + receive_partners + tax_credit)
            )

        ssr2018_17_2_d = (
            + ssr2018_17_2_d_i_iii
            + ssr2018_17_2_d_ii_iii
            )

        # (e) for a beneficiary who is in a relationship and whose spouse or
        #     partner is not entitled to an accommodation supplement under
        #     section 230 of the Act, the rate specified in paragraph (d) as if
        #     a rate of a benefit were paid in respect of that spouse or
        #     partner:

        # TODO: ssr2018_17_2_e

        # Non-beneficiaries who are single -
        non_beneficiaries = numpy.logical_not(beneficiaries)

        # (f) for a single non-beneficiary with 1 or more dependent children,—
        #     (i)   the appropriate maximum weekly rate of jobseeker support;
        #           plus
        #     (ii)  the annual rate of family tax credit (divided by 52) that
        #           is payable in respect of an eldest dependent child who is
        #           under 16 years under subparts MA to MF and MZ of the Income
        #           Tax Act 2007:
        eligible = people("jobseeker_support__entitled", period)

        ssr2018_17_2_f = (
            + singles
            * non_beneficiaries
            * children
            * eligible
            * (rates[1] + tax_credit)
            )

        # (g) for any other single non-beneficiary, the weekly rate of
        #     jobseeker support at the rate in clause 1(d) of Part 1 of
        #     Schedule 4 of the Act before any abatement or deduction:
        ssa2018_sched_4_part_1_clause_1_d = (
            params(period)
            .social_security
            .jobseeker_support
            .base
            .clauses
            .clause_1_d
            )

        ssr2018_17_2_g = (
            + singles
            * non_beneficiaries
            * no_child
            * eligible
            * ssa2018_sched_4_part_1_clause_1_d
            )

        # Non-beneficiaries who are in a relationship -
        #
        # (h) for a non-beneficiary who is in a relationship,—
        #     (i)   the appropriate maximum weekly rate of jobseeker support;
        #           plus
        #     (ii)  if the beneficiary has 1 or more dependent children, the
        #           maximum annual rate of family tax credit (divided by 52)
        #           that is payable in respect of an eldest dependent child who
        #           is under 16 years under subparts MA to MF and MZ of the
        #           Income Tax Act 2007; plus
        #     (iii) the maximum weekly rate of jobseeker support that would
        #           have been payable in respect of the beneficiary’s spouse or
        #           partner.
        rate_partners = numpy.sum([
            + people.has_role(entities.Family.PARTNER)
            * eligible
            * rates[1],
            ])

        ssr2018_17_2_h_i_iii = (
            + mingled
            * non_beneficiaries
            * no_child
            * eligible
            * (rates[1] + rate_partners)
            )

        ssr2018_17_2_h_ii_iii = (
            + mingled
            * non_beneficiaries
            * children
            * eligible
            * (rates[1] + tax_credit + rate_partners)
            )

        ssr2018_17_2_h = (
            + ssr2018_17_2_h_i_iii
            + ssr2018_17_2_h_ii_iii
            )

        return (
            + ssr2018_17_2_a
            + ssr2018_17_2_b
            + ssr2018_17_2_c
            + ssr2018_17_2_d
            + ssr2018_17_2_f
            + ssr2018_17_2_g
            + ssr2018_17_2_h
            )
