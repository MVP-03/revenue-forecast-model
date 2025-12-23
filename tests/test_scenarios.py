import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from scenarios import apply_growth_rate, scenario, run_scenarios, best_case, worst_case


def test_apply_growth_rate_length():
    series = apply_growth_rate(100_000, 0.05, 12)
    assert len(series) == 12


def test_apply_growth_rate_grows():
    series = apply_growth_rate(100_000, 0.05, 3)
    assert series[0] < series[1] < series[2]


def test_scenario_keys():
    s = scenario('test', 100_000, 0.05, months=6)
    assert 'end_arr' in s
    assert 'total_growth' in s
    assert len(s['series']) == 6


def test_run_scenarios_three():
    scenarios = run_scenarios(200_000, months=12)
    assert len(scenarios) == 3


def test_best_case_is_bull():
    scenarios = run_scenarios(100_000)
    assert best_case(scenarios)['scenario'] == 'bull'


def test_worst_case_is_bear():
    scenarios = run_scenarios(100_000)
    assert worst_case(scenarios)['scenario'] == 'bear'
