# pro02-mycelial-mesh
## BRNA Layer 2 — Sub-Network Link Layer (Mycelial Mesh)

**Status:** Implementation Planning  
**TRL:** 4-5 (Lab validation, growth logic implemented)  
**Architecture Rank:** 2 (Physical topology — selected in ADR 0002)  
**Packet Tracer devices:** SW-BIO switch (10.0.2.0/24), SW-HITL switch (10.0.3.0/24)

---

## What this module does

The Ethernet switches in Packet Tracer represent the **mycelial mesh fabric** — the fungal substrate that physically distributes data across the BRNA network. This module models that fabric using NetworkX with Physarum polycephalum (slime mold) inspired growth logic:

- Self-healing: when a link fails (decoherence storm), new paths regrow automatically
- Nutrient-powered: each link has a metabolic cost that increases post-healing
- BLAP addressing: every node gets a 64-bit ID derived from a simulated mitochondrial DNA seed

The routing layer runs Bio-Resonance Routing (BRR) — a modified Dijkstra where the edge weight is the resonance cost C_R rather than hop count or latency.

---

## Files

| File | Purpose |
|------|---------|
| `mycelial_mesh.py` | `MycelialMesh` class, BLAP addressing, full 14-node topology builder |
| `routing.py` | BRR routing, resonance cost, entanglement swapping |

---

## Key classes and functions

### `MycelialMesh` (mycelial_mesh.py)

```python
mesh = build_brna_topology()          # builds all 14 nodes + links
mesh.topology_summary()               # print node table

mesh.simulate_decoherence_storm([     # remove failed links
    ("NR-A", "NR-B"), ("NR-B", "NR-D")
])
mesh.heal()                           # regrow with higher metabolic cost
```

### `routing.py` — key functions

| Function | Purpose |
|----------|---------|
| `resonance_cost(t_c, overhead)` | C_R = 1/T_c + metabolic_overhead |
| `brr_route(mesh, src, dst)` | Modified Dijkstra → lowest C_R path |
| `entanglement_swap(mesh, A, B, C)` | Create virtual A~~C from A~~B + B~~C |

---

## Topology — 14 nodes, 4 zones

```
CORE (10.0.1.x)          BIO (10.0.2.x)       HITL (10.0.3.x)
NR-A ─── NR-B ─── NR-C   NR-E                 HITL-GW
  \        |      /       DNA-Store             Monitor-1
   \──── NR-D ──/         NR-F                  Monitor-2
         (hub)

ENTANGLEMENT (10.0.4.x)
QNode-A ~~~ QNode-B   (pair 1)
QNode-C ~~~ QNode-D   (pair 2)
```

---

## BLAP Address generation

```python
from mycelial_mesh import generate_blap_address
addr = generate_blap_address("NR-A")
# → "A3F2B901CD456E78"  (64-bit hex, derived from SHA-256 of mito-DNA seed)
```

Each address is deterministic — same node ID always produces the same BLAP address — modelling real mitochondrial DNA uniqueness.

---

## Resonance cost formula

```
C_R = (1 / CoherenceTime_ms) + MetabolicOverhead

Example:
  NR-A: coherence=120ms, overhead=0.1  → C_R = 0.00833 + 0.1 = 0.108
  NR-B: coherence=95ms,  overhead=0.4  → C_R = 0.01053 + 0.4 = 0.411

BRR prefers the path through NR-A (lower C_R).
```

---

## How to run

```bash
cd pro02-mycelial-mesh

# Build topology + print summary
python mycelial_mesh.py

# Run BRR routing + entanglement swap demo
python routing.py
```

---

## Connection to other modules

- Takes `get_resonance_cost()` from `pro01-neural-repeater/microtubule.py` as node weights
- Provides `brr_route()` paths to `pro04-resonance-protocol/qsp_protocol.py` for packet forwarding
- Entanglement pairs consumed by `pro04-resonance-protocol/qsp_protocol.py` QSP handshake
