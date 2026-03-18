"""
pro01-neural-repeater/orch_or.py
Penrose-Hameroff Orchestrated Objective Reduction (Orch OR) Formalization
BRNA Layer 1 — Bio-Physical Processing

References:
  - Penrose, R. (1994). Shadows of the Mind. Oxford University Press.
  - Hameroff, S. & Penrose, R. (2014). Consciousness in the Universe.
    Physics of Life Reviews, 11(1), 39-78.

This module formalizes the mathematical foundation for wave function
collapse inside microtubule lattices — the core "processing cycle" of
every neural repeater node in the BRNA network.
"""

import math
import numpy as np

# Physical constants
HBAR        = 1.0545718e-34   # Reduced Planck constant (J·s)
G           = 6.674e-11       # Gravitational constant (m³/kg·s²)
K_BOLTZMANN = 1.380649e-23    # Boltzmann constant (J/K)

# Tubulin dimer physical parameters
TUBULIN_MASS_KG       = 8.0e-23    # ~110 kDa per dimer
TUBULIN_SEPARATION_M  = 4.0e-9     # ~4 nm lattice spacing
MICROTUBULE_DIAMETER  = 25e-9      # 25 nm outer diameter
BODY_TEMP_K           = 310.15     # 37°C in Kelvin


# ---------------------------------------------------------------------------
# 1. Gravitational self-energy — the Penrose threshold
# ---------------------------------------------------------------------------

def gravitational_self_energy(mass_kg: float,
                               separation_m: float = TUBULIN_SEPARATION_M) -> float:
    """
    Compute the gravitational self-energy E_G of a superimposed
    mass distribution — the threshold for Orch OR collapse.

    Penrose formula (simplified):
        E_G = G * m² / a

    where:
        G   = gravitational constant
        m   = mass of superimposed object
        a   = spatial separation of superposition states

    Parameters
    ----------
    mass_kg      : float  Mass of the quantum system (kg)
    separation_m : float  Separation between superposition branches (m)

    Returns
    -------
    float  Gravitational self-energy in Joules
    """
    return G * (mass_kg ** 2) / separation_m


def collapse_time(E_G: float) -> float:
    """
    Time until Orch OR wave function collapse.

    Penrose relation:
        t = ℏ / E_G

    A larger gravitational self-energy → faster collapse.
    A smaller E_G → longer coherence window before OR occurs.

    Parameters
    ----------
    E_G : float  Gravitational self-energy (J)

    Returns
    -------
    float  Collapse time in seconds
    """
    if E_G <= 0:
        raise ValueError("E_G must be positive.")
    return HBAR / E_G


def collapse_time_ms(E_G: float) -> float:
    """Return collapse time in milliseconds."""
    return collapse_time(E_G) * 1000.0


# ---------------------------------------------------------------------------
# 2. Thermal decoherence — the competing mechanism
# ---------------------------------------------------------------------------

def thermal_decoherence_time(mass_kg: float,
                              temperature_k: float = BODY_TEMP_K,
                              separation_m: float = TUBULIN_SEPARATION_M) -> float:
    """
    Estimate thermal decoherence time τ_D from environmental noise.

    Simplified Zurek formula:
        τ_D = ℏ / (mass * v_thermal * separation)
    where v_thermal = sqrt(k_B * T / mass)

    This gives the timescale on which thermal fluctuations at body
    temperature would destroy quantum coherence — the enemy of Orch OR.

    Parameters
    ----------
    mass_kg      : float  Mass (kg)
    temperature_k: float  Temperature (K)
    separation_m : float  Superposition separation (m)

    Returns
    -------
    float  Thermal decoherence time (seconds)
    """
    v_thermal = math.sqrt(K_BOLTZMANN * temperature_k / mass_kg)
    return HBAR / (mass_kg * v_thermal * separation_m)


def coherence_is_viable(E_G: float,
                         mass_kg: float = TUBULIN_MASS_KG,
                         temperature_k: float = BODY_TEMP_K) -> bool:
    """
    Check whether Orch OR collapse can occur before thermal decoherence.
    Returns True if t_OR < τ_D (collapse beats decoherence).
    """
    t_or = collapse_time(E_G)
    t_decohere = thermal_decoherence_time(mass_kg, temperature_k)
    return t_or < t_decohere


# ---------------------------------------------------------------------------
# 3. Metabolic protection factor
# ---------------------------------------------------------------------------

