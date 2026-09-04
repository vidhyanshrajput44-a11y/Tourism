"""
End-to-end pipeline: generate data → train model.

Run:  python train.py
"""

from data_generator import generate_dataset, print_summary, save_dataset
from model import train_and_save


def main():
    print("=" * 60)
    print("FootPrint — Training Pipeline")
    print("=" * 60)

    print("\n[1/2] Generating synthetic dataset...")
    df = generate_dataset()
    save_dataset(df)
    print_summary(df)

    print("\n[2/2] Training models...")
    metrics = train_and_save()

    print("\n" + "=" * 60)
    print("Training complete!")
    print(f"  Best model: {metrics['best_model'].upper()}")
    print(f"  XGBoost RMSE: {metrics['xgboost']['rmse']}")
    if not metrics.get("prophet", {}).get("skipped"):
        print(f"  Prophet RMSE: {metrics['prophet']['rmse']}")
    print("=" * 60)
    print("\nStart API:  uvicorn api:app --reload")


if __name__ == "__main__":
    main()
