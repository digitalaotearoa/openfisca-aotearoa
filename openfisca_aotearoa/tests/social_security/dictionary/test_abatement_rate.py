import numpy
import pytest

from openfisca_core import taxscales, tools

from openfisca_aotearoa.variables.acts.social_security import dictionary


class IncomeTest(taxscales.MarginalRateTaxScale):
    ...


@pytest.fixture
def income_test() -> IncomeTest:
    scale = IncomeTest()
    scale.add_bracket(0, 0.00)
    scale.add_bracket(160, 0.30)
    scale.add_bracket(250, 0.70)
    return scale


def test_abatement_rate_floor(income_test: IncomeTest) -> None:
    rate = numpy.full((4,), 100.00)
    income = numpy.array([159.99, 160.00, 160.99, 161.99])
    abatement = dictionary.AbatementRate(rate, income)(income_test.calc)
    tools.assert_near(abatement, numpy.array([0.00, 0.00, 0.00, 0.30]))


def test_abatement_rate_ceiling(income_test: IncomeTest) -> None:
    rate = numpy.full((4,), 100.00)
    income = numpy.array([249.99, 250.00, 251.00, 251.99])
    abatement = dictionary.AbatementRate(rate, income)(income_test.calc)
    tools.assert_near(abatement, numpy.array([26.70, 27.00, 27.70, 27.70]))


def test_abatement_rate_is_not_negative(income_test: IncomeTest) -> None:
    rate = numpy.full((3,), 100.00)
    income = numpy.array([354.00, 355.00, 356.00])
    abatement = dictionary.AbatementRate(rate, income)(income_test.calc)
    tools.assert_near(abatement, numpy.array([99.80, 100.00, 100.00]))
