-- Customer Churn Intelligence Platform
-- Power BI-ready analytics views


CREATE OR REPLACE VIEW churn.v_customer_risk AS
SELECT
    c.customer_id,
    c.service_area,

    c.months_in_service,
    c.current_equipment_days,

    c.monthly_minutes,
    c.monthly_revenue,
    c.total_recurring_charge,
    c.overage_minutes,

    c.perc_change_minutes,
    c.perc_change_revenues,

    c.handset_price,
    c.credit_rating,
    c.occupation,
    c.age_hh1,
    c.unique_subs,

    c.minutes_per_revenue_dollar,
    c.equipment_age_to_tenure,

    c.low_usage,
    c.older_equipment,
    c.high_overage,

    c.actual_churn,

    p.churn_probability,
    p.predicted_churn,
    p.risk_tier,
    p.scored_at,

    p.model_run_id

FROM churn.customers AS c
JOIN churn.predictions AS p
    ON c.customer_id = p.customer_id;

CREATE OR REPLACE VIEW churn.v_risk_summary AS
SELECT
    p.model_run_id,
    p.risk_tier,

    COUNT(*) AS customer_count,

    ROUND(
        100.0 * COUNT(*) /
        SUM(COUNT(*)) OVER (
            PARTITION BY p.model_run_id
        ),
        2
    ) AS customer_percent,

    ROUND(
        AVG(p.churn_probability),
        4
    ) AS avg_churn_probability,

    SUM(c.actual_churn) AS actual_churners,

    ROUND(
        AVG(c.actual_churn),
        4
    ) AS actual_churn_rate

FROM churn.predictions AS p
JOIN churn.customers AS c
    ON p.customer_id = c.customer_id

GROUP BY
    p.model_run_id,
    p.risk_tier;

CREATE OR REPLACE VIEW churn.v_service_area_risk AS
SELECT
    c.service_area,

    COUNT(*) AS customer_count,

    SUM(c.actual_churn) AS actual_churners,

    ROUND(
        AVG(c.actual_churn),
        4
    ) AS actual_churn_rate,

    ROUND(
        AVG(p.churn_probability),
        4
    ) AS avg_churn_probability,

    SUM(
        CASE
            WHEN p.predicted_churn = 1 THEN 1
            ELSE 0
        END
    ) AS customers_flagged,

    SUM(
        CASE
            WHEN p.risk_tier = 'Very High' THEN 1
            ELSE 0
        END
    ) AS very_high_risk_customers

FROM churn.customers AS c
JOIN churn.predictions AS p
    ON c.customer_id = p.customer_id

GROUP BY c.service_area;

CREATE OR REPLACE VIEW churn.v_retention_priority AS
SELECT
    c.customer_id,
    c.service_area,

    p.churn_probability,
    p.risk_tier,

    c.months_in_service,
    c.current_equipment_days,
    c.monthly_minutes,
    c.monthly_revenue,
    c.total_recurring_charge,
    c.overage_minutes,

    c.minutes_per_revenue_dollar,
    c.equipment_age_to_tenure,

    c.low_usage,
    c.older_equipment,
    c.high_overage,

    c.actual_churn,

    ROW_NUMBER() OVER (
        ORDER BY p.churn_probability DESC
    ) AS retention_priority_rank

FROM churn.customers AS c
JOIN churn.predictions AS p
    ON c.customer_id = p.customer_id

WHERE p.predicted_churn = 1;