"""
pro04-resonance-protocol/qsp_protocol.py
BRNA Layer 3-5 — Quantum Sensory Protocol (QSP)
Intent-focused messaging using phase synchronization.
Unlike TCP, QSP prioritizes resonance over guaranteed delivery.
"""

import hashlib
import time
import uuid

QSP_VERSION = "1.0"


class QSPFrame:
    """
    QSP Frame Structure:
    [ ResonanceID | EntanglementPairID | BiologicalMetabolism | Payload ]
    """

    def __init__(self, source: str, destination: str,
                 payload: bytes, phase_state: float = 0.0, atp_level: float = 100.0):
        self.resonance_id = uuid.uuid4().hex[:16].upper()
        self.entanglement_pair_id = self._derive_pair_id(source, destination)
        self.source = source
        self.destination = destination
        self.phase_state = phase_state        # Quantum phase of transmitting node
        self.atp_level = atp_level            # Biological metabolism indicator
        self.payload = payload
        self.dna_checksum = self._dna_checksum(payload)
        self.timestamp = time.time()

    def _derive_pair_id(self, src: str, dst: str) -> str:
        combined = "".join(sorted([src, dst]))
        return hashlib.sha256(combined.encode()).hexdigest()[:16].upper()

    def _dna_checksum(self, data: bytes) -> str:
        """32-byte biological integrity checksum."""
        return hashlib.sha256(data).hexdigest()

    def to_dict(self) -> dict:
        return {
            "qsp_version": QSP_VERSION,
            "resonance_id": self.resonance_id,
            "entanglement_pair_id": self.entanglement_pair_id,
            "source": self.source,
            "destination": self.destination,
            "phase_state": self.phase_state,
            "atp_level": self.atp_level,
            "dna_checksum": self.dna_checksum,
            "payload_length": len(self.payload),
            "payload": self.payload.decode(errors="replace"),
        }

    def __repr__(self):
        return (f"QSPFrame(rid={self.resonance_id}, "
                f"{self.source}→{self.destination}, "
                f"phase={self.phase_state:.3f}, payload={len(self.payload)}B)")


class QSPHandshake:
    """
    QSP Resonance Handshake — replaces TCP 3-way handshake.
    Uses phase synchronization instead of SYN/ACK.
    Steps: RESONATE → PHASE-SYNC → ENTANGLE → DATA
    """

    def __init__(self, node_a: str, node_b: str):
        self.node_a = node_a
        self.node_b = node_b
        self.phase_a = 0.0
        self.phase_b = 0.0
        self.synchronized = False

    def resonate(self) -> float:
        """Step 1: Node A broadcasts its phase."""
        import random
        self.phase_a = random.uniform(0, 2 * 3.14159)
        print(f"[QSP] RESONATE: {self.node_a} broadcasts phase={self.phase_a:.4f} rad")
        return self.phase_a

    def phase_sync(self, received_phase: float, tolerance: float = 0.5) -> bool:
        """Step 2: Node B synchronizes to Node A's phase."""
        import random
        self.phase_b = received_phase + random.uniform(-0.1, 0.1)
        diff = abs(self.phase_a - self.phase_b)
        self.synchronized = diff < tolerance
        print(f"[QSP] PHASE-SYNC: {self.node_b} phase={self.phase_b:.4f} rad  diff={diff:.4f}  sync={'OK' if self.synchronized else 'FAIL'}")
        return self.synchronized

    def entangle(self) -> str:
        """Step 3: Establish entanglement pair ID."""
        if not self.synchronized:
            raise RuntimeError("Cannot entangle: phases not synchronized.")
        pair_id = hashlib.sha256(f"{self.node_a}{self.node_b}{self.phase_a:.4f}".encode()).hexdigest()[:16].upper()
        print(f"[QSP] ENTANGLE: Pair established  PairID={pair_id}")
        return pair_id

    def run(self) -> str:
        """Run full QSP handshake. Returns entanglement pair ID."""
        print(f"\n[QSP] Handshake: {self.node_a} ↔ {self.node_b}")
        phase = self.resonate()
        sync = self.phase_sync(phase)
        if sync:
            return self.entangle()
        raise RuntimeError(f"QSP handshake failed between {self.node_a} and {self.node_b}")


if __name__ == "__main__":
    print("=== BRNA Week 2: QSP Protocol ===\n")

    handshake = QSPHandshake("NR-A", "NR-B")
    pair_id = handshake.run()

    print(f"\n--- Sending Hello World spin state ---")
    frame = QSPFrame(
        source="NR-A",
        destination="NR-B",
        payload=b"Hello World - spin state |1>",
        phase_state=handshake.phase_a,
        atp_level=87.5,
    )
    print(f"Frame created: {frame}")
    import json
    print(json.dumps(frame.to_dict(), indent=2))
