"""
Custom Gymnasium environment for crypto trading.

Action space  : Box(1,)  ∈ [-1, 1]
  -1 = full short, 0 = flat, +1 = full long
  (fractional positions supported)

Observation   : [features..., position, unrealised_pnl_pct, drawdown_pct,
                  time_in_position_norm, portfolio_return_norm]

Reward        : Differential Sharpe – encourages risk-adjusted returns
                + small position-change penalty  (realistic slippage proxy)

Episode       : Fixed-length window drawn randomly from the dataset.
"""

import numpy as np
import pandas as pd
import gymnasium as gym
from gymnasium import spaces


class CryptoTradingEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(
        self,
        price_df: pd.DataFrame,
        feature_df: pd.DataFrame,
        window_size: int = 1000,        # bars per episode
        initial_capital: float = 10_000.0,
        commission: float = 0.001,      # 0.1% per side
        slippage: float = 0.0005,       # 0.05% per side
        max_position: float = 1.0,      # max fraction of capital
        reward_mode: str = "sharpe",    # "sharpe" | "pnl" | "sortino"
        risk_penalty: float = 0.01,     # penalise large drawdowns
    ):
        super().__init__()

        # Align indices
        common = price_df.index.intersection(feature_df.index)
        self.prices   = price_df.loc[common, "close"].values.astype(np.float32)
        self.features = feature_df.loc[common].values.astype(np.float32)

        self.n_features     = self.features.shape[1]
        self.window_size    = min(window_size, len(self.prices) - 1)
        self.initial_capital= initial_capital
        self.commission     = commission
        self.slippage       = slippage
        self.max_position   = max_position
        self.reward_mode    = reward_mode
        self.risk_penalty   = risk_penalty

        # Extra state dimensions added to features
        n_state = 5   # position, upnl%, drawdown%, time_in_pos, port_ret
        obs_dim = self.n_features + n_state

        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(obs_dim,), dtype=np.float32
        )
        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(1,), dtype=np.float32
        )

        self._rng = np.random.default_rng(0)
        self.reset()

    # ------------------------------------------------------------------
    def reset(self, *, seed=None, options=None):
        if seed is not None:
            self._rng = np.random.default_rng(seed)

        max_start = len(self.prices) - self.window_size - 1
        self._start = int(self._rng.integers(0, max(1, max_start)))
        self._end   = self._start + self.window_size
        self._step  = 0

        self.capital         = self.initial_capital
        self.position        = 0.0          # fraction [-1, 1]
        self.entry_price     = 0.0
        self.peak_capital    = self.initial_capital
        self.time_in_pos     = 0
        self._returns        = []           # episode return series
        self._prev_portfolio = self.initial_capital

        return self._get_obs(), {}

    # ------------------------------------------------------------------
    def _get_obs(self):
        idx  = self._start + self._step
        feat = self.features[idx].copy()

        price = self.prices[idx]
        upnl  = 0.0
        if self.position != 0 and self.entry_price > 0:
            upnl = self.position * (price - self.entry_price) / (self.entry_price + 1e-9)

        port_val  = self.capital * (1 + upnl * self.max_position)
        self.peak_capital = max(self.peak_capital, port_val)
        drawdown  = (port_val - self.peak_capital) / (self.peak_capital + 1e-9)

        port_ret = (port_val - self.initial_capital) / self.initial_capital

        state = np.array([
            np.clip(self.position, -1, 1),
            np.clip(upnl,          -2, 2),
            np.clip(drawdown,      -1, 0),
            np.clip(self.time_in_pos / 100.0, 0, 1),
            np.clip(port_ret,      -2, 2),
        ], dtype=np.float32)

        return np.concatenate([feat, state])

    # ------------------------------------------------------------------
    def step(self, action: np.ndarray):
        target_pos = float(np.clip(action[0], -1, 1)) * self.max_position

        idx   = self._start + self._step
        price = self.prices[idx]

        # --- Execute trade ---
        delta = target_pos - self.position
        trade_cost = abs(delta) * (self.commission + self.slippage)

        # PnL from closing/adjusting position
        if self.position != 0 and self.entry_price > 0:
            pnl_frac = self.position * (price - self.entry_price) / (self.entry_price + 1e-9)
        else:
            pnl_frac = 0.0

        # Update capital (simplified mark-to-market)
        realised = 0.0
        if abs(delta) > 0.01:
            realised = pnl_frac * abs(delta / (self.position + 1e-9)) if self.position != 0 else 0
            self.capital *= (1 + realised - trade_cost)
            if target_pos != 0:
                self.entry_price = price * (1 + np.sign(delta) * self.slippage)
            else:
                self.entry_price = 0.0
            self.position    = target_pos
            self.time_in_pos = 0
        else:
            self.time_in_pos += 1

        # Portfolio value this step
        curr_portfolio = self.capital
        if self.position != 0 and self.entry_price > 0:
            curr_portfolio *= (1 + self.position * (price - self.entry_price) / (self.entry_price + 1e-9))

        step_return = (curr_portfolio - self._prev_portfolio) / (self._prev_portfolio + 1e-9)
        self._returns.append(step_return)
        self._prev_portfolio = curr_portfolio

        # --- Reward ---
        reward = self._compute_reward(step_return, curr_portfolio)

        self._step += 1
        done = (self._step >= self.window_size - 1)
        truncated = False

        obs = self._get_obs() if not done else np.zeros(self.observation_space.shape, dtype=np.float32)
        info = {
            "capital":   curr_portfolio,
            "position":  self.position,
            "step_return": step_return,
        }
        return obs, reward, done, truncated, info

    # ------------------------------------------------------------------
    def _compute_reward(self, step_return: float, portfolio_value: float) -> float:
        """Differential Sharpe ratio reward with drawdown penalty."""

        if self.reward_mode == "pnl":
            return float(step_return * 100)

        returns = np.array(self._returns[-50:], dtype=np.float64)
        if len(returns) < 5:
            return 0.0

        mean_r = np.mean(returns)
        std_r  = np.std(returns) + 1e-9

        if self.reward_mode == "sortino":
            neg = returns[returns < 0]
            downside = np.sqrt(np.mean(neg ** 2)) if len(neg) > 0 else 1e-9
            reward = mean_r / downside
        else:  # sharpe
            reward = mean_r / std_r * np.sqrt(len(returns))

        # Drawdown penalty
        dd = (portfolio_value - self.peak_capital) / (self.peak_capital + 1e-9)
        reward += self.risk_penalty * dd  # dd is negative → penalty

        return float(np.clip(reward, -10, 10))

    # ------------------------------------------------------------------
    def render(self):
        pass


