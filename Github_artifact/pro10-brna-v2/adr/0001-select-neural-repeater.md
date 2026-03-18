# ADR 0001 — Select Neural Repeater as Primary Architecture

**Date:** 2026-03-17  
**Status:** Accepted  
**Deciders:** Architect, Bio-Quantum Specialist

---

## Context

The BRNA project evaluated four architectural branches using Tree of Thoughts (ToT):

- Branch A: Mycelial Mesh (substrate-first)
- Branch B: Orch OR Neural Repeater (processor-first)
- Branch C: DNA Data-Lake (storage-first)
- Branch D: Entangled Bio-Resonance Sky (protocol-first)

A primary architecture must be selected that best addresses the core challenge: maintaining quantum coherence at room temperature across a living network substrate.

## Decision

**Select Branch B — Orch OR Neural Repeater** as the primary architecture (Rank 1).

## Rationale

| Criterion | Score | Reasoning |
|-----------|-------|-----------|
| Scalability | Medium | Complex but extensible via entanglement swapping |
| Biological Feasibility | Medium | Theoretical but grounded in Penrose-Hameroff Orch OR |
| Novelty | Extreme | Highest innovation potential |
| Impact | Philosophical + Practical | Solves quantum coherence at room temp |

The Neural Repeater directly solves the "cryogenic quantum" problem by using biological micro-environments (microtubule lattices) to protect coherence — eliminating the need for cryogenic infrastructure.

## Consequences

- **Positive:** Enables BCI integration without external hardware; biological micro-environments handle decoherence natively
- **Negative:** Ethical risk of using "conscious" structures for routing; potential for neural noise / ghost-signals
- **Mitigation:** HITL gateway (ADR 0004) required; neural noise filtered via AI signal isolation in QSP layer

## Rejected Alternatives

- **Branch C (DNA Data-Lake):** Relegated to Storage Module role due to high read/write latency (sequencing/synthesis bottleneck)
- **Branch D (Bio-Resonance Sky):** Entanglement monogamy limits broadcast; low scalability score
