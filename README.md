# revenue-forecast-model

Fits a linear trend to historical MRR data and projects the next N months, with 95% confidence intervals. No external dependencies — uses only Python stdlib (`math`, `statistics`, `csv`).

## Usage

```bash
python -c "from src.forecaster import load_mrr, forecast; import json; print(json.dumps(forecast(load_mrr('data/mrr_history.csv')), indent=2))"
pytest tests/
make run
```

## Sample output

```json
{
  "slope": 4706.25,
  "intercept": 43812.5,
  "r_squared": 0.9987,
  "standard_error": 892.41,
  "avg_mom_growth_pct": 8.21,
  "forecast": [
    {"period": 1, "predicted_mrr": 120612.5, "lower_bound": 118863.4, "upper_bound": 122361.6},
    {"period": 2, "predicted_mrr": 125318.75, "lower_bound": 123569.65, "upper_bound": 127067.85}
  ]
}
```

## Interpreting results

- **slope**: MRR added per month on average across the history window
- **r_squared**: How well the linear trend fits. Values > 0.95 mean the trend is reliable; lower values suggest seasonality or inflection points that a linear model won't capture well
- **avg_mom_growth_pct**: Average month-over-month growth rate — useful to cross-check the slope against percentage-based targets
- **lower/upper_bound**: 95% confidence interval. Widens as you forecast further out

## Motivation

QBR prep was taking 2+ hours of manual Excel work per rep to produce MRR projections. This script reads from a CRM export and produces a forecast with R² in seconds, so we can spend QBR time on strategy rather than spreadsheet wrangling.
