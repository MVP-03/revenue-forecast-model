from typing import Dict, List


def validate_forecast_inputs(base_arr: float, months: int) -> List[str]:
    errors = []
    if base_arr <= 0:
        errors.append('base_arr must be positive')
    if not (1 <= months <= 60):
        errors.append('months must be between 1 and 60')
    return errors


def validate_scenario(scenario: Dict) -> List[str]:
    errors = []
    if not scenario.get('scenario'):
        errors.append('scenario name is required')
    rate = scenario.get('monthly_rate', None)
    if rate is None or not (-0.5 <= float(rate) <= 0.5):
        errors.append('monthly_rate must be in [-0.5, 0.5]')
    return errors
