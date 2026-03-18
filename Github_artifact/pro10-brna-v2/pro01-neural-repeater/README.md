# pro01-neural-repeater
## BRNA Layer 1 — Bio-Physical Processing

**Status:** Active Research  
**TRL:** 3-4 (Proof-of-concept simulation)  
**Architecture Rank:** 1 (Primary — selected in ADR 0001)  
**Packet Tracer devices:** Routers NR-A, NR-B, NR-C, NR-D (10.0.1.x/24)

---

## What this module does

Every router in the Packet Tracer topology maps to a `MicrotubuleBundle` instance. The bundle simulates a tubulin-dipole lattice that can hold a quantum superposition state, then collapse it via Orchestrated Objective Reduction (Orch OR) when the gravitational self-energy threshold E_G = ℏ/t is reached.

The collapsed spin state (0 or 1) is the raw output of the BRNA processing cycle — equivalent to one clock tick in a classical CPU, but governed by quantum gravity rather than silicon oscillators.

---

## Files

| File | Purpose |
|------|---------|
| `microtubule.py` | `MicrotubuleBundle` class — initializes qubit, holds coherence, triggers OR |
| `orch_or.py` | Full Penrose-Hameroff math — E_G, collapse time, thermal decoherence, fidelity |

---

## Key classes and functions

### `MicrotubuleBundle` (microtubule.py)

```python
node = MicrotubuleBundle(node_id="NR-A", temperature=37.2)
qc   = node.initialize_qubit()       # |0⟩ → |+⟩ superposition via Hadamard
ok   = node.hold_coherence(100.0)    # hold for 100ms, drain ATP
spin = node.objective_reduction(qc)  # collapse → 0 or 1
cost = node.get_resonance_cost()     # C_R for routing layer
```

**Constraints enforced:**
- Temperature must be 36°C–39°C or `EnvironmentError` is raised
- ATP below 20% causes metabolic decoherence → `hold_coherence()` returns False
- Week 1 pass criterion: `coherence_time_ms >= 100`

### `orch_or.py` — key functions

| Function | Formula | Purpose |
|----------|---------|---------|
| `gravitational_self_energy(m, a)` | E_G = G·m²/a | Penrose OR threshold |
| `collapse_time(E_G)` | t = ℏ/E_G | Time until OR event |
| `thermal_decoherence_time(m, T, a)` | τ_D = ℏ/(m·v_th·a) | Enemy: thermal noise |
| `metabolic_cooling_factor(ATP%)` | 1.0 + (ATP/100)·1.5 | Biological shielding |
| `effective_coherence_window(E_G, ATP)` | t·factor | Actual node window |
| `resonance_fidelity(t_ms, target, ATP)` | F_R ∈ [0,1] | Quality metric for BRR |

---

## Physical parameters (tubulin dimer)

| Parameter | Value | Unit |
|-----------|-------|------|
| Mass (m) | 8.0 × 10⁻²³ | kg |
| Lattice separation (a) | 4.0 × 10⁻⁹ | m |
| Thermal window | 36–39 | °C |
| ATP decoherence threshold | 20 | % |
| Target coherence | > 100 | ms |

---

## How to run

```bash
cd pro01-neural-repeater

# Week 1 simulation — all 4 nodes
python microtubule.py

# Orch OR physics deep-dive
python orch_or.py
```

Expected output from `microtubule.py`:
```
[NR-A] Qubit initialized in superposition.
[NR-A] Held coherence for 100.0ms. ATP: 90.0%
[NR-A] Orch OR triggered → spin state: |1>  E_G=3.73e-43 J
Week 1 check: coherence held >100ms = True
```

---

## Connection to other modules

- `get_resonance_cost()` → feeds into `pro02-mycelial-mesh/routing.py` as C_R metric
- `spin_state` output → passed to `pro04-resonance-protocol/spin_bridge.py` for L4 conversion
- `temperature` + `metabolic_atp` → monitored by `pro04-resonance-protocol/dashboard.py`
