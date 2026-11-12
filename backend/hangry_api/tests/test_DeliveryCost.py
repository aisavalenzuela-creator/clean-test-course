from types import SimpleNamespace

import pytest

from api.controllers import Delivery


def make_order(*quantities):
    # Lightweight objects keep these unit tests independent of Django's ORM.
    return [SimpleNamespace(quantity=quantity) for quantity in quantities]


@pytest.mark.parametrize(
    ("quantities", "distance", "expected_fee"),
    [
        # The highest tier applies only when both thresholds are exceeded.
        ((5, 5, 1), 6, 7.50),
        # The middle tier applies when only one high-tier threshold is exceeded.
        ((5, 5, 1), 5, 5.00),
        ((5, 5), 6, 5.00),
        ((2, 2, 2), 4, 5.00),
        # The standard fee is the default, including exact threshold boundaries.
        ((3, 1), 2, 3.50),
        ((3, 2), 4, 3.50),
        ((2, 2, 2), 3, 3.50),
        ((), 0, 3.50),
    ],
)
def test_delivery_fee_tiers(quantities, distance, expected_fee):
    order = make_order(*quantities)

    assert Delivery.calculate(order, distance) == expected_fee
