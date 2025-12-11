import pytest


@pytest.fixture
def base_arr():
    return 500_000.0


@pytest.fixture
def forecast_months():
    return 12


@pytest.fixture
def sample_scenario():
    return {
        'scenario':     'base',
        'base_arr':     500_000.0,
        'monthly_rate': 0.04,
        'months':       12,
        'series':       [500_000 * (1.04 ** i) for i in range(12)],
        'end_arr':      748_500.0,
        'total_growth': 49.7,
    }
