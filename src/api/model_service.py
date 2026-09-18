import pandas as pd

from src.features.build_features import build_features
import json
from pathlib import Path

import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "models" / "churn_model.joblib"
METADATA_PATH = PROJECT_ROOT / "models" / "model_metadata.json"


def load_model():
    """Load the saved production churn model."""
    return joblib.load(MODEL_PATH)


def load_metadata():
    """Load metadata associated with the production model."""
    with open(METADATA_PATH, "r") as file:
        return json.load(file)


model = load_model()
metadata = load_metadata()

ENGINEERED_FEATURES = [
    "MinutesPerRevenueDollar",
    "EquipmentAgeToTenure",
    "TotalCallActivity",
    "LowUsage",
    "OlderEquipment",
    "HighOverage",
    "LowUsageOlderEquipment",
    "HighRiskHandset",
]

MODEL_FEATURES = model.feature_names_in_.tolist()

RAW_MODEL_FEATURES = [
    feature
    for feature in MODEL_FEATURES
    if feature not in ENGINEERED_FEATURES
]

def get_risk_tier(probability):
    """Convert churn probability into a business risk tier."""

    if probability < 0.20:
        return "Low"
    elif probability < 0.27:
        return "Medium"
    elif probability < 0.40:
        return "High"
    else:
        return "Very High"


def predict_customer(customer_data):
    """Generate a churn prediction from raw customer attributes."""

    customer_df = pd.DataFrame(
        [customer_data]
    )

    thresholds = metadata[
        "feature_engineering_thresholds"
    ]

    customer_engineered = build_features(
        customer_df,
        low_usage_threshold=thresholds[
            "low_usage_threshold"
        ],
        older_equipment_threshold=thresholds[
            "older_equipment_threshold"
        ],
        high_overage_threshold=thresholds[
            "high_overage_threshold"
        ],
    )

    customer_model_input = customer_engineered[
        MODEL_FEATURES
    ]

    probability = float(
        model.predict_proba(
            customer_model_input
        )[0, 1]
    )

    threshold = float(
        metadata["decision_threshold"]
    )

    predicted_churn = int(
        probability >= threshold
    )

    return {
        "churn_probability": round(
            probability,
            4,
        ),
        "predicted_churn": predicted_churn,
        "risk_tier": get_risk_tier(
            probability
        ),
        "decision_threshold": threshold,
    }