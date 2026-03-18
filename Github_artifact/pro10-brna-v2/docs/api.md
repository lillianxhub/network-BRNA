# QSP Protocol API Documentation
## BRNA — Bio-Resonance Network Architecture

---

## Overview

The BRNA API spans Layers 3–5 of the bio-quantum stack. All inter-node communication uses the Quantum Sensory Protocol (QSP) rather than TCP/IP. This document describes every public class, method, and data structure.

---

## Module: qsp_protocol.py

### Class: `QSPFrame`

The fundamental unit of BRNA communication — analogous to a TCP packet but intent-focused.

**Constructor:**
```python
QSPFrame(source, destination, payload, phase_state=0.0, atp_level=100.0)
```

**Fields:**

| Field | Type | Size | Description |
|-------|------|------|-------------|
| `resonance_id` | str | 16 chars (64-bit hex) | Unique per-frame identifier |
| `entanglement_pair_id` | str | 16 chars | Deterministic ID for the source-destination pair |
| `source` | str | variable | Sending node ID (e.g. "NR-A") |
| `destination` | str | variable | Receiving node ID |
| `phase_state` | float | 4 bytes | Quantum phase of transmitting node (radians) |
| `atp_level` | float | 4 bytes | Biological metabolism level (0–100%) |
| `dna_checksum` | str | 64 chars (SHA-256) | Biological integrity verification |
| `payload` | bytes | variable | Data content — neural state or digital command |
| `timestamp` | float | 8 bytes | Unix timestamp of frame creation |

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `to_dict()` | dict | Serialize frame to dictionary |

**Example:**
```python
frame = QSPFrame(
    source="NR-A",
    destination="NR-B",
    payload=b"spin state |1>",
    phase_state=2.18,
    atp_level=87.5
)
print(frame.resonance_id)         # "A3F2B901CD456E78"
print(frame.entanglement_pair_id) # same for NR-A↔NR-B in any direction
print(frame.dna_checksum)         # SHA-256 of payload
```

---

### Class: `QSPHandshake`

Establishes a resonance-synchronized channel between two nodes.
Replaces TCP 3-way handshake with phase synchronization.

**Constructor:**
```python
QSPHandshake(node_a: str, node_b: str)
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `resonate()` | float | Step 1: Node A broadcasts random phase (0–2π) |
| `phase_sync(received_phase, tolerance=0.5)` | bool | Step 2: Node B syncs to A's phase within tolerance |
| `entangle()` | str | Step 3: Generate shared entanglement pair ID |
| `run()` | str | Execute all 3 steps; returns pair ID or raises RuntimeError |

**Example:**
```python
hs = QSPHandshake("NR-A", "NR-B")
pair_id = hs.run()
# [QSP] RESONATE: NR-A broadcasts phase=2.1847 rad
# [QSP] PHASE-SYNC: NR-B phase=2.1923 rad  diff=0.0076  sync=OK
# [QSP] ENTANGLE: Pair established  PairID=A3F2B901CD456E78
```

---

## Module: spin_bridge.py

### `spin_to_bit(spin_state) → int`
Map a single qubit measurement to a classical bit. `|0⟩ → 0`, `|1⟩ → 1`.

### `spins_to_bytes(spin_list, pad_to_byte=True) → bytes`
Pack a list of spin measurements into bytes (MSB first, 8 spins per byte).

### `bytes_to_spins(data) → list[int]`
Inverse: unpack bytes into spin list for injection into the quantum layer.

### `superdense_encode(bit_pair) → str`
Encode 2 classical bits as a quantum gate: `(0,0)→'I'`, `(0,1)→'X'`, `(1,0)→'Z'`, `(1,1)→'XZ'`.

### `superdense_decode(gate, measured_pair) → tuple`
Decode gate back to 2 classical bits.

### `bridge_pipeline(spin_states, output_format='utf8') → dict`
Full L4 pipeline. Returns:
```python
{
    "input_spins": 64,
    "output_bytes": 8,
    "superdense_bits": 128,
    "checksum": "a3f2b901cd45",
    "format": "utf8",
    "data": "Hi BRNA!",
    "error": None
}
```

### `encode_for_transmission(text) → list[int]`
Encode UTF-8 text → spin list (reverse pipeline for injection).

### `decode_with_fidelity_check(spin_states, threshold=0.7) → str | None`
Decode only if estimated signal fidelity exceeds threshold. Returns None if too noisy.

---

## Module: hitl_gateway.py

### Class: `HITLGateway`

**Constructor:** `HITLGateway(node_id="HITL-GW")`

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `entropy_check(frame)` | float | Compute entropy delta for the frame |
| `ppp_filter(frame)` | bool | True = forward, False = drop (PPP) |
| `human_override(resonance_id, approve)` | None | Log manual operator decision |
| `print_audit_log()` | None | Print last 5 audit events |

**PPP entropy rule:**
```
entropy_delta = payload_entropy - phase_delta
if entropy_delta < -0.15:  DROP
else:                       FORWARD
```

**Audit log entry format:**
```python
{
    "timestamp": 1742198400.0,
    "resonance_id": "A3F2B901CD456E78",
    "source": "NR-A",
    "destination": "NR-B",
    "entropy_delta": 0.3821,
    "decision": "APPROVED"   # or "DROPPED (PPP)" or "HUMAN-APPROVED"
}
```

---

## Module: dashboard.py

### CLI flags

| Flag | Default | Description |
|------|---------|-------------|
| `--static` | False | Single snapshot, no live refresh |
| `--export` | False | Save JSON to `dashboard_snapshot.json` |
| `--seconds N` | 30 | Live dashboard duration |

### Programmatic use

```python
from dashboard import NetworkDashboard

dash = NetworkDashboard()
readings = dash.poll_all()         # list of 14 node telemetry dicts
stats    = dash.summary_stats(readings)
# stats["avg_fidelity"], stats["nodes_ok"], stats["drop_rate_pct"] etc.
```

### Node telemetry dict schema

```python
{
    "node_id":         "NR-A",
    "ip":              "10.0.1.1",
    "zone":            "core",
    "role":            "neural-repeater",
    "coherence_ms":    118.4,
    "atp_pct":         83.2,
    "fidelity":        0.9731,
    "packets_sent":    47,
    "packets_dropped": 2,
    "status":          "OK",       # "OK" | "WARN" | "CRIT"
    "timestamp":       "2026-03-17T12:00:00"
}
```
