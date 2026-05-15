"""
idle-engine/progression.py
Level / XP system with deterministic integer math.

Level curve: exponential, each level requires 1.5x previous.
XP = sum of earnings, discoveries, battles.
"""

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Tuple, Dict

CONFIG_PATH = Path(__file__).with_name("config.yaml")
with open(CONFIG_PATH, "r") as f:
    _CONFIG = yaml.safe_load(f)

_PROG = _CONFIG["game_balance"]["progression"]
_BP = int(_CONFIG["game_balance"]["math"]["basis_points"])

_BASE_XP = int(_PROG["base_xp_for_level_2"])
_NUM = int(_PROG["level_multiplier_num"])   # 3
_DEN = int(_PROG["level_multiplier_den"])   # 2
_MAX_LEVEL = int(_PROG["max_level"])

_XP_TRADE_BP = int(_PROG["xp_from_trade_bp"])
_XP_DISCOVERY = int(_PROG["xp_from_discovery"])
_XP_BATTLE_WIN = int(_PROG["xp_from_battle_win"])
_XP_BATTLE_LOSS = int(_PROG["xp_from_battle_loss"])

_SLOTS_PER_LEVEL = int(_PROG["command_center_slots_per_level"])
_BASE_SLOTS = int(_PROG["base_drone_slots"])
_TECH_PER_LEVEL = int(_PROG["tech_points_per_level"])


def xp_required_for_level(level: int) -> int:
    """
    XP needed to reach `level` from level-1.
    level 1 -> 0 XP
    level 2 -> base_xp
    level 3 -> base_xp * 3/2
    level N -> base_xp * (3/2)^(N-2)
    """
    if level <= 1:
        return 0
    # Use integer math: multiply by 3^(level-2), divide by 2^(level-2)
    xp = _BASE_XP
    for _ in range(level - 2):
        xp = (xp * _NUM) // _DEN
    return xp


def total_xp_for_level(target_level: int) -> int:
    """Cumulative XP required to reach target_level."""
    if target_level <= 1:
        return 0
    total = 0
    for lvl in range(2, target_level + 1):
        total += xp_required_for_level(lvl)
    return total


def level_from_xp(current_xp: int) -> int:
    """Binary search for level given total XP."""
    lo, hi = 1, _MAX_LEVEL
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if total_xp_for_level(mid) <= current_xp:
            lo = mid
        else:
            hi = mid - 1
    return lo


def add_xp(
    current_xp: int,
    current_level: int,
    trade_earnings: int = 0,
    discovery: bool = False,
    battle_win: bool = False,
    battle_loss: bool = False,
) -> Tuple[int, int, int, Dict]:
    """
    Apply XP gains and check for level-ups.

    Returns:
        (new_xp, new_level, levels_gained, breakdown)
    """
    gained = 0
    breakdown = {
        "trade_xp": 0,
        "discovery_xp": 0,
        "battle_win_xp": 0,
        "battle_loss_xp": 0,
    }

    if trade_earnings > 0:
        trade_xp = (trade_earnings * _XP_TRADE_BP) // _BP
        gained += trade_xp
        breakdown["trade_xp"] = trade_xp

    if discovery:
        gained += _XP_DISCOVERY
        breakdown["discovery_xp"] = _XP_DISCOVERY

    if battle_win:
        gained += _XP_BATTLE_WIN
        breakdown["battle_win_xp"] = _XP_BATTLE_WIN

    if battle_loss:
        gained += _XP_BATTLE_LOSS
        breakdown["battle_loss_xp"] = _XP_BATTLE_LOSS

    new_xp = current_xp + gained
    new_level = level_from_xp(new_xp)
    levels_gained = new_level - current_level

    breakdown["total_gained"] = gained
    breakdown["previous_level"] = current_level
    breakdown["new_level"] = new_level

    return new_xp, new_level, levels_gained, breakdown


def drone_slots_for_level(level: int) -> int:
    """Command center provides extra slots per level."""
    return _BASE_SLOTS + (level - 1) * _SLOTS_PER_LEVEL


def tech_points_for_level(level: int) -> int:
    """Tech points awarded cumulatively up to level."""
    return (level - 1) * _TECH_PER_LEVEL


def get_level_rewards(levels_gained: int, old_level: int) -> Dict:
    """Return rewards granted from level-ups."""
    rewards = {
        "drone_slots": 0,
        "tech_points": 0,
    }
    for _ in range(levels_gained):
        rewards["drone_slots"] += _SLOTS_PER_LEVEL
        rewards["tech_points"] += _TECH_PER_LEVEL
    return rewards