def metabolic_cooling_factor(atp_level_pct: float) -> float:
    """
    Biological micro-environment protection factor.

    Hameroff's proposal: tubulin dipoles inside microtubules are partially
    shielded from thermal noise by ordered water (Fröhlich condensate) and
    metabolic energy (ATP hydrolysis). Higher ATP → better shielding.

    Modeled as a linear multiplier on coherence window:
        factor = 1.0 + (ATP% / 100) * 1.5

    Range: 1.0 (ATP=0%, no shielding) to 2.5 (ATP=100%, full shielding)

    Parameters
    ----------
    atp_level_pct : float  ATP energy level as percentage (0–100)

    Returns
    -------
    float  Multiplier applied to effective coherence time
    """
    clamped = max(0.0, min(100.0, atp_level_pct))
    return 1.0 + (clamped / 100.0) * 1.5


def effective_coherence_window(E_G: float, atp_level_pct: float) -> float:
    """
    Compute the biologically-protected coherence window.

    t_effective = t_OR * metabolic_cooling_factor(ATP)

    This is the actual time window the BRNA node has to maintain its
    qubit before Orch OR collapse — the key Week 1 metric (>100ms target).

    Parameters
    ----------
    E_G           : float  Gravitational self-energy (J)
    atp_level_pct : float  ATP level (%)

    Returns
    -------
    float  Effective coherence window in seconds
    """
    return collapse_time(E_G) * metabolic_cooling_factor(atp_level_pct)


# ---------------------------------------------------------------------------
# 4. Network-level OR statistics
# ---------------------------------------------------------------------------

def or_rate_per_second(coherence_time_s: float) -> float:
    """
    Estimated Orch OR events per second for a single node.
    Each OR event = one 'processing cycle' = one qubit collapse.
    """
    return 1.0 / coherence_time_s if coherence_time_s > 0 else 0.0


def network_or_bandwidth(num_nodes: int, coherence_time_s: float) -> float:
    """
    Total network OR bandwidth: how many collapse events per second
    across all nodes — analogous to network throughput in classical terms.

    Parameters
    ----------
    num_nodes       : int    Number of active neural repeater nodes
    coherence_time_s: float  Average coherence time per node (s)

    Returns
    -------
    float  Total OR events per second (network-wide)
    """
    return num_nodes * or_rate_per_second(coherence_time_s)


def resonance_fidelity(coherence_time_ms: float,
                        target_ms: float = 100.0,
                        atp_pct: float = 100.0) -> float:
    """
    Compute resonance fidelity F_R for a node — the key quality metric
    used by the BRR routing layer to select optimal paths.

    F_R = min(1.0, coherence_time / target) * (ATP / 100)

    Range: 0.0 (dead node) to 1.0 (perfect node)

    Parameters
    ----------
    coherence_time_ms : float  Actual coherence time (ms)
    target_ms         : float  Required minimum coherence time (ms)
    atp_pct           : float  ATP level (%)

    Returns
    -------
    float  Fidelity score 0.0–1.0
    """
    coherence_score = min(1.0, coherence_time_ms / target_ms)
    metabolic_score = atp_pct / 100.0
    return round(coherence_score * metabolic_score, 4)


# ---------------------------------------------------------------------------
# 5. Main demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("BRNA — Orch OR Formalization Module")
    print("=" * 60)

    m = TUBULIN_MASS_KG
    sep = TUBULIN_SEPARATION_M

    E_G = gravitational_self_energy(m, sep)
    t_base = collapse_time(E_G)
    t_thermal = thermal_decoherence_time(m, BODY_TEMP_K, sep)

    print(f"\n--- Single tubulin dimer ---")
    print(f"Mass:              {m:.2e} kg")
    print(f"Separation:        {sep:.2e} m")
    print(f"E_G:               {E_G:.4e} J")
    print(f"Base collapse time:{t_base:.4e} s")
    print(f"Thermal decohere:  {t_thermal:.4e} s")
    print(f"Orch OR viable:    {coherence_is_viable(E_G)}")

    print(f"\n--- Metabolic protection at different ATP levels ---")
    for atp in [20, 50, 75, 85, 100]:
        t_eff = effective_coherence_window(E_G, atp)
        fid = resonance_fidelity(t_eff * 1000, target_ms=100.0, atp_pct=atp)
        print(f"  ATP={atp:3d}%  t_eff={t_eff:.4e}s  F_R={fid:.4f}")

    print(f"\n--- Network OR bandwidth (4 nodes, 100ms coherence) ---")
    bw = network_or_bandwidth(num_nodes=4, coherence_time_s=0.1)
    print(f"  Total OR events/sec: {bw:.1f}")
    print(f"  Classical equivalent: {bw * 2:.0f} bits/sec (superdense coding)")
