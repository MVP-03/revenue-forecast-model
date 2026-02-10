from typing import List, Dict


def format_scenario_table(scenarios: List[Dict]) -> str:
    lines = [
        f"{'Scenario':<10} {'Base ARR':>12}  {'End ARR':>12}  {'Growth':>8}",
        '-' * 48,
    ]
    for s in scenarios:
        lines.append(
            f"{s['scenario']:<10} ${s['base_arr']:>11,.0f}  "
            f"${s['end_arr']:>11,.0f}  {s['total_growth']:>7.1f}%"
        )
    return '\n'.join(lines)


def format_monthly_series(scenario: Dict) -> str:
    lines = [f"Monthly ARR — {scenario['scenario'].title()} case", '-' * 30]
    for i, arr in enumerate(scenario['series'], 1):
        lines.append(f'Month {i:>2}: ${arr:>12,.2f}')
    return '\n'.join(lines)
