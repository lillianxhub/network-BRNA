# ADR 0003 — DNA Data-Lake as Storage Module (Not Primary Router)

**Date:** 2026-03-17  
**Status:** Accepted  
**Deciders:** Architect, Engineer

---

## Context

Branch C (DNA Data-Lake) scored "Extreme" on storage density (10^18 bytes/cc) but was originally proposed as a full network architecture. The evaluation must decide whether to use it as a primary routing tier or relegate it to a supplementary role.

## Decision

**Relegate Branch C to a Storage Module** — not a primary routing architecture. Implemented as `dna_store.py` hanging off the bio zone (DNA-Store PC node, 10.0.2.2).

## Rationale

| Factor | Assessment |
|--------|------------|
| Read/write latency | Sequencing/synthesis = seconds to hours — unusable for live routing |
| Storage density | 10^18 bytes/cc — unmatched, ideal for archival |
| Error resilience | Reed-Solomon ECC handles 10% corruption |
| Role fit | "Galactic Archive" — long-term persistence only |

## Consequences

- DNA-Store becomes the permanent archival sink for collapsed spin states
- All routing bypasses DNA-Store (too slow for L3)
- Write-once semantics: data written to DNA-Store is treated as immutable historical record
- Simulated as a Python class with in-memory dict (models the fluid array concept)

## Rejected Alternative

Using DNA-Store as a primary packet buffer — rejected due to microsecond routing requirements vs. millisecond-to-second DNA synthesis latency.
