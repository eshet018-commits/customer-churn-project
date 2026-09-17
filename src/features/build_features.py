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

def add_behavioral_features(df: pd.DataFrame) -> pd.DataFrame:
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
        (df["MonthlyMinutes"] <= 158).astype(int),
    )

    df["OlderEquipment"] = np.where(
        df["CurrentEquipmentDays"].isna(),
        np.nan,
        (df["CurrentEquipmentDays"] > 330).astype(int),
    )

    df["HighOverage"] = np.where(
        df["OverageMinutes"].isna(),
        np.nan,
        (df["OverageMinutes"] >= 66).astype(int),
    )

    return df

def add_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add interaction features based on customer behavior and handset profile."""

    df = df.copy()

    df["LowUsageOlderEquipment"] = np.where(
        df["MonthlyMinutes"].isna()
        | df["CurrentEquipmentDays"].isna(),
        np.nan,
        (
            (df["MonthlyMinutes"] <= 158)
            & (df["CurrentEquipmentDays"] > 330)
        ).astype(int),
    )

    df["HighRiskHandset"] = (
        (df["HandsetRefurbished"] == "Yes")
        & (df["HandsetWebCapable"] == "No")
    ).astype(int)

    return df

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build all engineered features for the customer churn dataset."""

    df = add_ratio_features(df)
    df = add_behavioral_features(df)
    df = add_interaction_features(df)

    return df