"""
imputation.py — Scientific imputation for exoplanet data.

Key principle: DON'T fill NaNs with column means.
Use physical relationships when possible, and always flag imputed values
so the analysis can track what's real vs. estimated.
"""

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Mass-Radius relationship (Zeng & Sasselov 2016)
# ---------------------------------------------------------------------------

def impute_mass_from_radius(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estimate missing masses from known radii using the M-R relation.

    Zeng & Sasselov (2016):
      For Earth-like rocky planets:  M/M⊕ ≈ (R/R⊕) ^ (1/0.27)
      For 50% H2O planets:          M/M⊕ ≈ (R/R⊕) ^ (1/0.33)
      For 100% H2O planets:         M/M⊕ ≈ (R/R⊕) ^ (1/0.37)

    Strategy:
      - R < 1.5 R⊕  → assume rocky (exponent 1/0.27 ≈ 3.7)
      - 1.5 ≤ R < 4 R⊕ → transitional, use intermediate relation
      - R ≥ 4 R⊕ → uncertain (flag, use rough estimate)
    """
    df = df.copy()
    df["pl_bmasse_imputed"] = 0

    missing_mass = df["pl_bmasse"].isna() & df["pl_rade"].notna() & (df["pl_rade"] > 0)
    n_missing = missing_mass.sum()
    print(f"  Planets missing mass (with known radius): {n_missing}")

    if n_missing > 0:
        radius = df.loc[missing_mass, "pl_rade"].values

        # Default exponent for rocky
        exponent = np.full_like(radius, 1.0 / 0.27)

        # Transition zone: blend
        mid_mask = (radius >= 1.5) & (radius < 4.0)
        exponent[mid_mask] = 1.0 / 0.30

        # Large planets: uncertain
        large_mask = radius >= 4.0
        exponent[large_mask] = 1.0 / 0.33

        estimated_mass = radius ** exponent
        df.loc[missing_mass, "pl_bmasse"] = estimated_mass
        df.loc[missing_mass, "pl_bmasse_imputed"] = 1

    return df


def impute_radius_from_mass(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estimate missing radii from known masses (reverse M-R relation).

    R/R⊕ ≈ (M/M⊕) ^ 0.27  for rocky planets.
    """
    df = df.copy()
    df["pl_rade_imputed"] = 0

    missing_radius = df["pl_rade"].isna() & df["pl_bmasse"].notna() & (df["pl_bmasse"] > 0)
    n_missing = missing_radius.sum()
    print(f"  Planets missing radius (with known mass): {n_missing}")

    if n_missing > 0:
        mass = df.loc[missing_radius, "pl_bmasse"].values

        # Assume rocky for reasonable masses
        exponent = np.full_like(mass, 0.27)
        large_mask = mass > 100  # > Saturn mass, different regime
        exponent[large_mask] = 0.30

        estimated_radius = mass ** exponent
        df.loc[missing_radius, "pl_rade"] = estimated_radius
        df.loc[missing_radius, "pl_rade_imputed"] = 1

    return df


# ---------------------------------------------------------------------------
# Equilibrium temperature imputation
# ---------------------------------------------------------------------------

def impute_equilibrium_temp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estimate missing equilibrium temperatures from stellar and orbital data.

    T_eq = T_star * sqrt(R_star / (2 * a)) * (1 - A)^(1/4)
    where A = albedo (assume 0.3 for unknown planets).

    Simplified form:
    T_eq ≈ T_eff * sqrt(R_star / (2 * a_orbsmax))

    Units: T_eff in K, R_star in R_sun, a in AU.
    """
    df = df.copy()
    df["pl_eqt_imputed"] = 0

    missing_eqt = (
        df["pl_eqt"].isna()
        & df["st_teff"].notna()
        & df["pl_orbsmax"].notna()
        & (df["pl_orbsmax"] > 0)
    )
    n_missing = missing_eqt.sum()
    print(f"  Planets missing equilibrium temp (estimable): {n_missing}")

    if n_missing > 0:
        t_star = df.loc[missing_eqt, "st_teff"].values
        a = df.loc[missing_eqt, "pl_orbsmax"].values

        # If stellar radius is known, use it; otherwise assume 1 R_sun
        if "st_rad" in df.columns:
            r_star = df.loc[missing_eqt, "st_rad"].fillna(1.0).values
        else:
            r_star = np.ones_like(t_star)

        # Albedo assumption: 0.3 (Earth-like)
        albedo_factor = (1 - 0.3) ** 0.25  # ≈ 0.91

        t_eq_est = t_star * np.sqrt(r_star / (2 * a)) * albedo_factor
        df.loc[missing_eqt, "pl_eqt"] = t_eq_est.round(0)
        df.loc[missing_eqt, "pl_eqt_imputed"] = 1

    return df


# ---------------------------------------------------------------------------
# Insolation flux imputation
# ---------------------------------------------------------------------------

def impute_insolation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estimate missing insolation flux from stellar and orbital data.

    Insolation = (L_star / L_sun) / (a / 1 AU)²
    where L_star / L_sun ≈ (T_star / T_sun)⁴ * (R_star / R_sun)²
    and T_sun ≈ 5778 K.
    """
    df = df.copy()
    df["pl_insol_imputed"] = 0

    missing_insol = (
        df["pl_insol"].isna()
        & df["st_teff"].notna()
        & df["pl_orbsmax"].notna()
        & (df["pl_orbsmax"] > 0)
    )
    n_missing = missing_insol.sum()
    print(f"  Planets missing insolation (estimable): {n_missing}")

    if n_missing > 0:
        T_SUN = 5778.0
        t_star = df.loc[missing_insol, "st_teff"].values
        a = df.loc[missing_insol, "pl_orbsmax"].values

        if "st_rad" in df.columns:
            r_star = df.loc[missing_insol, "st_rad"].fillna(1.0).values
        else:
            r_star = np.ones_like(t_star)

        # L/L_sun
        luminosity_ratio = (t_star / T_SUN) ** 4 * (r_star ** 2)
        insol_est = luminosity_ratio / (a ** 2)

        df.loc[missing_insol, "pl_insol"] = insol_est
        df.loc[missing_insol, "pl_insol_imputed"] = 1

    return df


# ---------------------------------------------------------------------------
# Stellar metallicity imputation
# ---------------------------------------------------------------------------

def impute_metallicity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing stellar metallicity with solar value (0.0).
    Conservative default — flag as imputed.
    """
    df = df.copy()
    df["st_met_imputed"] = 0
    n_missing = df["st_met"].isna().sum()
    print(f"  Planets missing metallicity: {n_missing}")

    df["st_met"] = df["st_met"].fillna(0.0)
    df.loc[df["st_met_imputed"] == 0, "st_met_imputed"] = (
        (df["st_met"].isna() | (df["st_met"] == 0.0)).astype(int)
    )

    return df


# ---------------------------------------------------------------------------
# Master imputation pipeline
# ---------------------------------------------------------------------------

def run_scientific_imputation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all scientific imputation methods.
    Returns DataFrame with imputed values and _imputed flags.
    """
    print("Scientific Imputation Report:")
    print("-" * 40)
    df = impute_mass_from_radius(df)
    df = impute_radius_from_mass(df)
    df = impute_insolation(df)
    df = impute_equilibrium_temp(df)
    df = impute_metallicity(df)

    # Summary
    imputed_cols = [c for c in df.columns if c.endswith("_imputed")]
    for col in imputed_cols:
        n = df[col].sum()
        print(f"  {col}: {int(n)} values imputed")

    print("-" * 40)
    return df
