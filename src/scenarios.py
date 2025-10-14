from typing import List, Dict


def apply_growth_rate(base_arr: float, monthly_rate: float, months: int) -> List[float]:
    series = [base_arr]
    for _ in range(months - 1):
        series.append(round(series[-1] * (1 + monthly_rate), 2))
    return series


def scenario(name: str, base_arr: float, monthly_rate: float, months: int = 12) -> Dict:
    series = apply_growth_rate(base_arr, monthly_rate, months)
    return {
        'scenario':    name,
        'base_arr':    base_arr,
        'monthly_rate':monthly_rate,
        'months':      months,
        'series':      series,
        'end_arr':     series[-1],
        'total_growth':round((series[-1] - base_arr) / base_arr * 100, 1),
    }


def run_scenarios(base_arr: float, months: int = 12) -> List[Dict]:
    return [
        scenario('bear',  base_arr, monthly_rate=0.01, months=months),
        scenario('base',  base_arr, monthly_rate=0.04, months=months),
        scenario('bull',  base_arr, monthly_rate=0.08, months=months),
    ]


def best_case(scenarios: List[Dict]) -> Dict:
    return max(scenarios, key=lambda s: s['end_arr'])


def worst_case(scenarios: List[Dict]) -> Dict:
    return min(scenarios, key=lambda s: s['end_arr'])
