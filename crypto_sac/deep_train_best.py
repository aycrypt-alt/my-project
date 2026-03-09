"""
Phase 2: Deep training of top-3 strategies from Phase 1.

Top candidates:
  1. B_trend    + sortino  → +18.71% ann.  (best overall)
  2. A_momentum + sortino  → +9.33%  ann.
  3. D_volume   + sharpe   → +6.20%  ann.

Each trained for 200k steps with a refined network + learning rate.
We also test a novel hybrid: B_trend features ∪ D_volume features (call it
F_trend_vol — a custom combination NOT in the Phase 1 grid).
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd

from stable_baselines3 import SAC
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import EvalCallback

sys.path.insert(0, os.path.dirname(__file__))
from data_generator import generate_crypto_data
from features import (
    features_trend, features_volume, features_momentum,
    FEATURE_SETS, build_features
)
from trading_env import CryptoTradingEnv, backtest_model


# ── Custom feature set: Trend + Volume hybrid ─────────────────
def features_trend_vol(df: pd.DataFrame) -> pd.DataFrame:
    """B_trend ∪ D_volume — hypothesis: trend signals + volume confirmation."""
    import pandas as pd
    trend  = features_trend(df)
    volume = features_volume(df)
    return pd.concat([trend, volume], axis=1).fillna(0)


DEEP_FEATURE_SETS = {
    "B_trend":       (features_trend,     "sortino"),
    "A_momentum":    (features_momentum,  "sortino"),
    "D_volume":      (features_volume,    "sharpe"),
    "F_trend_vol":   (features_trend_vol, "sortino"),   # new hybrid
}

DEEP_HYPERPARAMS = dict(
    learning_rate     = 2e-4,
    buffer_size       = 30_000,
    learning_starts   = 1_000,
    batch_size        = 64,
    tau               = 0.005,
    gamma             = 0.995,           # longer horizon — holds positions
    train_freq        = 8,
    gradient_steps    = 1,
    ent_coef          = "auto",
    target_update_interval = 1,
    policy_kwargs     = dict(
        net_arch = [128, 64],            # fast + effective on CPU
    ),
    verbose           = 0,
)

TOTAL_TIMESTEPS  = 200_000
WINDOW_SIZE      = 500
N_BACKTEST_EPS   = 10


def deep_train(name, feat_fn, reward_mode, price_train, price_test, seed=42):
    print(f"\n{'='*65}")
    print(f"  DEEP TRAIN: {name}  |  reward: {reward_mode}")
    print(f"{'='*65}")

    feats_train = feat_fn(price_train).iloc[60:].copy()
    feats_test  = feat_fn(price_test).iloc[60:].copy()

    train_env = DummyVecEnv([lambda: Monitor(
        CryptoTradingEnv(price_train, feats_train, window_size=WINDOW_SIZE,
                         reward_mode=reward_mode, risk_penalty=0.02)
    )])

    model_dir = f"models/deep_{name}_{reward_mode}"
    os.makedirs(model_dir, exist_ok=True)

    model = SAC("MlpPolicy", train_env, seed=seed, **DEEP_HYPERPARAMS)

    t0 = time.time()
    model.learn(total_timesteps=TOTAL_TIMESTEPS, progress_bar=False)
    elapsed = time.time() - t0

    model.save(os.path.join(model_dir, "model"))
    print(f"  Saved → {model_dir}/model.zip  ({elapsed:.0f}s)")

    # ── Backtest on unseen test set ──────────────────────────────
    ws_test = min(WINDOW_SIZE, len(feats_test) - 2)
    test_env = CryptoTradingEnv(price_test, feats_test,
                                 window_size=ws_test,
                                 reward_mode=reward_mode)
    metrics = backtest_model(model, test_env, n_episodes=N_BACKTEST_EPS, seed=200)
    metrics["name"]        = name
    metrics["reward_mode"] = reward_mode
    metrics["train_time_s"]= round(elapsed, 1)
    metrics["n_features"]  = feats_train.shape[1]

    bars_per_ep = ws_test
    ann_factor  = 8760 / bars_per_ep
    metrics["ann_return"]  = (1 + metrics["mean_return"]) ** ann_factor - 1

    print(f"  Mean return  : {metrics['mean_return']:+.3%}")
    print(f"  Ann. return  : {metrics['ann_return']:+.2%}")
    print(f"  Max drawdown : {metrics['mean_max_dd']:.2%}")
    print(f"  Calmar ratio : {metrics['calmar']:.3f}")

    # ── Equity curve for plotting ────────────────────────────────
    obs, _ = test_env.reset(seed=999)
    done   = False
    capitals = [test_env.initial_capital]
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, _, done, _, info = test_env.step(action)
        capitals.append(info.get("capital", capitals[-1]))

    metrics["equity_curve"] = capitals
    return metrics


def run_deep_study():
    print("\n" + "="*65)
    print("   PHASE 2 — DEEP TRAINING: TOP STRATEGIES")
    print("="*65)

    df_full = generate_crypto_data(n_bars=15_000, seed=42)
    split   = int(len(df_full) * 0.70)
    price_train = df_full.iloc[:split]
    price_test  = df_full.iloc[split:]
    print(f"Dataset: {len(df_full)} bars  |  Train {split}  |  Test {len(df_full)-split}")

    all_metrics = []
    for name, (feat_fn, rmode) in DEEP_FEATURE_SETS.items():
        m = deep_train(name, feat_fn, rmode, price_train, price_test, seed=42)
        all_metrics.append({k: v for k, v in m.items() if k != "equity_curve"})

    results_df = pd.DataFrame(all_metrics).sort_values("ann_return", ascending=False)

    print("\n\n" + "="*70)
    print("  PHASE 2 RESULTS — sorted by Annualised Return")
    print("="*70)
    cols = ["name", "reward_mode", "ann_return", "mean_max_dd",
            "calmar", "n_features", "train_time_s"]
    print(results_df[cols].to_string(index=False, float_format="{:.4f}".format))

    best = results_df.iloc[0]
    print(f"\n★  CHAMPION: {best['name']}  [{best['reward_mode']}]")
    print(f"   Annualised return : {best['ann_return']:+.2%}")
    print(f"   Max drawdown      : {best['mean_max_dd']:.2%}")
    print(f"   Calmar ratio      : {best['calmar']:.3f}")

    os.makedirs("results", exist_ok=True)
    results_df.to_csv("results/deep_train_results.csv", index=False)
    print("\n  Saved → results/deep_train_results.csv")

    return results_df, best


if __name__ == "__main__":
    results_df, best = run_deep_study()
