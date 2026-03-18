"""
pro04-resonance-protocol/hitl_gateway.py
BRNA Layer 5 — Human-in-the-Loop (HITL) Gateway
Implements the Paradox Prevention Protocol (PPP).
Drops causality-violating packets. Logs ethics events.
"""

import time
import json
from qsp_protocol import QSPFrame

PPP_ENTROPY_THRESHOLD = 0.15   # Max allowed entropy decrease


class HITLGateway:
    """
    Human-in-the-loop oversight node.
    Implements PPP (Paradox Prevention Protocol):
    - Drops packets that decrease local entropy beyond threshold
    - Flags ethics violations
    - Logs all decisions for audit
    """

    def __init__(self, node_id: str = "HITL-GW"):
        self.node_id = node_id
        self.audit_log = []
        self.approved = 0
        self.dropped = 0

    def entropy_check(self, frame: QSPFrame) -> float:
        """
        Estimate entropy change the packet would cause.
        Simplified: based on payload size and phase state delta.
        """
        payload_entropy = len(set(frame.payload)) / max(len(frame.payload), 1)
        phase_delta = abs(frame.phase_state) / (2 * 3.14159)
        return payload_entropy - phase_delta

    def ppp_filter(self, frame: QSPFrame) -> bool:
        """
        Paradox Prevention Protocol:
        Returns True if packet is safe to forward, False if dropped.
        """
        delta = self.entropy_check(frame)
        safe = delta >= -PPP_ENTROPY_THRESHOLD

        event = {
            "timestamp": time.time(),
            "resonance_id": frame.resonance_id,
            "source": frame.source,
            "destination": frame.destination,
            "entropy_delta": round(delta, 4),
            "decision": "APPROVED" if safe else "DROPPED (PPP)",
        }
        self.audit_log.append(event)

        if safe:
            self.approved += 1
            print(f"[HITL] APPROVED  rid={frame.resonance_id}  entropy_delta={delta:.4f}")
        else:
            self.dropped += 1
            print(f"[HITL] DROPPED   rid={frame.resonance_id}  entropy_delta={delta:.4f}  — causality violation")

        return safe

    def human_override(self, resonance_id: str, approve: bool):
        """Manual human operator override for flagged packets."""
        action = "HUMAN-APPROVED" if approve else "HUMAN-BLOCKED"
        self.audit_log.append({
            "timestamp": time.time(),
            "resonance_id": resonance_id,
            "decision": action,
            "source": "human-operator",
        })
        print(f"[HITL] {action} by human operator  rid={resonance_id}")

    def print_audit_log(self):
        print(f"\n[HITL] Audit log ({len(self.audit_log)} events):")
        print(f"  Approved: {self.approved} | Dropped: {self.dropped}")
        for entry in self.audit_log[-5:]:
            print(f"  {entry}")


if __name__ == "__main__":
    print("=== BRNA HITL Gateway + PPP ===\n")
    gw = HITLGateway()

    frame_ok = QSPFrame("NR-A", "NR-B", b"Normal data packet", phase_state=1.2, atp_level=90.0)
    frame_bad = QSPFrame("QNode-A", "QNode-D", b"X" * 5, phase_state=6.0, atp_level=10.0)

    gw.ppp_filter(frame_ok)
    gw.ppp_filter(frame_bad)
    gw.human_override(frame_bad.resonance_id, approve=False)
    gw.print_audit_log()
