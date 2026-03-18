"""
tests/test_microtubule.py
Unit tests for pro01-neural-repeater/microtubule.py and orch_or.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pro01-neural-repeater'))

import pytest
from microtubule import MicrotubuleBundle, COHERENCE_TARGET_MS, HBAR, THERMAL_WINDOW
from orch_or import (
    gravitational_self_energy, collapse_time, metabolic_cooling_factor,
    thermal_decoherence_time, coherence_is_viable, effective_coherence_window,
    resonance_fidelity, network_or_bandwidth, or_rate_per_second,
    TUBULIN_MASS_KG, TUBULIN_SEPARATION_M, BODY_TEMP_K
)


class TestMicrotubuleBundle:

    def test_node_creation_valid_temp(self):
        node = MicrotubuleBundle("NR-A", temperature=37.0)
        assert node.node_id == "NR-A"
        assert node.temperature == 37.0
        assert node.metabolic_atp == 100.0
        assert node.is_coherent is False

    def test_thermal_window_lower_bound(self):
        with pytest.raises(EnvironmentError, match="thermal window"):
            MicrotubuleBundle("NR-BAD", temperature=35.9)

    def test_thermal_window_upper_bound(self):
        with pytest.raises(EnvironmentError, match="thermal window"):
            MicrotubuleBundle("NR-BAD", temperature=39.1)

    def test_thermal_window_edge_lower(self):
        node = MicrotubuleBundle("NR-EDGE", temperature=36.0)
        assert node.temperature == 36.0

    def test_thermal_window_edge_upper(self):
        node = MicrotubuleBundle("NR-EDGE", temperature=39.0)
        assert node.temperature == 39.0

    def test_initialize_qubit_sets_coherent(self):
        node = MicrotubuleBundle("NR-A", temperature=37.0)
        qc = node.initialize_qubit()
        assert node.is_coherent is True
        assert qc is not None

    def test_hold_coherence_target(self):
        node = MicrotubuleBundle("NR-A", temperature=37.0)
        node.initialize_qubit()
        result = node.hold_coherence(duration_ms=100.0)
        assert result is True
        assert node.coherence_time_ms == 100.0
        assert node.coherence_time_ms >= COHERENCE_TARGET_MS

    def test_hold_coherence_atp_drain(self):
        node = MicrotubuleBundle("NR-A", temperature=37.0)
        node.initialize_qubit()
        initial_atp = node.metabolic_atp
        node.hold_coherence(duration_ms=100.0)
        assert node.metabolic_atp < initial_atp

    def test_low_atp_causes_decoherence(self):
        node = MicrotubuleBundle("NR-A", temperature=37.0)
        node.initialize_qubit()
        node.metabolic_atp = 15.0   # below 20% threshold
        result = node.hold_coherence(duration_ms=10.0)
        assert result is False
        assert node.is_coherent is False

    def test_objective_reduction_returns_valid_spin(self):
        node = MicrotubuleBundle("NR-A", temperature=37.0)
        qc = node.initialize_qubit()
        spin = node.objective_reduction(qc)
        assert spin in (0, 1)

    def test_objective_reduction_clears_coherent_flag(self):
        node = MicrotubuleBundle("NR-A", temperature=37.0)
        qc = node.initialize_qubit()
        assert node.is_coherent is True
        node.objective_reduction(qc)
        assert node.is_coherent is False

    def test_resonance_cost_positive(self):
        node = MicrotubuleBundle("NR-A", temperature=37.0)
        node.initialize_qubit()
        node.hold_coherence(100.0)
        cost = node.get_resonance_cost()
        assert cost > 0

    def test_resonance_cost_lower_with_better_coherence(self):
        node_a = MicrotubuleBundle("NR-A", temperature=37.0)
        node_b = MicrotubuleBundle("NR-B", temperature=37.0)
        node_a.initialize_qubit()
        node_b.initialize_qubit()
        node_a.hold_coherence(200.0)  # longer coherence
        node_b.hold_coherence(50.0)
        assert node_a.get_resonance_cost() < node_b.get_resonance_cost()

    def test_status_dict_keys(self):
        node = MicrotubuleBundle("NR-A", temperature=37.0)
        s = node.status()
        for key in ["node_id", "temperature", "coherent", "spin_state",
                    "coherence_ms", "atp_level", "resonance_cost"]:
            assert key in s

    def test_week1_pass_criterion(self):
        """Week 1 definition of done: qubit holds >100ms."""
        node = MicrotubuleBundle("NR-A", temperature=37.0)
        qc = node.initialize_qubit()
        node.hold_coherence(duration_ms=100.0)
        node.objective_reduction(qc)
        assert node.coherence_time_ms >= COHERENCE_TARGET_MS, \
            f"Week 1 FAIL: coherence={node.coherence_time_ms}ms < {COHERENCE_TARGET_MS}ms target"


class TestOrchOR:

    def test_gravitational_self_energy_positive(self):
        E_G = gravitational_self_energy(TUBULIN_MASS_KG, TUBULIN_SEPARATION_M)
        assert E_G > 0

    def test_collapse_time_positive(self):
        E_G = gravitational_self_energy(TUBULIN_MASS_KG)
        t = collapse_time(E_G)
        assert t > 0

    def test_collapse_time_zero_energy_raises(self):
        with pytest.raises(ValueError):
            collapse_time(0.0)

    def test_metabolic_cooling_factor_range(self):
        assert metabolic_cooling_factor(0)   == pytest.approx(1.0)
        assert metabolic_cooling_factor(100) == pytest.approx(2.5)

    def test_metabolic_cooling_factor_clamped(self):
        assert metabolic_cooling_factor(-10) == pytest.approx(1.0)
        assert metabolic_cooling_factor(150) == pytest.approx(2.5)

    def test_effective_window_greater_than_base(self):
        E_G  = gravitational_self_energy(TUBULIN_MASS_KG)
        t_base = collapse_time(E_G)
        t_eff  = effective_coherence_window(E_G, atp_level_pct=80.0)
        assert t_eff > t_base

    def test_resonance_fidelity_perfect_node(self):
        f = resonance_fidelity(coherence_time_ms=100.0, target_ms=100.0, atp_pct=100.0)
        assert f == pytest.approx(1.0)

    def test_resonance_fidelity_dead_node(self):
        f = resonance_fidelity(coherence_time_ms=0.0, target_ms=100.0, atp_pct=0.0)
        assert f == pytest.approx(0.0)

    def test_resonance_fidelity_partial(self):
        f = resonance_fidelity(coherence_time_ms=50.0, target_ms=100.0, atp_pct=80.0)
        assert 0 < f < 1

    def test_network_or_bandwidth(self):
        bw = network_or_bandwidth(num_nodes=4, coherence_time_s=0.1)
        assert bw == pytest.approx(40.0)

    def test_thermal_decoherence_positive(self):
        t = thermal_decoherence_time(TUBULIN_MASS_KG, BODY_TEMP_K, TUBULIN_SEPARATION_M)
        assert t > 0
