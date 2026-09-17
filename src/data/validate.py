import pandas as pd


EXPECTED_CHURN_VALUES = {"Yes", "No"}


def validate_duplicates(df: pd.DataFrame) -> dict:
    """Check for duplicate rows and duplicate customer IDs."""

    return {
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_customer_ids": int(
            df["CustomerID"].duplicated().sum()
        ),
    }

def validate_target(df: pd.DataFrame) -> dict:
    """Check that the churn target contains only expected values."""

    actual_values = set(df["Churn"].dropna().unique())

    return {
        "actual_churn_values": actual_values,
        "target_valid": actual_values == EXPECTED_CHURN_VALUES,
    }

def validate_subscriptions(df: pd.DataFrame) -> dict:
    """Check that active subscriptions do not exceed unique subscriptions."""

    invalid_records = int(
        (df["ActiveSubs"] > df["UniqueSubs"]).sum()
    )

    return {
        "active_subs_exceed_unique_subs": invalid_records,
        "subscription_counts_valid": invalid_records == 0,
    }

def validate_handsets(df: pd.DataFrame) -> dict:
    """Check that handset models do not exceed total handsets."""

    invalid_records = int(
        (df["HandsetModels"] > df["Handsets"]).sum()
    )

    return {
        "handset_models_exceed_handsets": invalid_records,
        "handset_counts_valid": invalid_records == 0,
    }

def validate_retention(df: pd.DataFrame) -> dict:
    """Check consistency among retention-related variables."""

    retention_flag_mismatch = int(
        (
            (df["MadeCallToRetentionTeam"] == "Yes")
            != (df["RetentionCalls"] > 0)
        ).sum()
    )

    offers_exceed_calls = int(
        (
            df["RetentionOffersAccepted"]
            > df["RetentionCalls"]
        ).sum()
    )

    return {
        "retention_flag_mismatches": retention_flag_mismatch,
        "accepted_offers_exceed_calls": offers_exceed_calls,
        "retention_data_valid": (
            retention_flag_mismatch == 0
            and offers_exceed_calls == 0
        ),
    }

NON_NEGATIVE_COLUMNS = [
    "MonthlyMinutes",
    "OverageMinutes",
    "RoamingCalls",
    "DroppedCalls",
    "BlockedCalls",
    "UnansweredCalls",
    "CustomerCareCalls",
    "ThreewayCalls",
    "ReceivedCalls",
    "OutboundCalls",
    "InboundCalls",
    "PeakCallsInOut",
    "OffPeakCallsInOut",
    "DroppedBlockedCalls",
    "CallForwardingCalls",
    "CallWaitingCalls",
    "MonthsInService",
    "UniqueSubs",
    "ActiveSubs",
    "Handsets",
    "HandsetModels",
    "RetentionCalls",
    "RetentionOffersAccepted",
    "ReferralsMadeBySubscriber",
    "AdjustmentsToCreditRating",
]

def validate_non_negative_columns(df: pd.DataFrame) -> dict:
    """Check that selected activity and count variables are non-negative."""

    negative_counts = {
        column: int((df[column] < 0).sum())
        for column in NON_NEGATIVE_COLUMNS
    }

    total_negative_values = sum(negative_counts.values())

    return {
        "negative_value_counts": negative_counts,
        "total_negative_values": total_negative_values,
        "non_negative_columns_valid": total_negative_values == 0,
    }

EXPECTED_COLUMNS = {
    "CustomerID",
    "Churn",
    "MonthlyRevenue",
    "MonthlyMinutes",
    "TotalRecurringCharge",
    "DirectorAssistedCalls",
    "OverageMinutes",
    "RoamingCalls",
    "PercChangeMinutes",
    "PercChangeRevenues",
    "DroppedCalls",
    "BlockedCalls",
    "UnansweredCalls",
    "CustomerCareCalls",
    "ThreewayCalls",
    "ReceivedCalls",
    "OutboundCalls",
    "InboundCalls",
    "PeakCallsInOut",
    "OffPeakCallsInOut",
    "DroppedBlockedCalls",
    "CallForwardingCalls",
    "CallWaitingCalls",
    "MonthsInService",
    "UniqueSubs",
    "ActiveSubs",
    "ServiceArea",
    "Handsets",
    "HandsetModels",
    "CurrentEquipmentDays",
    "AgeHH1",
    "AgeHH2",
    "ChildrenInHH",
    "HandsetRefurbished",
    "HandsetWebCapable",
    "TruckOwner",
    "RVOwner",
    "Homeownership",
    "BuysViaMailOrder",
    "RespondsToMailOffers",
    "OptOutMailings",
    "NonUSTravel",
    "OwnsComputer",
    "HasCreditCard",
    "RetentionCalls",
    "RetentionOffersAccepted",
    "NewCellphoneUser",
    "NotNewCellphoneUser",
    "ReferralsMadeBySubscriber",
    "IncomeGroup",
    "OwnsMotorcycle",
    "AdjustmentsToCreditRating",
    "HandsetPrice",
    "MadeCallToRetentionTeam",
    "CreditRating",
    "PrizmCode",
    "Occupation",
    "MaritalStatus",
}

def validate_schema(df: pd.DataFrame) -> dict:
    """Check that the dataset contains exactly the expected columns."""

    actual_columns = set(df.columns)

    missing_columns = EXPECTED_COLUMNS - actual_columns
    unexpected_columns = actual_columns - EXPECTED_COLUMNS

    return {
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
        "schema_valid": (
            len(missing_columns) == 0
            and len(unexpected_columns) == 0
        ),
    }

def run_all_validations(df: pd.DataFrame) -> dict:
    """Run all dataset validation checks and return the results."""

    return {
        "schema": validate_schema(df),
        "duplicates": validate_duplicates(df),
        "target": validate_target(df),
        "subscriptions": validate_subscriptions(df),
        "handsets": validate_handsets(df),
        "retention": validate_retention(df),
        "non_negative_columns": validate_non_negative_columns(df),
    }

def validation_passed(results: dict) -> bool:
    """Return True if all required dataset validation checks pass."""

    return (
        results["schema"]["schema_valid"]
        and results["duplicates"]["duplicate_rows"] == 0
        and results["duplicates"]["duplicate_customer_ids"] == 0
        and results["target"]["target_valid"]
        and results["subscriptions"]["subscription_counts_valid"]
        and results["handsets"]["handset_counts_valid"]
        and results["retention"]["retention_data_valid"]
        and results["non_negative_columns"]["non_negative_columns_valid"]
    )