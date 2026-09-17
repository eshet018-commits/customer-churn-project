# Customer Intelligence & Churn Prediction Platform

An end-to-end data science and machine learning project designed to analyze customer behavior, identify drivers of customer churn, and predict customers at risk of leaving a telecommunications provider.

## Project Objectives

- Analyze customer demographics, usage behavior, revenue, and service interactions.
- Identify factors associated with customer churn.
- Develop and compare traditional machine learning and deep learning models.
- Build reproducible data transformation and machine learning pipelines.
- Track machine learning experiments and model performance.
- Serve churn predictions through an API and interactive application.
- Develop business intelligence dashboards for customer and retention analysis.
- Deploy components of the platform using cloud infrastructure.

## Planned Technology Stack

### Data Science & Machine Learning
- Python
- Pandas
- NumPy
- scikit-learn
- XGBoost
- TensorFlow / Keras

### Data Engineering
- PostgreSQL
- SQL
- dbt
- Apache Airflow

### MLOps & Software Engineering
- MLflow
- FastAPI
- Docker
- pytest
- GitHub Actions

### Cloud
- Amazon Web Services (AWS)
- Amazon S3
- Amazon RDS
- AWS compute services

### Visualization
- Power BI
- Streamlit
- Matplotlib

## Project Structure

```text
customer-churn-project/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── sql/
├── dbt/
├── airflow/
├── api/
├── app/
├── dashboards/
├── tests/
├── docker/
├── .github/
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE

## Current Status

### Phase 1 — Project Foundation ✅

- Project repository initialized
- Python virtual environment configured
- Project structure established
- Git/GitHub version control configured

### Phase 2 — AWS Data Storage & Ingestion 🚧

- Amazon S3 bucket created in `us-east-2`
- Raw training and holdout datasets stored in S3
- AWS CLI configured using login-based authentication
- Python S3 integration implemented with boto3
- S3 CSV data can be loaded directly into Pandas

### Next

- Data validation and profiling
- Exploratory data analysis
- PostgreSQL database architecture

## Dataset

This project uses a telecommunications customer churn dataset containing customer demographics, service usage, billing and revenue information, customer service interactions, retention activity, and churn outcomes.

The dataset includes:

- **51,047 training observations**
- **20,000 holdout observations**
- **58 variables**
- Customer demographics and household information
- Service usage and call behavior
- Revenue and billing information
- Customer care interactions
- Retention activity
- Equipment information
- Customer churn outcomes

Raw datasets are stored privately in Amazon S3 and are not committed to this repository.

## Project Roadmap

1. Project foundation and Git/GitHub setup
2. AWS S3 data storage and ingestion
3. Data profiling and validation
4. Exploratory data analysis and feature engineering
5. PostgreSQL database development and advanced SQL
6. dbt data transformations
7. Baseline machine learning models
8. XGBoost churn prediction
9. TensorFlow neural network
10. MLflow experiment tracking
11. Apache Airflow pipeline orchestration
12. FastAPI prediction API
13. Streamlit application
14. Power BI dashboards
15. Docker containerization
16. AWS deployment
17. Automated testing and GitHub Actions CI/CD
18. Final documentation and portfolio presentation