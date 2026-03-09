"""
SAC training pipeline using Stable-Baselines3.

For each feature set we:
  1. Generate data (train 70% / test 30%)
  2. Build features
  3. Train SAC with tuned hyperparameters
  4. Backtest on held-out test set
  5. Record metrics
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

# Local modules
sys.path.insert(0, os.path.dirname(__file__))
from data_generator import generate_crypto_data
from features import FEATURE_SETS, build_features
from trading_env import CryptoTradingEnv, backtest_model


# ───────────────────────────────────────────────────
# SAC hyperparameter grid (tuned for crypto)
# ───────────────────────────────────────────────────

SAC_HYPERPARAMS = dict(
    learning_rate     = 3e-4,
    buffer_size       = 20_000,
    learning_starts   = 500,
    batch_size        = 64,
    tau               = 0.005,
    gamma             = 0.99,
    train_freq        = 8,
    gradient_steps    = 1,
    ent_coef          = "auto",
    target_update_interval = 1,
    policy_kwargs     = dict(
        net_arch = [64, 64],   # fast for CPU
    ),
    verbose           = 0,
)

TOTAL_TIMESTEPS = 50_000   # ~70s per config on CPU
EVAL_FREQ       = 5_000
N_EVAL_EPISODES = 2
WINDOW_SIZE     = 150      # short episodes → more episodes per training run


def make_env(price_train, feat_train, reward_mode="sharpe", seed=0):
    def _init():
        env = CryptoTradingEnv(
            price_df=price_train,
            feature_df=feat_train,
            window_size=WINDOW_SIZE,
            reward_mode=reward_mode,
        )
        return Monitor(env)
    return _init


def train_and_evaluate(
    feature_set_name: str,
    price_train: pd.DataFrame,
    price_test: pd.DataFrame,
    seed: int = 42,
    reward_mode: str = "sharpe",
    save_dir: str = "models",
) -> dict:
    print(f"\n{'='*60}")
    print(f"  Feature set: {feature_set_name}  |  reward: {reward_mode}")
    print(f"{'='*60}")

    # Build features
    feat_full_train = build_features(price_train, feature_set_name)
    feat_full_test  = build_features(price_test,  feature_set_name)

    print(f"  Train bars: {len(feat_full_train)}  |  Test bars: {len(feat_full_test)}")
    print(f"  Features  : {feat_full_train.shape[1]}")

    # Training env (vec)
    train_env = DummyVecEnv([
        make_env(price_train, feat_full_train, reward_mode=reward_mode, seed=seed)
    ])

    os.makedirs(save_dir, exist_ok=True)
    model_path = os.path.join(save_dir, f"{feature_set_name}_{reward_mode}")

    model = SAC("MlpPolicy", train_env, seed=seed, **SAC_HYPERPARAMS)

    t0 = time.time()
    model.learn(total_timesteps=TOTAL_TIMESTEPS, progress_bar=False)
    elapsed = time.time() - t0

    model.save(model_path)
    print(f"  Model saved → {model_path}.zip")

    # ── Backtest on TEST set ──────────────────────────────
    test_env = CryptoTradingEnv(
        price_df=price_test,
        feature_df=feat_full_test,
        window_size=min(WINDOW_SIZE, len(feat_full_test) - 2),
        reward_mode=reward_mode,
    )
    metrics = backtest_model(model, test_env, n_episodes=5, seed=100)
    metrics["feature_set"]  = feature_set_name
    metrics["reward_mode"]  = reward_mode
    metrics["train_time_s"] = round(elapsed, 1)
    metrics["n_features"]   = feat_full_train.shape[1]

    # Annualise (assuming hourly bars, 8760 hrs/yr)
    bars_per_ep = min(WINDOW_SIZE, len(feat_full_test) - 2)
    ann_factor  = 8760 / bars_per_ep
    metrics["ann_return"] = (1 + metrics["mean_return"]) ** ann_factor - 1

    print(f"  Mean return : {metrics['mean_return']:+.2%}")
    print(f"  Ann. return : {metrics['ann_return']:+.2%}")
    print(f"  Max drawdown: {metrics['mean_max_dd']:.2%}")
    print(f"  Calmar ratio: {metrics['calmar']:.3f}")
    print(f"  Train time  : {elapsed:.0f}s")

    return metrics


# ───────────────────────────────────────────────────
# Main: run all feature sets × reward modes
# ───────────────────────────────────────────────────

def run_full_study():
    print("\n" + "="*60)
    print("   CRYPTO SAC STRATEGY — FULL STUDY")
    print("="*60)

    # Generate data once
    df_full = generate_crypto_data(n_bars=12_000, seed=42)
    split   = int(len(df_full) * 0.70)
    price_train = df_full.iloc[:split]
    price_test  = df_full.iloc[split:]

    print(f"Dataset : {len(df_full)} bars  |  Train {split}  |  Test {len(df_full)-split}")

    reward_modes = ["pnl", "sharpe", "sortino"]
    all_metrics  = []

    for rmode in reward_modes:
        for fs_name in FEATURE_SETS:
            m = train_and_evaluate(
                feature_set_name=fs_name,
                price_train=price_train,
                price_test=price_test,
                seed=42,
                reward_mode=rmode,
                save_dir="models",
            )
            all_metrics.append(m)

    # ── Summary table ─────────────────────────────────────
    results_df = pd.DataFrame(all_metrics)
    results_df = results_df.sort_values("ann_return", ascending=False)

    print("\n\n" + "="*70)
    print("   RESULTS SUMMARY — sorted by Annualised Return")
    print("="*70)
    cols = ["feature_set", "reward_mode", "ann_return", "mean_max_dd",
            "calmar", "n_features", "train_time_s"]
    print(results_df[cols].to_string(index=False, float_format="{:.4f}".format))

    best = results_df.iloc[0]
    print(f"\n★  BEST STRATEGY: {best['feature_set']}  [{best['reward_mode']}]")
    print(f"   Annualised return : {best['ann_return']:+.2%}")
    print(f"   Max drawdown      : {best['mean_max_dd']:.2%}")
    print(f"   Calmar ratio      : {best['calmar']:.3f}")

    # Save results
    os.makedirs("results", exist_ok=True)
    results_df.to_csv("results/sac_study_results.csv", index=False)
    print("\n  Results saved → results/sac_study_results.csv")

    return results_df, best


if __name__ == "__main__":
    results_df, best = run_full_study()