# ───────────────────────────────────────────────────
# Utility: evaluate a trained model on the env
# ───────────────────────────────────────────────────

def backtest_model(model, env: CryptoTradingEnv, n_episodes: int = 5, seed: int = 99):
    """
    Run `n_episodes` full episodes deterministically and collect metrics.
    Returns dict with aggregated performance stats.
    """
    all_returns, all_maxdds, all_capitals = [], [], []

    for ep in range(n_episodes):
        obs, _ = env.reset(seed=seed + ep)
        done, info = False, {}
        episode_returns = []
        init_cap = env.initial_capital

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, truncated, info = env.step(action)
            episode_returns.append(info.get("step_return", 0))

        final_cap = info.get("capital", init_cap)
        total_ret = (final_cap - init_cap) / init_cap
        eq_curve  = np.cumprod(1 + np.array(episode_returns))
        peak      = np.maximum.accumulate(eq_curve)
        dd        = (eq_curve - peak) / peak
        max_dd    = dd.min()
        ret_arr   = np.array(episode_returns)
        sharpe    = (np.mean(ret_arr) / (np.std(ret_arr) + 1e-9)) * np.sqrt(len(ret_arr))

        all_returns.append(total_ret)
        all_maxdds.append(max_dd)
        all_capitals.append(final_cap)

    calmar = np.mean(all_returns) / (abs(np.mean(all_maxdds)) + 1e-9)

    return {
        "mean_return":   np.mean(all_returns),
        "std_return":    np.std(all_returns),
        "mean_max_dd":   np.mean(all_maxdds),
        "calmar":        calmar,
        "mean_final_cap":np.mean(all_capitals),
        "n_episodes":    n_episodes,
    }
