# ADR 0004 — HITL Gateway and Paradox Prevention Protocol

**Date:** 2026-03-17  
**Status:** Accepted  
**Deciders:** Architect, Ethics Lead

---

## Context

Non-local QSP communication (zero-latency, potentially non-causal) creates risk of causality violations — packets that arrive before they are sent, or that decrease local entropy in ways that violate thermodynamic constraints. Human oversight is also required by the project's ethics and governance requirements.

## Decision

**Implement HITL-GW as a mandatory L5 node** with the Paradox Prevention Protocol (PPP) as its automated filter, plus human operator override capability.

## Rationale

- PPP entropy check: drops packets where `entropy_delta < -0.15` (configurable)
- Human override: operator can approve or permanently block any flagged resonance_id
- Audit log: every decision recorded — satisfies ethics/governance requirement
- Maps to a dedicated PC node (HITL-GW, 10.0.3.1) in Packet Tracer

## PPP Algorithm

```
entropy_delta = payload_entropy - phase_delta
if entropy_delta < -PPP_ENTROPY_THRESHOLD:
    DROP packet
    LOG to audit trail
    ALERT human operator
else:
    FORWARD to destination
```

## Consequences

- Adds latency at L5 for all packets passing through HITL zone
- Required for any packet destined for Monitor nodes or external outputs
- Neural noise from Orch OR ghost-signals is filtered here before reaching application layer
- All QNode entanglement packets are automatically flagged for human review (conscious-structure policy)
