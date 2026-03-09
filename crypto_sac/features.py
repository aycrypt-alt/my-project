"""
Feature engineering: 5 indicator sets tested by SAC.

Set A – Momentum  : RSI, Stochastic %K/%D, Williams %R, ROC, CCI
Set B – Trend     : EMA-cross, MACD, ADX/+DI/-DI, Aroon
Set C – Volatility: Bollinger %B + bandwidth, ATR, Keltner %K, HV
Set D – Volume    : OBV-norm, MFI, VWAP-dist, CMF, AD-line
Set E – Combined  : best 3 from each set above (12-feature fusion)

All features are normalised to roughly [-1, 1] to help the neural net.
"""

import numpy as np
import pandas as pd
import talib


# ───────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────

def _safe_norm(s: pd.Series, window: int = 200) -> pd.Series:
    """Rolling z-score normalisation."""
    mu  = s.rolling(window, min_periods=20).mean()
    std = s.rolling(window, min_periods=20).std().replace(0, 1e-9)
    return ((s - mu) / std).clip(-4, 4)


def _minmax(s: pd.Series, lo: float = 0, hi: float = 100) -> pd.Series:
    """Map [lo, hi] → [-1, 1]."""
    return (2 * (s - lo) / (hi - lo) - 1).clip(-1, 1)


# ───────────────────────────────────────────────────
# Set A – Momentum
# ───────────────────────────────────────────────────

def features_momentum(df: pd.DataFrame) -> pd.DataFrame:
    o, h, l, c, v = df.open.values, df.high.values, df.low.values, df.close.values, df.volume.values

    rsi14 = talib.RSI(c, timeperiod=14)
    rsi28 = talib.RSI(c, timeperiod=28)
    stoch_k, stoch_d = talib.STOCH(h, l, c, fastk_period=14, slowk_period=3, slowd_period=3)
    willr  = talib.WILLR(h, l, c, timeperiod=14)
    roc10  = talib.ROC(c, timeperiod=10)
    cci14  = talib.CCI(h, l, c, timeperiod=14)
    mom10  = talib.MOM(c, timeperiod=10)

    out = pd.DataFrame(index=df.index)
    out["rsi14"]   = _minmax(pd.Series(rsi14,   index=df.index))
    out["rsi28"]   = _minmax(pd.Series(rsi28,   index=df.index))
    out["stoch_k"] = _minmax(pd.Series(stoch_k, index=df.index))
    out["stoch_d"] = _minmax(pd.Series(stoch_d, index=df.index))
    out["willr"]   = _minmax(pd.Series(willr,   index=df.index), -100, 0)
    out["roc10"]   = _safe_norm(pd.Series(roc10,  index=df.index))
    out["cci14"]   = _safe_norm(pd.Series(cci14,  index=df.index))
    out["mom10"]   = _safe_norm(pd.Series(mom10,  index=df.index))
    return out.fillna(0)


# ───────────────────────────────────────────────────
# Set B – Trend
# ───────────────────────────────────────────────────

def features_trend(df: pd.DataFrame) -> pd.DataFrame:
    c = df.close.values
    h, l = df.high.values, df.low.values

    ema8    = talib.EMA(c, timeperiod=8)
    ema21   = talib.EMA(c, timeperiod=21)
    ema55   = talib.EMA(c, timeperiod=55)
    macd, macd_sig, macd_hist = talib.MACD(c, fastperiod=12, slowperiod=26, signalperiod=9)
    adx     = talib.ADX(h, l, c, timeperiod=14)
    plus_di = talib.PLUS_DI(h, l, c, timeperiod=14)
    minus_di= talib.MINUS_DI(h, l, c, timeperiod=14)
    aroon_d, aroon_u = talib.AROON(h, l, timeperiod=25)

    # EMA alignment score: how stacked are the EMAs?
    ema_align = np.sign(ema8 - ema21) + np.sign(ema21 - ema55)  # in {-2,-1,0,1,2}

    out = pd.DataFrame(index=df.index)
    c_ser = pd.Series(c, index=df.index)
    out["ema_cross"]  = _safe_norm(pd.Series(ema8 - ema21, index=df.index))
    out["ema_align"]  = pd.Series(ema_align / 2, index=df.index).fillna(0)
    out["macd_hist"]  = _safe_norm(pd.Series(macd_hist, index=df.index))
    out["macd_sig"]   = _safe_norm(pd.Series(macd_sig,  index=df.index))
    out["adx"]        = _minmax(pd.Series(adx, index=df.index), 0, 100)
    out["di_diff"]    = _minmax(pd.Series(plus_di - minus_di, index=df.index), -100, 100)
    out["aroon_osc"]  = _minmax(pd.Series(aroon_u - aroon_d,  index=df.index), -100, 100)
    out["price_ema55"]= _safe_norm(pd.Series((c - ema55) / (ema55 + 1e-9), index=df.index))
    return out.fillna(0)


# ───────────────────────────────────────────────────
# Set C – Volatility
# ───────────────────────────────────────────────────

