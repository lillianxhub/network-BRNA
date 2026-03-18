"""
pro01-neural-repeater/microtubule.py
BRNA Layer 1 — Bio-Physical Processing
MicrotubuleBundle: the primary living processor node.
Simulates a quantum-coherent microtubule lattice using Qiskit.
"""

import time
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

HBAR = 1.0545718e-34          # Reduced Planck constant (J·s)
THERMAL_WINDOW = (36.0, 39.0) # Valid operating temp in Celsius
COHERENCE_TARGET_MS = 100     # Target qubit hold time in milliseconds


class MicrotubuleBundle:
    """
    Represents a single biological neural repeater node.
    Each bundle holds one logical qubit via tubulin dipole superposition.
    Collapses via Orchestrated Objective Reduction (Orch OR).
    """

    def __init__(self, node_id: str, temperature: float = 37.0):
        self.node_id = node_id
        self.temperature = temperature
        self.coherence_time_ms = 0.0
        self.is_coherent = False
        self.spin_state = None
        self.metabolic_atp = 100.0    # ATP energy level (0-100%)
        self.simulator = AerSimulator()
        self._validate_thermal_window()

    def _validate_thermal_window(self):
        lo, hi = THERMAL_WINDOW
        if not (lo <= self.temperature <= hi):
            raise EnvironmentError(
                f"Node {self.node_id}: temperature {self.temperature}C "
                f"outside thermal window {THERMAL_WINDOW}. Decoherence risk."
            )

    def initialize_qubit(self) -> QuantumCircuit:
        """Place tubulin dipole into superposition — the start of Orch OR cycle."""
        qc = QuantumCircuit(1, 1)
        qc.h(0)   # Hadamard: |0> → |+> superposition
        self.is_coherent = True
        print(f"[{self.node_id}] Qubit initialized in superposition.")
        return qc

    def objective_reduction(self, qc: QuantumCircuit, gravitational_energy: float = None) -> int:
        """
        Trigger Orchestrated Objective Reduction (Orch OR).
        Wave function collapses per Penrose-Hameroff: E_G = hbar / t
        Returns the collapsed spin state: 0 or 1.
        """
        if gravitational_energy is None:
            t = 0.1  # 100ms default coherence window
            gravitational_energy = HBAR / t

        qc.measure(0, 0)
        job = self.simulator.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        self.spin_state = int(list(counts.keys())[0])
        self.is_coherent = False
        print(f"[{self.node_id}] Orch OR triggered → spin state: |{self.spin_state}>  E_G={gravitational_energy:.2e} J")
        return self.spin_state

    def hold_coherence(self, duration_ms: float = 100.0) -> bool:
        """
        Simulate holding the qubit for a given duration.
        ATP must be above 20% for coherence to survive.
        """
        self.metabolic_atp -= duration_ms * 0.005   # ATP drain per ms
        if self.metabolic_atp < 20.0:
            print(f"[{self.node_id}] WARNING: Low ATP ({self.metabolic_atp:.1f}%). Metabolic decoherence risk.")
            self.is_coherent = False
            return False
        time.sleep(duration_ms / 1000.0)
        self.coherence_time_ms = duration_ms
        print(f"[{self.node_id}] Held coherence for {duration_ms}ms. ATP: {self.metabolic_atp:.1f}%")
        return True

    def get_resonance_cost(self) -> float:
        """
        Compute resonance cost C_R for routing layer.
        C_R = 1/CoherenceTime + MetabolicOverhead
        """
        coherence = self.coherence_time_ms if self.coherence_time_ms > 0 else 0.001
        metabolic_overhead = (100.0 - self.metabolic_atp) / 100.0
        return (1.0 / coherence) + metabolic_overhead

    def status(self) -> dict:
        return {
            "node_id": self.node_id,
            "temperature": self.temperature,
            "coherent": self.is_coherent,
            "spin_state": self.spin_state,
            "coherence_ms": self.coherence_time_ms,
            "atp_level": self.metabolic_atp,
            "resonance_cost": self.get_resonance_cost(),
        }


if __name__ == "__main__":
    print("=== BRNA Week 1: MicrotubuleBundle Simulation ===\n")
    node = MicrotubuleBundle(node_id="NR-A", temperature=37.2)
    qc = node.initialize_qubit()
    node.hold_coherence(duration_ms=100.0)
    spin = node.objective_reduction(qc)
    print(f"\nNode status: {node.status()}")
    print(f"\nWeek 1 check: coherence held >100ms = {node.coherence_time_ms >= COHERENCE_TARGET_MS}")
