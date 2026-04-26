"""
features.py — Derived features for exoplanet clustering.
Each feature has physical meaning, not just statistical convenience.
"""

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Log transforms — compress power-law distributions for clustering
# ---------------------------------------------------------------------------

def add_log_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add log10 versions of key continuous variables.
    Astronomical data is notoriously skewed (periods from hours to millennia).
    Log transforms prevent extreme values from dominating clustering.
    """
    df = df.copy()

    for col, new_col in [
        ("pl_orbper", "log_period"),
        ("pl_rade", "log_rade"),
        ("pl_bmasse", "log_bmasse"),
        ("pl_orbsmax", "log_smax"),
    ]:
        if col in df.columns:
            mask = df[col].notna() & (df[col] > 0)
            df[new_col] = np.nan
            df.loc[mask, new_col] = np.log10(df.loc[mask, col])

    return df


# ---------------------------------------------------------------------------
# Density — calculated from mass and radius
# ---------------------------------------------------------------------------

def add_density(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate bulk density in g/cm³ from mass (M⊕) and radius (R⊕).

    Earth reference: 1 M⊕, 1 R⊕ → 5.51 g/cm³
    Formula: ρ = ρ_earth * (M / M⊕) / (R / R⊕)³
    """
    df = df.copy()
    RHO_EARTH = 5.51  # g/cm³

    mask = (
        df["pl_rade"].notna()
        & df["pl_bmasse"].notna()
        & (df["pl_rade"] > 0)
        & (df["pl_bmasse"] > 0)
    )

    df["pl_dens_calc"] = np.nan
    df.loc[mask, "pl_dens_calc"] = (
        RHO_EARTH * df.loc[mask, "pl_bmasse"] / (df.loc[mask, "pl_rade"] ** 3)
    )

    return df


# ---------------------------------------------------------------------------
# Mass-Radius Ratio — composition proxy
# ---------------------------------------------------------------------------

def add_mass_radius_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """
    M/R ratio — quick composition proxy.
    High values → rocky / iron-rich.
    Low values → gas envelope / low density.
    """
    df = df.copy()
    mask = (
        df["pl_bmasse"].notna()
        & df["pl_rade"].notna()
        & (df["pl_rade"] > 0)
    )
    df["mass_radius_ratio"] = np.nan
    df.loc[mask, "mass_radius_ratio"] = (
        df.loc[mask, "pl_bmasse"] / df.loc[mask, "pl_rade"]
    )
    return df


# ---------------------------------------------------------------------------
# Kepler consistency check — validates orbital data
# ---------------------------------------------------------------------------

def add_kepler_check(df: pd.DataFrame) -> pd.DataFrame:
    """
    Kepler's Third Law: T² ∝ a³  (for a given stellar mass)

    For planets around the same star, T² / a³ should be constant.
    We compute the ratio and flag strongly deviant values (possible data errors).
    Units: T in days, a in AU → ratio ~ 1/M_star (solar masses).
    """
    df = df.copy()
    mask = (
        df["pl_orbper"].notna()
        & df["pl_orbsmax"].notna()
        & (df["pl_orbsmax"] > 0)
        & (df["pl_orbper"] > 0)
    )
    df["kepler_ratio"] = np.nan
    df.loc[mask, "kepler_ratio"] = (
        df.loc[mask, "pl_orbper"] ** 2 / df.loc[mask, "pl_orbsmax"] ** 3
    )

    if mask.sum() > 0:
        median_ratio = df.loc[mask, "kepler_ratio"].median()
        df["kepler_check"] = 0
        # Flag rows more than 10x away from median as suspicious
        df.loc[mask & (df["kepler_ratio"] > median_ratio * 10), "kepler_check"] = 1
        df.loc[mask & (df["kepler_ratio"] < median_ratio / 10), "kepler_check"] = 1
    else:
        df["kepler_check"] = np.nan

    return df


# ---------------------------------------------------------------------------
# Habitable Zone flag — Kopparapu conservative HZ
# ---------------------------------------------------------------------------

def add_hz_flag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag planets in the conservative habitable zone.

    Based on Kopparapu et al. (2014):
    Conservative HZ: 0.2 ≤ insolation flux ≤ 1.7 (Earth flux units)

    Additional constraint: radius < 2 R⊕ (likely rocky)
    """
    df = df.copy()
    df["hz_flag"] = 0

    mask = (
        df["pl_insol"].notna()
        & (df["pl_insol"] >= 0.2)
        & (df["pl_insol"] <= 1.7)
    )
    # Rocky radius constraint
    if "pl_rade" in df.columns:
        mask = mask & (df["pl_rade"] < 2.0)
    # Temperature constraint (liquid water possible with albedo ~0.3)
    if "pl_eqt" in df.columns:
        mask = mask & (df["pl_eqt"] >= 200) & (df["pl_eqt"] <= 320)

    df.loc[mask, "hz_flag"] = 1
    return df


# ---------------------------------------------------------------------------
# Master pipeline — run all feature engineering
# ---------------------------------------------------------------------------

def engineer_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the complete feature engineering pipeline.
    Returns a new DataFrame with all derived features added.
    """
    df = add_log_features(df)
    df = add_density(df)
    df = add_mass_radius_ratio(df)
    df = add_kepler_check(df)
    df = add_hz_flag(df)
    return df


# ---------------------------------------------------------------------------
# Feature list for clustering
# ---------------------------------------------------------------------------

CLUSTERING_FEATURES = [
    "log_rade",
    "log_bmasse",
    "log_period",
    "log_smax",
    "pl_dens_calc",
    "mass_radius_ratio",
    "pl_eqt",
    "st_teff",
    "st_met",
    "sy_pnum",
]