def features_volatility(df: pd.DataFrame) -> pd.DataFrame:
    c = df.close.values
    h, l = df.high.values, df.low.values

    bb_up, bb_mid, bb_lo = talib.BBANDS(c, timeperiod=20, nbdevup=2, nbdevdn=2)
    atr14  = talib.ATR(h, l, c, timeperiod=14)
    atr50  = talib.ATR(h, l, c, timeperiod=50)
    stddev = talib.STDDEV(c, timeperiod=20)
    natr   = talib.NATR(h, l, c, timeperiod=14)

    bb_width = (bb_up - bb_lo) / (bb_mid + 1e-9)
    bb_pct   = (c - bb_lo) / (bb_up - bb_lo + 1e-9)   # 0=at lower, 1=at upper
    atr_ratio= atr14 / (atr50 + 1e-9)                 # short/long ATR — vol regime

    # Keltner channel % position (using ATR)
    ema20   = talib.EMA(c, timeperiod=20)
    kelt_up = ema20 + 2 * atr14
    kelt_lo = ema20 - 2 * atr14
    kelt_pct= (c - kelt_lo) / (kelt_up - kelt_lo + 1e-9)

    out = pd.DataFrame(index=df.index)
    out["bb_pct"]    = pd.Series(bb_pct,   index=df.index).clip(0, 1) * 2 - 1
    out["bb_width"]  = _safe_norm(pd.Series(bb_width,  index=df.index))
    out["atr_ratio"] = _safe_norm(pd.Series(atr_ratio, index=df.index))
    out["natr"]      = _safe_norm(pd.Series(natr,      index=df.index))
    out["kelt_pct"]  = pd.Series(kelt_pct, index=df.index).clip(0, 1) * 2 - 1
    out["stddev_n"]  = _safe_norm(pd.Series(stddev / (c + 1e-9), index=df.index))
    return out.fillna(0)


# ───────────────────────────────────────────────────
# Set D – Volume
# ───────────────────────────────────────────────────

def features_volume(df: pd.DataFrame) -> pd.DataFrame:
    c = df.close.values
    h, l, v = df.high.values, df.low.values, df.volume.values

    obv   = talib.OBV(c, v)
    mfi14 = talib.MFI(h, l, c, v, timeperiod=14)
    adl   = talib.AD(h, l, c, v)

    # CMF – Chaikin Money Flow
    mf_mult   = ((c - l) - (h - c)) / (h - l + 1e-9)
    mf_vol    = mf_mult * v
    cmf = (pd.Series(mf_vol).rolling(20).sum() /
           pd.Series(v).rolling(20).sum().replace(0, 1e-9)).values

    # VWAP distance (rolling 24-bar)
    tp   = (h + l + c) / 3
    vwap = (pd.Series(tp * v).rolling(24).sum() /
            pd.Series(v).rolling(24).sum().replace(0, 1e-9)).values
    vwap_dist = (c - vwap) / (vwap + 1e-9)

    # Volume ratio: current vs 20-bar avg
    vol_ratio = v / (pd.Series(v).rolling(20).mean().values + 1e-9)

    out = pd.DataFrame(index=df.index)
    out["obv_n"]     = _safe_norm(pd.Series(obv,       index=df.index))
    out["mfi14"]     = _minmax(pd.Series(mfi14,        index=df.index))
    out["adl_n"]     = _safe_norm(pd.Series(adl,       index=df.index))
    out["cmf"]       = pd.Series(cmf,       index=df.index).clip(-1, 1).fillna(0)
    out["vwap_dist"] = _safe_norm(pd.Series(vwap_dist, index=df.index))
    out["vol_ratio"] = _safe_norm(pd.Series(vol_ratio, index=df.index))
    return out.fillna(0)


# ───────────────────────────────────────────────────
# Set E – Combined (best 3 from each of A-D)
# ───────────────────────────────────────────────────

def features_combined(df: pd.DataFrame) -> pd.DataFrame:
    ma = features_momentum(df)[["rsi14", "cci14", "stoch_k"]]
    mb = features_trend(df)[["macd_hist", "ema_align", "adx"]]
    mc = features_volatility(df)[["bb_pct", "atr_ratio", "natr"]]
    md = features_volume(df)[["cmf", "vwap_dist", "mfi14"]]
    return pd.concat([ma, mb, mc, md], axis=1).fillna(0)


# ───────────────────────────────────────────────────
# Registry
# ───────────────────────────────────────────────────

FEATURE_SETS = {
    "A_momentum":   features_momentum,
    "B_trend":      features_trend,
    "C_volatility": features_volatility,
    "D_volume":     features_volume,
    "E_combined":   features_combined,
}


def build_features(df: pd.DataFrame, set_name: str) -> pd.DataFrame:
    fn = FEATURE_SETS[set_name]
    feats = fn(df)
    # Drop first 60 rows (warm-up)
    feats = feats.iloc[60:].copy()
    return feats


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "..")
    from data_generator import generate_crypto_data
    df = generate_crypto_data(n_bars=5000)
    for name in FEATURE_SETS:
        f = build_features(df, name)
        print(f"{name:16s}: {f.shape[1]} features, NaN={f.isna().sum().sum()}")
