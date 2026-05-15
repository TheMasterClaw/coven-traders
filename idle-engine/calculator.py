"""
idle-engine/calculator.py
Deterministic offline earnings calculator using integer math.

Formula:
    earnings = base_rate * fleet_power * sector_multiplier * boost_multiplier * time_elapsed
All intermediate values use basis points (1 BP = 0.0001) to avoid floating-point drift.
"""

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Dict, List, Tuple

CONFIG_PATH = Path(__file__).with_name("config.yaml")

with open(CONFIG_PATH, "r") as f:
    _CONFIG = yaml.safe_load(f)

_BP = int(_CONFIG["game_balance"]["math"]["basis_points"])  # 10_000
_BASE_RATE = int(_CONFIG["game_balance"]["base_rate_per_power"])
_MAX_OFFLINE = int(_CONFIG["game_balance"]["boosts"]["max_offline_seconds"])


def _clamp(val: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, val))


def calculate_offline_earnings(
    fleet_power: int,
    sector_id: str,
    active_boosts: List[Dict],
    time_elapsed_seconds: int,
) -> Tuple[int, Dict]:
    """
    Compute offline earnings deterministically with integer math.

    Args:
        fleet_power: Total power of the player's fleet.
        sector_id: Key from config.yaml sectors.
        active_boosts: List of boost dicts, each with 'multiplier_bp' and 'type'.
        time_elapsed_seconds: Seconds since last sync (capped at max_offline).

    Returns:
        (earnings, breakdown_dict)
    """
    time_elapsed_seconds = _clamp(time_elapsed_seconds, 0, _MAX_OFFLINE)
    sectors = _CONFIG["game_balance"]["sectors"]
    sector = sectors.get(sector_id, sectors["core_systems"])
    sector_mult_bp = int(sector["yield_multiplier_bp"])

    # Base earnings per second = base_rate * fleet_power
    base_per_sec = _BASE_RATE * fleet_power

    # Apply sector multiplier (divide by BP)
    sector_adjusted = (base_per_sec * sector_mult_bp) // _BP

    # Aggregate boost multipliers multiplicatively
    total_boost_bp = _BP  # 1.0x in basis points
    boost_details = []
    for boost in active_boosts:
        mult = int(boost.get("multiplier_bp", _BP))
        total_boost_bp = (total_boost_bp * mult) // _BP
        boost_details.append({
            "type": boost.get("type", "unknown"),
            "multiplier_bp": mult,
        })

    # Apply boost multiplier
    boosted_per_sec = (sector_adjusted * total_boost_bp) // _BP

    # Total over elapsed time
    total_earnings = boosted_per_sec * time_elapsed_seconds

    breakdown = {
        "fleet_power": fleet_power,
        "sector": sector_id,
        "sector_multiplier_bp": sector_mult_bp,
        "base_per_sec": base_per_sec,
        "sector_adjusted_per_sec": sector_adjusted,
        "boost_multiplier_bp": total_boost_bp,
        "boosted_per_sec": boosted_per_sec,
        "time_elapsed_seconds": time_elapsed_seconds,
        "total_earnings": total_earnings,
        "boosts_applied": boost_details,
    }
    return total_earnings, breakdown


def calculate_tick_earnings(
    fleet_power: int,
    sector_id: str,
    active_boosts: List[Dict],
) -> int:
    """
    Single-tick earnings (per second). Useful for live updates.
    """
    earnings, _ = calculate_offline_earnings(
        fleet_power=fleet_power,
        sector_id=sector_id,
        active_boosts=active_boosts,
        time_elapsed_seconds=1,
    )
    return earnings
