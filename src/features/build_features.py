import numpy as np
import pandas as pd


def add_ratio_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add ratio-based customer behavior features."""

    df = df.copy()

    df["MinutesPerRevenueDollar"] = np.where(
        df["MonthlyRevenue"] > 0,
        df["MonthlyMinutes"] / df["MonthlyRevenue"],
        np.nan,
    )

    df["EquipmentAgeToTenure"] = np.where(
        (df["CurrentEquipmentDays"] >= 0)
        & (df["MonthsInService"] > 0),
        df["CurrentEquipmentDays"]
        / (df["MonthsInService"] * 30.44),
        np.nan,
    )

    return df

def add_behavioral_features(
    df: pd.DataFrame,
    low_usage_threshold: float,
    older_equipment_threshold: float,
    high_overage_threshold: float,
) -> pd.DataFrame:
    """Add customer usage and behavioral features."""

    df = df.copy()

    df["TotalCallActivity"] = (
        df["ReceivedCalls"]
        + df["OutboundCalls"]
        + df["InboundCalls"]
    )

    df["LowUsage"] = np.where(
        df["MonthlyMinutes"].isna(),
        np.nan,
        (df["MonthlyMinutes"] <= low_usage_threshold).astype(int),
    )

    df["OlderEquipment"] = np.where(
        df["CurrentEquipmentDays"].isna(),
        np.nan,
        (
            df["CurrentEquipmentDays"]
            > older_equipment_threshold
        ).astype(int),
    )

    df["HighOverage"] = np.where(
        df["OverageMinutes"].isna(),
        np.nan,
        (
            df["OverageMinutes"]
            >= high_overage_threshold
        ).astype(int),
    )

    return df

def add_interaction_features(
    df: pd.DataFrame,
    low_usage_threshold: float,
    older_equipment_threshold: float,
) -> pd.DataFrame:
    """Add interaction features based on customer behavior and handset profile."""

    df = df.copy()

    df["LowUsageOlderEquipment"] = np.where(
        df["MonthlyMinutes"].isna()
        | df["CurrentEquipmentDays"].isna(),
        np.nan,
        (
            (df["MonthlyMinutes"] <= low_usage_threshold)
            & (
                df["CurrentEquipmentDays"]
                > older_equipment_threshold
            )
        ).astype(int),
    )

    df["HighRiskHandset"] = (
        (df["HandsetRefurbished"] == "Yes")
        & (df["HandsetWebCapable"] == "No")
    ).astype(int)

    return df

def build_features(
    df: pd.DataFrame,
    low_usage_threshold: float,
    older_equipment_threshold: float,
    high_overage_threshold: float,
) -> pd.DataFrame:
    """Build all engineered features for the customer churn dataset."""

    df = add_ratio_features(df)

    df = add_behavioral_features(
        df,
        low_usage_threshold=low_usage_threshold,
        older_equipment_threshold=older_equipment_threshold,
        high_overage_threshold=high_overage_threshold,
    )

    df = add_interaction_features(
        df,
        low_usage_threshold=low_usage_threshold,
        older_equipment_threshold=older_equipment_threshold,
    )

    return df