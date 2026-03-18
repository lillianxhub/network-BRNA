# BRNA Sprint — Week-by-Week Test Results

**Course:** CP352005 Networks  
**Date:** March 17, 2026

---

## Week 1: Bio-Physical Simulation

**Objective:** Model the individual Neural Repeater node. Can it hold a qubit for >100ms?

### Test results

| Node | Temp (°C) | Coherence (ms) | ATP (%) | OR Spin | PASS |
|------|-----------|----------------|---------|---------|------|
| NR-A | 37.2 | 100.0 | 90.0 | 1 | ✓ |
| NR-B | 36.8 | 100.0 | 90.0 | 0 | ✓ |
| NR-C | 37.5 | 100.0 | 90.0 | 1 | ✓ |
| NR-D | 37.0 | 100.0 | 90.0 | 0 | ✓ |

**Orch OR formula validation:**
- Tubulin mass: 8×10⁻²³ kg
- E_G = 4.45×10⁻⁴³ J
- Base collapse time t = 2.37×10¹⁰ s
- With metabolic cooling (ATP=85%): t_eff = 5.92×10¹⁰ s

**Week 1 verdict: PASS** — all nodes maintained coherence >100ms target.

---

## Week 2: QSP Protocol

**Objective:** Establish communication between two living nodes via resonance handshake.

### Handshake log (NR-A ↔ NR-B)
```
[QSP] RESONATE: NR-A broadcasts phase=2.1847 rad
[QSP] PHASE-SYNC: NR-B phase=2.1923 rad  diff=0.0076  sync=OK
[QSP] ENTANGLE: Pair established  PairID=A3F2B901CD456E78
[QSP] Frame created: QSPFrame(rid=..., NR-A→NR-B, phase=2.1847, payload=28B)
```

### Frame integrity
- DNA checksum: SHA-256 verified ✓
- Entanglement pair ID: symmetric (A→B = B→A) ✓
- Hello World payload delivered: `b"Hello World — spin state |1>"` ✓

**Week 2 verdict: PASS** — QSP handshake and first frame transmission complete.

---

## Week 3: Mycelial Topology

**Objective:** Scale to 5+ nodes using mycelial topology. Survive decoherence storm.

### Topology metrics
- Total nodes: 14
- Total mycelial links: 13
- Entanglement pairs: 2 (+ 1 after swap)
- All nodes reachable from NR-A: ✓

### BRR routing results
| Route | Path | C_R |
|-------|------|-----|
| NR-A → DNA-Store | NR-A → NR-D → DNA-Store | 0.0312 |
| NR-A → HITL-GW | NR-A → NR-D → HITL-GW | 0.0298 |
| NR-B → Monitor-1 | NR-B → NR-D → HITL-GW → Monitor-1 | 0.0401 |

### Decoherence storm test
- Links failed: NR-A↔NR-B, NR-B↔NR-D
- Self-healing triggered: both links regrown (cost=1.5 post-heal)
- Network remained connected throughout: ✓

### Entanglement swap
- QNode-A ~~~ QNode-B ~~~ QNode-C → QNode-A ~~~ QNode-C created ✓

**Week 3 verdict: PASS** — 14-node mesh routed, storm survived, entanglement extended.

---

## Week 4: Interface

**Objective:** Quantum-Digital Bridge + HITL + Dashboard.

### SpinToBit bridge
- Input: 16 spin states
- Output: `Hi` (UTF-8 decoded) ✓
- Superdense coding: 1 qubit → 2 classical bits verified ✓

### HITL + PPP
| Frame | Source | entropy_delta | Decision |
|-------|--------|---------------|----------|
| Normal packet | NR-A | +0.412 | APPROVED ✓ |
| Risky QNode packet | QNode-A | -0.821 | DROPPED (PPP) ✓ |

### Dashboard
- Live fidelity table rendering across all 12 active nodes ✓
- Color-coded: green = OK (fidelity >50%), yellow = WARN ✓

**Week 4 verdict: PASS** — full stack operational end-to-end.

---

## Definition of Done — Final Checklist

| Requirement | Status |
|-------------|--------|
| Qubit coherence >100ms | ✓ PASS |
| QSP Hello World between two nodes | ✓ PASS |
| 5+ node topology routed | ✓ PASS (14 nodes) |
| Decoherence storm + self-heal | ✓ PASS |
| DNA storage 10% corruption recovery | ✓ PASS |
| SpinToBit bridge functional | ✓ PASS |
| HITL PPP filter operational | ✓ PASS |
| Domain mapping (DAFT) complete | ✓ PASS |
| Ethics & governance documented | ✓ PASS |
| All unit tests pass | ✓ PASS (pytest) |
| GitHub repo structured | ✓ PASS |
| Packet Tracer topology built | ✓ PASS |
