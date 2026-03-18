# ADR 0002 — Mycelial Mesh as Physical Layer 2 Topology

**Date:** 2026-03-17  
**Status:** Accepted  
**Deciders:** Architect, Bio-Quantum Specialist, Network Engineer

---

## Context

A physical Layer 2 topology must be chosen for planet-side distribution of the BRNA network. The topology must satisfy three requirements:

1. **Resilience:** survive partial node or link failure without full network partition
2. **Scalability:** able to grow organically to planetary scale
3. **Biological realism:** grounded in real fungal network behavior that can be modeled and simulated

Four candidates were evaluated from the ToT analysis:
- Star topology (classical, centralized)
- Full mesh (classical, high link overhead)
- Mycelial mesh (Branch A — Physarum polycephalum inspired)
- Quantum-only topology (Branch D — no classical L2)

---

## Decision

**Select Branch A — Mycelial Mesh** as the physical L2 substrate, implemented as:
- **Simulation:** Python `networkx.Graph` with weighted edges (metabolic cost)
- **Mockup:** Ethernet switches (SW-BIO, SW-HITL) in Cisco Packet Tracer
- **Addressing:** BLAP (Bio-Link Access Protocol) — 64-bit addresses derived from SHA-256 of mitochondrial DNA seeds

---

## Evaluation matrix

| Criterion | Star | Full Mesh | Mycelial Mesh | Quantum-only |
|-----------|------|-----------|---------------|-------------|
| Scalability | Low | Low | **High (Global)** | Low (pair-based) |
| Self-healing | No | Partial | **Yes (regrowth)** | No |
| Biological feasibility | N/A | N/A | **High (current bio)** | Low (physics limits) |
| Simulation complexity | Low | Medium | **Medium** | Very high |
| Maps to PT topology | Yes | Partial | **Yes (switches)** | No |

---

## Rationale

Physarum polycephalum (slime mold) has been scientifically demonstrated to independently evolve near-optimal network topologies that match human-engineered rail and highway networks (Tero et al., 2010, Science). This provides biological grounding for the mycelial mesh approach.

Key properties that make it ideal:
- **Self-healing:** fungal strands regrow around damage — modeled by `heal()` in `mycelial_mesh.py`
- **Nutrient-powered:** metabolic cost on each link models real biological energy consumption
- **Emergent optimization:** Dijkstra + resonance cost converges to biologically-inspired shortest paths
- **Practical simulation:** NetworkX provides graph primitives; switches in PT provide physical mockup

---

## Implementation mapping

| BRNA concept | Python class | PT device |
|-------------|-------------|-----------|
| Mycelial fiber strand | `Graph.add_edge(weight=metabolic_cost)` | Ethernet link |
| Fungal junction node | `Graph.add_node()` with BLAP address | Switch port |
| Self-healing regrowth | `heal()` — re-adds edges at higher cost | Redundant link |
| Decoherence storm | `simulate_decoherence_storm()` | Link failure simulation |

---

## Consequences

**Positive:**
- Provides the most viable physical topology for planet-side deployment
- Self-healing property directly satisfies the Week 3 stress test requirement
- Nutrient-powered model introduces a second routing metric (metabolic overhead) alongside coherence time — enriching the C_R formula

**Negative:**
- Biological latency for classical signals: real fungal networks propagate signals at ~1 cm/min — far too slow for classical networking
- Requires constant "feeding" (metabolic maintenance) — modeled as ATP drain
- Mitigation: in simulation, latency is abstracted away; only the topology and routing logic are modeled

**Rejected alternatives:**
- **Full mesh:** O(n²) link overhead; impractical at planetary scale
- **Quantum-only (Branch D):** entanglement monogamy prevents broadcast; no L2 equivalent
- **Star topology:** single point of failure; contradicts BRNA resilience requirement

---

## References

- Tero, A. et al. (2010). Rules for Biologically Inspired Adaptive Network Design. *Science*, 327(5964), 439–442.
- Nakagaki, T. et al. (2000). Maze-solving by an amoeboid organism. *Nature*, 407, 470.
