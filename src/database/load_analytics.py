import pandas as pd
from sqlalchemy import text

from src.database.connection import get_engine

def prepare_customer_data(df):
    """Prepare engineered customer data for the analytics database."""

    customer_columns = {
        "CustomerID": "customer_id",
        "ServiceArea": "service_area",
        "MonthsInService": "months_in_service",
        "CurrentEquipmentDays": "current_equipment_days",
        "MonthlyMinutes": "monthly_minutes",
        "MonthlyRevenue": "monthly_revenue",
        "TotalRecurringCharge": "total_recurring_charge",
        "OverageMinutes": "overage_minutes",
        "PercChangeMinutes": "perc_change_minutes",
        "PercChangeRevenues": "perc_change_revenues",
        "HandsetPrice": "handset_price",
        "CreditRating": "credit_rating",
        "Occupation": "occupation",
        "AgeHH1": "age_hh1",
        "UniqueSubs": "unique_subs",
        "MinutesPerRevenueDollar": "minutes_per_revenue_dollar",
        "EquipmentAgeToTenure": "equipment_age_to_tenure",
        "LowUsage": "low_usage",
        "OlderEquipment": "older_equipment",
        "HighOverage": "high_overage",
        "ChurnTarget": "actual_churn",
    }

    missing_columns = [
        column
        for column in customer_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required customer columns: {missing_columns}"
        )

    customers = (
        df[list(customer_columns)]
        .rename(columns=customer_columns)
        .copy()
    )

    customers = customers.astype(object).where(
        pd.notna(customers),
        None
    )
    return customers

def load_customers(df):
    """Load customer analytics data into PostgreSQL."""

    customers = prepare_customer_data(df)

    engine = get_engine()

    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE churn.customers CASCADE")
        )

        customers.to_sql(
            name="customers",
            con=connection,
            schema="churn",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000,
        )

    return len(customers)

def create_model_run(metadata):
    """Insert model metadata and return the generated model_run_id."""

    engine = get_engine()

    query = text("""
        INSERT INTO churn.model_runs (
            model_name,
            model_type,
            decision_threshold,
            predictor_count,
            validation_roc_auc,
            validation_pr_auc,
            test_accuracy,
            test_precision,
            test_recall,
            test_f1,
            test_roc_auc,
            test_pr_auc
        )
        VALUES (
            :model_name,
            :model_type,
            :decision_threshold,
            :predictor_count,
            :validation_roc_auc,
            :validation_pr_auc,
            :test_accuracy,
            :test_precision,
            :test_recall,
            :test_f1,
            :test_roc_auc,
            :test_pr_auc
        )
        RETURNING model_run_id
    """)

    values = {
        "model_name": metadata["model_name"],
        "model_type": metadata["model_type"],
        "decision_threshold": metadata["decision_threshold"],
        "predictor_count": metadata["predictor_count"],
        "validation_roc_auc": metadata["validation_metrics"]["roc_auc"],
        "validation_pr_auc": metadata["validation_metrics"]["pr_auc"],
        "test_accuracy": metadata["test_metrics"]["accuracy"],
        "test_precision": metadata["test_metrics"]["precision"],
        "test_recall": metadata["test_metrics"]["recall"],
        "test_f1": metadata["test_metrics"]["f1"],
        "test_roc_auc": metadata["test_metrics"]["roc_auc"],
        "test_pr_auc": metadata["test_metrics"]["pr_auc"],
    }

    with engine.begin() as connection:
        model_run_id = connection.execute(
            query,
            values
        ).scalar_one()

    return model_run_id

def load_predictions(predictions_df, model_run_id):
    """Load customer churn predictions for a model run into PostgreSQL."""

    predictions = predictions_df.copy()

    predictions["model_run_id"] = model_run_id

    predictions = predictions[
        [
            "customer_id",
            "model_run_id",
            "churn_probability",
            "predicted_churn",
            "risk_tier",
        ]
    ]

    if predictions["customer_id"].duplicated().any():
        raise ValueError(
            "Duplicate customer IDs found in prediction data."
        )

    if predictions["churn_probability"].isna().any():
        raise ValueError(
            "Missing churn probabilities found."
        )

    if not predictions["churn_probability"].between(0, 1).all():
        raise ValueError(
            "Churn probabilities must be between 0 and 1."
        )

    valid_tiers = {
        "Low",
        "Medium",
        "High",
        "Very High",
    }

    if not set(predictions["risk_tier"].unique()).issubset(valid_tiers):
        raise ValueError(
            "Invalid risk tier found in prediction data."
        )

    engine = get_engine()

    with engine.begin() as connection:
        predictions.to_sql(
            name="predictions",
            con=connection,
            schema="churn",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000,
        )

    return len(predictions)