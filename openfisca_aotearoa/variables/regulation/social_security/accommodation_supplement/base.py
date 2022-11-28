"""TODO: Add missing doctring."""

import string

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

    def formula_2018_11_26(people, period, _params):
        # (2) The base rate is as follows:
        #
        # Beneficiaries who are single

        # We check whether P is beneficiary
        beneficiaries = people("social_security__beneficiary", period)

        # We then calculate all main benefit amounts, as well as emergency
        # benefit, superannuation, and veteran pension.
        emergency_benefit = (
            + people("sole_parent_support__entitled", period)
            * people("sole_parent_support__base", period)
            )

        jobseeker_support = (
            + people("jobseeker_support__entitled", period)
            * people("jobseeker_support__base", period)
            )

        sole_parent_support = (
            + people("sole_parent_support__entitled", period)
            * people("sole_parent_support__base", period)
            )

        superannuation = (
            + people("super__entitled", period)
            * people("super__base", period)
            )

        veterans_pension = (
            + people("veterans_pension__entitled", period)
            * people("veterans_pension__base", period)
            )

        young_parent_payment = (
            + people("young_parent_payment__entitled", period)
            * people("young_parent_payment__base", period)
            )

        youth_payment = (
            + people("youth_payment__entitled", period)
            * people("youth_payment__base", period)
            )

        # We compare the base rates and take the maximum amount.
        rate = numpy.maximum.reduce([
            emergency_benefit,
            jobseeker_support,
            sole_parent_support,
            young_parent_payment,
            superannuation,
            veterans_pension,
            youth_payment,
            ])

        # We assume single as in "no partner"
        principal = people.has_role(entities.Family.PRINCIPAL)
        mingled = principal * people("in_a_relationship", period)
        singles = principal * numpy.logical_not(mingled)

        # We calculate the number of dependent children.
        f_members = people.family.members
        dependent = sum(f_members("social_security__dependent_child", period))
        children = dependent >= 1
        no_child = numpy.logical_not(children)

        # (a) for a single beneficiary under the age of 25 years, the maximum
        #     weekly rate of a benefit that the beneficiary would have been
        #     entitled to receive, before any abatement or deduction, if the
        #     beneficiary had attained the age of 25 years:

        # We assume age on Monday
        monday = period.first_day

        # We assume under 25 years by Monday
        age = people("age", monday)
        under25y = age < 25

        # We need to create a new simulation to calculate a benefit, where
        # people would be 25 years by Monday this week. We assume jobseeker.
        #
        # 1. We clone the current simulation:
        simulation = people.simulation.clone()

        # 2. We delete the actual result of jobseeker base rate:
        simulation.delete_arrays("jobseeker_support__base", period)

        # 3. We make everybody 25 years old:
        simulation.delete_arrays("age", monday)
        simulation.set_input("age", monday, numpy.repeat(25, len(people.ids)))

        # 4. Finally, we delete the result of any other variable we need to
        # recalculate (in our case those related to single beneficiaries):
        for letter in string.ascii_lowercase[0:6]:
            simulation.delete_arrays(f"schedule_4__part1_1_{letter}", period)

        # 5. Then, we recalculate jobseeker base rate as if having 25 years:
        base25y = simulation.calculate("jobseeker_support__base", period)

        # 6. After, we restore the original ages:
        simulation.delete_arrays("age", monday)
        simulation.set_input("age", monday, age)

        # 7. And we re-invalidate the cached calculations:
        for letter in string.ascii_lowercase[0:6]:
            simulation.delete_arrays(f"schedule_4__part1_1_{letter}", period)

        # And apply all the conditions.
        ssr2018_17_2_a = (
            + singles
            * beneficiaries
            * no_child
            * under25y
            * base25y
            )

        # (b) for a single beneficiary with 1 or more dependent children,—
        #     (i)   the maximum weekly rate of a benefit that the beneficiary
        #           is entitled to receive, before any abatement or deduction;
        #           plus
        #     (ii)  the maximum annual rate of family tax credit (divided by
        #           52) that is payable in respect of an eldest dependent child
        #           who is under 16 years old under subparts MA to MF and MZ of
        #           the Income Tax Act 2007:

        # We calculate the maximum amount of tax credit for the eldest.
        this_year = period.this_year
        tax_credit = people("family_tax_credit__eldest", this_year, "add") / 52

        # And apply all the conditions.
        ssr2018_17_2_b = (
            + singles
            * beneficiaries
            * children
            * (rate + tax_credit)
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
            * rate
            )

        return ssr2018_17_2_a + ssr2018_17_2_b + ssr2018_17_2_c
