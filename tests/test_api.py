from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)

TEST_CUSTOMER = {
    "MonthlyRevenue": 24.0,
    "MonthlyMinutes": 219.0,
    "TotalRecurringCharge": 22.0,
    "DirectorAssistedCalls": 0.25,
    "OverageMinutes": 0.0,
    "RoamingCalls": 0.0,
    "PercChangeMinutes": -157.0,
    "PercChangeRevenues": -19.0,
    "DroppedCalls": 0.7,
    "BlockedCalls": 0.7,
    "UnansweredCalls": 6.3,
    "CustomerCareCalls": 0.0,
    "ThreewayCalls": 0.0,
    "ReceivedCalls": 97.2,
    "OutboundCalls": 0.0,
    "InboundCalls": 0.0,
    "PeakCallsInOut": 58.0,
    "OffPeakCallsInOut": 24.0,
    "DroppedBlockedCalls": 1.3,
    "CallForwardingCalls": 0.0,
    "CallWaitingCalls": 0.3,
    "MonthsInService": 61,
    "UniqueSubs": 2,
    "ActiveSubs": 1,
    "ServiceArea": "SEAPOR503",
    "Handsets": 2.0,
    "HandsetModels": 2.0,
    "CurrentEquipmentDays": 361.0,
    "AgeHH1": 62.0,
    "AgeHH2": 0.0,
    "ChildrenInHH": "No",
    "HandsetRefurbished": "No",
    "HandsetWebCapable": "Yes",
    "TruckOwner": "No",
    "RVOwner": "No",
    "Homeownership": "Known",
    "BuysViaMailOrder": "Yes",
    "RespondsToMailOffers": "Yes",
    "OptOutMailings": "No",
    "NonUSTravel": "No",
    "OwnsComputer": "Yes",
    "HasCreditCard": "Yes",
    "NewCellphoneUser": "No",
    "NotNewCellphoneUser": "No",
    "ReferralsMadeBySubscriber": 0,
    "IncomeGroup": 4,
    "OwnsMotorcycle": "No",
    "AdjustmentsToCreditRating": 0,
    "HandsetPrice": "30",
    "CreditRating": "1-Highest",
    "PrizmCode": "Suburban",
    "Occupation": "Professional",
    "MaritalStatus": "No",
}

def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "Customer Churn Intelligence API"
    assert data["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_model():
    response = client.get("/model")

    assert response.status_code == 200

    data = response.json()

    assert data["decision_threshold"] == 0.27
    assert data["predictor_count"] == 61


def test_features():
    response = client.get("/features")

    assert response.status_code == 200

    data = response.json()

    assert data["raw_feature_count"] == 53
    assert len(data["raw_features"]) == 53
    assert "MonthlyRevenue" in data["raw_features"]

def test_predict_success():
    response = client.post(
        "/predict",
        json={
            "customer_data": TEST_CUSTOMER
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["churn_probability"] == 0.3053
    assert data["predicted_churn"] == 1
    assert data["risk_tier"] == "High"
    assert data["decision_threshold"] == 0.27

def test_predict_missing_feature():
    customer = TEST_CUSTOMER.copy()
    customer.pop("MonthlyRevenue")

    response = client.post(
        "/predict",
        json={
            "customer_data": customer
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert (
        data["detail"]["message"]
        == "Missing required customer features."
    )

    assert "MonthlyRevenue" in (
        data["detail"]["missing_features"]
    )

def test_predict_unexpected_feature():
    customer = TEST_CUSTOMER.copy()
    customer["FakeFeature"] = 123

    response = client.post(
        "/predict",
        json={
            "customer_data": customer
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert (
        data["detail"]["message"]
        == "Unexpected customer features."
    )

    assert "FakeFeature" in (
        data["detail"]["unexpected_features"]
    )