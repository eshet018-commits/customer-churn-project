-- Customer Churn Intelligence Platform
-- PostgreSQL analytics schema
-- Core database tables

CREATE SCHEMA IF NOT EXISTS churn;

CREATE TABLE IF NOT EXISTS churn.model_runs (
    model_run_id BIGSERIAL PRIMARY KEY,

    model_name VARCHAR(100) NOT NULL,
    model_type VARCHAR(100) NOT NULL,

    decision_threshold NUMERIC(6, 4) NOT NULL,

    predictor_count INTEGER NOT NULL,

    validation_roc_auc NUMERIC(6, 4),
    validation_pr_auc NUMERIC(6, 4),

    test_accuracy NUMERIC(6, 4),
    test_precision NUMERIC(6, 4),
    test_recall NUMERIC(6, 4),
    test_f1 NUMERIC(6, 4),
    test_roc_auc NUMERIC(6, 4),
    test_pr_auc NUMERIC(6, 4),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS churn.predictions (
    prediction_id BIGSERIAL PRIMARY KEY,

    customer_id BIGINT NOT NULL,

    model_run_id BIGINT NOT NULL,

    churn_probability NUMERIC(8, 6) NOT NULL
        CHECK (
            churn_probability >= 0
            AND churn_probability <= 1
        ),

    predicted_churn SMALLINT NOT NULL
        CHECK (predicted_churn IN (0, 1)),

    risk_tier VARCHAR(20) NOT NULL
        CHECK (
            risk_tier IN (
                'Low',
                'Medium',
                'High',
                'Very High'
            )
        ),

    scored_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_prediction_model
        FOREIGN KEY (model_run_id)
        REFERENCES churn.model_runs(model_run_id),

    CONSTRAINT uq_customer_model_run
        UNIQUE (customer_id, model_run_id)
);

CREATE TABLE IF NOT EXISTS churn.customers (
    customer_id BIGINT PRIMARY KEY,

    service_area VARCHAR(50),

    months_in_service INTEGER,
    current_equipment_days NUMERIC(10, 2),

    monthly_minutes NUMERIC(12, 2),
    monthly_revenue NUMERIC(12, 2),
    total_recurring_charge NUMERIC(12, 2),
    overage_minutes NUMERIC(12, 2),

    perc_change_minutes NUMERIC(12, 2),
    perc_change_revenues NUMERIC(12, 2),

    handset_price VARCHAR(50),
    credit_rating VARCHAR(50),
    occupation VARCHAR(100),

    age_hh1 NUMERIC(8, 2),
    unique_subs INTEGER,

    minutes_per_revenue_dollar NUMERIC(12, 4),
    equipment_age_to_tenure NUMERIC(12, 4),

    low_usage SMALLINT
        CHECK (low_usage IN (0, 1)),

    older_equipment SMALLINT
        CHECK (older_equipment IN (0, 1)),

    high_overage SMALLINT
        CHECK (high_overage IN (0, 1)),

    actual_churn SMALLINT NOT NULL
        CHECK (actual_churn IN (0, 1))
);

CREATE INDEX IF NOT EXISTS idx_customers_service_area
    ON churn.customers(service_area);

CREATE INDEX IF NOT EXISTS idx_customers_actual_churn
    ON churn.customers(actual_churn);

CREATE INDEX IF NOT EXISTS idx_predictions_risk_tier
    ON churn.predictions(risk_tier);

CREATE INDEX IF NOT EXISTS idx_predictions_probability
    ON churn.predictions(churn_probability);

CREATE INDEX IF NOT EXISTS idx_predictions_model_run
    ON churn.predictions(model_run_id);