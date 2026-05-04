import csv
import math
from statistics import mean


def load_mrr(path):
    records = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({'month': row['month'].strip(), 'mrr': float(row['mrr_usd'])})
    records.sort(key=lambda r: r['month'])
    return records


def linear_regression(x_values, y_values):
    n = len(x_values)
    if n < 2:
        raise ValueError('Need at least 2 data points')
    x_mean = mean(x_values)
    y_mean = mean(y_values)
    ss_xy = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
    ss_xx = sum((x - x_mean) ** 2 for x in x_values)
    if ss_xx == 0:
        raise ValueError('All x values are identical — cannot fit a line')
    slope = ss_xy / ss_xx
    intercept = y_mean - slope * x_mean
    return slope, intercept


def r_squared(x_values, y_values, slope, intercept):
    y_mean = mean(y_values)
    y_pred = [slope * x + intercept for x in x_values]
    ss_res = sum((y - yp) ** 2 for y, yp in zip(y_values, y_pred))
    ss_tot = sum((y - y_mean) ** 2 for y in y_values)
    if ss_tot == 0:
        return 1.0
    return 1 - ss_res / ss_tot


def standard_error(x_values, y_values, slope, intercept):
    n = len(x_values)
    y_pred = [slope * x + intercept for x in x_values]
    sse = sum((y - yp) ** 2 for y, yp in zip(y_values, y_pred))
    return math.sqrt(sse / max(n - 2, 1))


def mom_growth_rates(records):
    rates = []
    for i in range(1, len(records)):
        prev = records[i - 1]['mrr']
        curr = records[i]['mrr']
        if prev > 0:
            rates.append(round((curr - prev) / prev * 100, 2))
    return rates


def forecast(records, periods=6):
    x = list(range(len(records)))
    y = [r['mrr'] for r in records]
    slope, intercept = linear_regression(x, y)
    r2 = r_squared(x, y, slope, intercept)
    se = standard_error(x, y, slope, intercept)
    growth_rates = mom_growth_rates(records)
    avg_mom_growth = round(mean(growth_rates), 2) if growth_rates else 0.0
    predictions = []
    for i in range(1, periods + 1):
        xi = len(records) - 1 + i
        predicted = slope * xi + intercept
        predictions.append({
            'period': i,
            'predicted_mrr': round(max(predicted, 0), 2),
            'lower_bound': round(max(predicted - 1.96 * se, 0), 2),
            'upper_bound': round(predicted + 1.96 * se, 2),
        })
    return {
        'slope': round(slope, 2),
        'intercept': round(intercept, 2),
        'r_squared': round(r2, 4),
        'standard_error': round(se, 2),
        'avg_mom_growth_pct': avg_mom_growth,
        'forecast': predictions,
    }
