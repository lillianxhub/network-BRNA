# pro04-resonance-protocol
## BRNA Layers 3-5 — QSP, Spin Bridge, HITL, Dashboard

**Status:** Conceptual Architecture  
**TRL:** 2-3 (Technology formulation, simulation implemented)  
**Packet Tracer devices:** HITL-GW, Monitor-1, Monitor-2 (10.0.3.x), QNodes (10.0.4.x)

---

## What this module does

This module implements the upper layers of the BRNA stack — everything from the quantum-digital translation point up to the human operator interface:

- **L3 QSP:** Intent-focused messaging using phase synchronization instead of TCP SYN/ACK
- **L4 SpinBridge:** Converts collapsed qubit spin states into classical UTF-8/JSON data
- **L5 HITL:** Human-in-the-Loop gateway enforcing the Paradox Prevention Protocol (PPP)
- **L5 Dashboard:** Live fidelity monitoring across all 14 nodes

---

## Files

| File | Layer | Purpose |
|------|-------|---------|
| `qsp_protocol.py` | L3–L5 | QSP frame structure + resonance handshake |
| `spin_bridge.py` | L4 | SpinToBit(), superdense coding, fidelity-aware decode |
| `hitl_gateway.py` | L5 | PPP entropy filter, human override, audit log |
| `dashboard.py` | L5 | Live terminal dashboard (rich UI, 14-node telemetry) |

---

## QSP vs TCP — key differences

| Property | TCP | QSP |
|----------|-----|-----|
| Handshake | SYN → SYN-ACK → ACK (3 messages) | RESONATE → PHASE-SYNC → ENTANGLE (phase match) |
| Delivery guarantee | Lossless (retransmit) | Resonance-based (intent-focused) |
| Addressing | IP + port | Entanglement Pair ID |
| Integrity | CRC32 / checksum | DNA checksum (SHA-256) |
| Causality | Sequential | PPP entropy guardrail |

---

## QSP Frame structure

```
+------------------+----------------+------------------+----------+
| ResonanceID      | PhaseState     | DNAChecksum      | Payload  |
| 16 bytes         | 4 bytes        | 32 bytes         | variable |
+------------------+----------------+------------------+----------+
```

```python
from qsp_protocol import QSPFrame, QSPHandshake

hs = QSPHandshake("NR-A", "NR-B")
pair_id = hs.run()               # RESONATE → PHASE-SYNC → ENTANGLE

frame = QSPFrame(
    source="NR-A", destination="NR-B",
    payload=b"Hello World — spin state |1>",
    phase_state=hs.phase_a, atp_level=87.5
)
```

---

## SpinToBit — superdense coding

```python
from spin_bridge import encode_for_transmission, bridge_pipeline

spins  = encode_for_transmission("Hi BRNA!")  # text → spin list
result = bridge_pipeline(spins, output_format="utf8")
# result["data"] == "Hi BRNA!"

# Bandwidth: 1 qubit → 2 classical bits (superdense coding)
# 8 qubits → 1 byte
```

---

## HITL + PPP

```python
from hitl_gateway import HITLGateway
from qsp_protocol import QSPFrame

gw = HITLGateway()
frame = QSPFrame("NR-A", "NR-B", b"Normal packet", phase_state=1.2)
approved = gw.ppp_filter(frame)   # True = forward, False = drop

gw.human_override(frame.resonance_id, approve=True)  # manual operator decision
gw.print_audit_log()
```

**PPP rule:** if `entropy_delta < -0.15` → packet dropped (causality violation risk)

---

## Dashboard

```bash
python dashboard.py                    # live 30-second refresh
python dashboard.py --static           # single snapshot
python dashboard.py --export           # save JSON to dashboard_snapshot.json
python dashboard.py --seconds 60       # run for 60 seconds
```

---

## How to run all modules

```bash
pip install rich qiskit qiskit-aer networkx

python qsp_protocol.py     # Week 2: Hello World spin state handshake
python spin_bridge.py      # Week 4: SpinToBit encoding/decoding pipeline
python hitl_gateway.py     # Week 4: PPP filter + HITL audit log
python dashboard.py        # Week 4: Live 14-node fidelity dashboard
```
