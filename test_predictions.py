"""
Sanity-check script: print 7-day forecast tables for demo destinations.

Run after training:  python test_predictions.py

Weekends and holidays should show visibly higher crowd scores than weekdays.
"""

from model import FootprintPredictor

DEMO_DESTINATIONS = ["taj_mahal", "goa_baga_beach", "manali"]


def print_forecast_table(predictor: FootprintPredictor, dest_id: str) -> None:
    meta = predictor.destinations[dest_id]
    print(f"\n{'=' * 70}")
    print(f"  {meta['name']} ({meta['city']}, {meta['state']})")
    print(f"  Max capacity: {meta['max_capacity']:,}")
    print(f"{'=' * 70}")
    print(f"{'Date':<12} {'Day':<10} {'Wknd':<6} {'Hol':<5} {'Footfall':>10} {'Score':>7} {'Category':<8}")
    print("-" * 70)

    forecasts = predictor.forecast_7_days(dest_id)
    for f in forecasts:
        wknd = "Yes" if f["is_weekend"] else "No"
        hol = "Yes" if f["is_holiday"] else "No"
        print(
            f"{f['date']:<12} {f['day_of_week']:<10} {wknd:<6} {hol:<5} "
            f"{f['predicted_footfall']:>10,} {f['crowd_score']:>7} {f['crowd_category']:<8}"
        )

    # Quick sanity assertion
    weekend_scores = [f["crowd_score"] for f in forecasts if f["is_weekend"]]
    weekday_scores = [f["crowd_score"] for f in forecasts if not f["is_weekend"]]
    if weekend_scores and weekday_scores:
        avg_wknd = sum(weekend_scores) / len(weekend_scores)
        avg_wday = sum(weekday_scores) / len(weekday_scores)
        marker = "✓" if avg_wknd > avg_wday else "✗"
        print(f"\n  {marker} Weekend avg score ({avg_wknd:.0f}) vs weekday ({avg_wday:.0f})")


def main():
    print("FootPrint — Prediction Sanity Check")
    predictor = FootprintPredictor()
    predictor.load()

    if predictor.metrics:
        print(f"\nModel metrics (best: {predictor.best_model_name}):")
        for model_name, m in predictor.metrics.items():
            if isinstance(m, dict) and "mae" in m:
                print(f"  {model_name}: MAE={m['mae']}, RMSE={m['rmse']}")

    for dest_id in DEMO_DESTINATIONS:
        print_forecast_table(predictor, dest_id)

    print(f"\n{'=' * 70}")
    print("Sanity check complete. Start API with: uvicorn api:app --reload")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
