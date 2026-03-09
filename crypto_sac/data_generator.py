"""
Synthetic crypto price data generator.
Produces BTC-like OHLCV data with:
 - Geometric Brownian Motion base
 - GARCH-like volatility clustering
 - Fat-tailed returns (Student-t noise)
 - Realistic intraday patterns
 - Trend regimes (bull/bear/sideways)
"""

import numpy as np
import pandas as pd
from scipy.stats import t as student_t


def generate_crypto_data(
    n_bars: int = 10_000,
    freq: str = "1h",
    seed: int = 42,
    initial_price: float = 30_000.0,
    annual_drift: float = 0.3,
    annual_vol: float = 0.8,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dt = 1 / (365 * 24)  # hourly

    # --- Regime switching (bull / bear / sideways) ---
    n_regimes = n_bars // 500 + 1
    regime_lengths = rng.integers(200, 800, size=n_regimes)
    regimes = np.repeat(rng.choice([0, 1, 2], size=n_regimes, p=[0.45, 0.35, 0.20]), regime_lengths)
    regimes = regimes[:n_bars]
    drift_map = {0: annual_drift, 1: -annual_drift * 0.6, 2: 0.02}
    vol_map   = {0: annual_vol, 1: annual_vol * 1.4, 2: annual_vol * 0.5}

    # --- GARCH(1,1) volatility ---
    omega, alpha, beta = 1e-6, 0.12, 0.85
    sigma2 = np.zeros(n_bars)
    sigma2[0] = (annual_vol * np.sqrt(dt)) ** 2
    eps = rng.standard_normal(n_bars)
    for i in range(1, n_bars):
        sigma2[i] = omega + alpha * (eps[i-1] ** 2) * sigma2[i-1] + beta * sigma2[i-1]

    garch_vol = np.sqrt(sigma2)

    # --- Fat-tailed innovations (Student-t, df=4) ---
    df_t = 4.0
    z = student_t.rvs(df=df_t, size=n_bars, random_state=int(seed))
    z = z / np.sqrt(df_t / (df_t - 2))  # normalise variance to 1

    # --- Log-returns ---
    log_returns = np.zeros(n_bars)
    for i in range(n_bars):
        r = regimes[i]
        mu  = drift_map[r] * dt
        sig = vol_map[r] * garch_vol[i]
        log_returns[i] = mu + sig * z[i]

    # --- Close prices ---
    log_prices = np.log(initial_price) + np.cumsum(log_returns)
    close = np.exp(log_prices)

    # --- OHLCV from close ---
    bar_vol_pct = np.abs(rng.normal(0, annual_vol * np.sqrt(dt) * 2, n_bars))
    high  = close * np.exp( bar_vol_pct * rng.uniform(0.3, 1.0, n_bars))
    low   = close * np.exp(-bar_vol_pct * rng.uniform(0.3, 1.0, n_bars))
    open_ = np.roll(close, 1)
    open_[0] = initial_price

    # Ensure OHLC consistency
    high  = np.maximum(high,  np.maximum(open_, close))
    low   = np.minimum(low,   np.minimum(open_, close))

    # Volume: positively correlated with volatility
    base_vol = 5e8
    volume = base_vol * (1 + 3 * np.abs(log_returns) / np.std(log_returns)) * rng.lognormal(0, 0.4, n_bars)

    idx = pd.date_range("2020-01-01", periods=n_bars, freq=freq)
    df = pd.DataFrame({
        "open":   open_,
        "high":   high,
        "low":    low,
        "close":  close,
        "volume": volume,
        "regime": regimes,
    }, index=idx)

    df.index.name = "datetime"
    return df


if __name__ == "__main__":
    df = generate_crypto_data(n_bars=8760)  # 1 year of hourly data
    print(df.describe())
    print(f"\nPrice range: ${df['close'].min():.0f} – ${df['close'].max():.0f}")
    print(f"Regimes: bull={( df['regime']==0).mean():.1%}  bear={(df['regime']==1).mean():.1%}  sideways={(df['regime']==2).mean():.1%}")
