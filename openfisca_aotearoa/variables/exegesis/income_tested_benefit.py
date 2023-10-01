"""Exegesis — Income-tested benefit.

Income-tested benefit is a benefit subject to an income-test. While the term
has been repealed in favour of "main benefit", we use it to refer to any
benefit that is subject to an income-test, whether it is a main benefit or not.

For example, the Accommodation Supplement is not a main benefit, but it is,
under certain conditions, subject to an income-test.

"""

from openfisca_core import indexed_enums


class IncomeTestedBenefit(indexed_enums.Enum):
    sole_parent_support = "sole_parent_support"
