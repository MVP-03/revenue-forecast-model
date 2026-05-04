import pytest
from src.forecaster import linear_regression, r_squared, standard_error, forecast, mom_growth_rates


def test_linear_regression_perfect_fit():
    x = [0, 1, 2, 3, 4]
    y = [10, 12, 14, 16, 18]
    slope, intercept = linear_regression(x, y)
    assert abs(slope - 2.0) < 1e-9
    assert abs(intercept - 10.0) < 1e-9


def test_r_squared_perfect_fit():
    x = [0, 1, 2, 3]
    y = [1, 3, 5, 7]
    slope, intercept = linear_regression(x, y)
    r2 = r_squared(x, y, slope, intercept)
    assert abs(r2 - 1.0) < 1e-9


def test_r_squared_constant_y():
    x = [0, 1, 2, 3]
    y = [4, 4, 4, 4]
    slope, intercept = linear_regression(x, y)
    r2 = r_squared(x, y, slope, intercept)
    assert r2 == 1.0


def test_forecast_returns_correct_periods():
    records = [{'month': f'2025-0{i}', 'mrr': 10000 + i * 500} for i in range(1, 7)]
    result = forecast(records, periods=3)
    assert len(result['forecast']) == 3


def test_forecast_increasing_trend():
    records = [{'month': f'2025-0{i}', 'mrr': 10000 + i * 1000} for i in range(1, 7)]
    result = forecast(records, periods=6)
    first = result['forecast'][0]['predicted_mrr']
    last = result['forecast'][-1]['predicted_mrr']
    assert last > first


def test_forecast_lower_bound_below_upper():
    records = [{'month': f'2025-0{i}', 'mrr': 10000 + i * 500} for i in range(1, 7)]
    result = forecast(records, periods=3)
    for p in result['forecast']:
        assert p['lower_bound'] <= p['predicted_mrr'] <= p['upper_bound']


def test_forecast_predicted_mrr_non_negative():
    records = [{'month': f'2025-0{i}', 'mrr': max(0, 5000 - i * 2000)} for i in range(1, 7)]
    result = forecast(records, periods=6)
    for p in result['forecast']:
        assert p['predicted_mrr'] >= 0


def test_linear_regression_insufficient_data_raises():
    with pytest.raises(ValueError):
        linear_regression([1], [10])


def test_linear_regression_identical_x_raises():
    with pytest.raises(ValueError):
        linear_regression([5, 5, 5], [10, 20, 30])


def test_forecast_positive_slope_on_growth_data():
    records = [{'month': f'2025-0{i}', 'mrr': 10000 + i * 800} for i in range(1, 9)]
    result = forecast(records, periods=6)
    assert result['slope'] > 0


def test_r_squared_in_valid_range():
    records = [{'month': f'2025-{i:02d}', 'mrr': 48000 + i * 3800} for i in range(1, 13)]
    x = list(range(12))
    y = [r['mrr'] for r in records]
    slope, intercept = linear_regression(x, y)
    r2 = r_squared(x, y, slope, intercept)
    assert 0.0 <= r2 <= 1.0


def test_mom_growth_rates_length():
    records = [{'month': f'2025-0{i}', 'mrr': 10000 + i * 500} for i in range(1, 7)]
    rates = mom_growth_rates(records)
    assert len(rates) == 5


def test_forecast_includes_avg_mom_growth():
    records = [{'month': f'2025-0{i}', 'mrr': 10000 + i * 500} for i in range(1, 7)]
    result = forecast(records, periods=3)
    assert 'avg_mom_growth_pct' in result
