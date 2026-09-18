from fastapi import FastAPI, HTTPException

from src.api.model_service import (
    RAW_MODEL_FEATURES,
    metadata,
    predict_customer,
)
from src.api.schemas import (
    PredictionRequest,
    PredictionResponse,
)


app = FastAPI(
    title="Customer Churn Intelligence API",
    description=(
        "API for customer churn risk scoring "
        "and model information."
    ),
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "service": "Customer Churn Intelligence API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/model")
def model_info():
    return {
        "model_name": metadata["model_name"],
        "model_type": metadata["model_type"],
        "decision_threshold": metadata["decision_threshold"],
        "predictor_count": metadata["predictor_count"],
        "excluded_retention_features": metadata[
            "excluded_retention_features"
        ],
        "validation_metrics": metadata[
            "validation_metrics"
        ],
        "test_metrics": metadata[
            "test_metrics"
        ],
    }


@app.get("/features")
def model_features():
    return {
        "raw_feature_count": len(RAW_MODEL_FEATURES),
        "raw_features": RAW_MODEL_FEATURES,
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(request: PredictionRequest):
    customer_data = request.customer_data

    missing_features = [
        feature
        for feature in RAW_MODEL_FEATURES
        if feature not in customer_data
    ]

    unexpected_features = [
        feature
        for feature in customer_data
        if feature not in RAW_MODEL_FEATURES
    ]

    if missing_features:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Missing required customer features.",
                "missing_features": missing_features,
            },
        )

    if unexpected_features:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Unexpected customer features.",
                "unexpected_features": unexpected_features,
            },
        )

    try:
        return predict_customer(customer_data)

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Prediction failed.",
                "error": str(exc),
            },
        ) from exc