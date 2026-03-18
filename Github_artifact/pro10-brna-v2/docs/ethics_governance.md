# Ethics, Regulations & HITL Governance

---

## 1. Ethical Concerns

### Conscious infrastructure risk
Branch B (Neural Repeater) uses microtubule structures that, under Orch OR theory, may produce moments of consciousness. Using "conscious" biological structures as data routers raises:
- **Informed consent** — biological nodes cannot consent to data processing
- **Pain/experience** — unknown whether OR events involve subjective experience
- **Exploitation** — living systems as infrastructure without reciprocity

### Mitigation
- Simulation-only scope: this project uses Qiskit simulation, not actual biology
- All biological modeling is in silico — no living organisms are used
- Future wet-lab work would require IRB/ethics board approval

---

## 2. Regulations

| Domain | Applicable Regulation | BRNA Compliance |
|--------|----------------------|-----------------|
| Data storage | GDPR (EU), PDPA (Thailand) | DNA checksum for integrity; data deletion supported |
| Bio research | Biosafety Level protocols | Simulation only — no lab work |
| Quantum comms | ITU-T quantum network standards | QSP aligned with ITU-T Y.3800 framework |
| AI/ML governance | Thailand PDPA, EU AI Act | HITL gateway ensures human oversight |

---

## 3. Human-in-the-Loop (HITL) Design

### HITL-GW node responsibilities
1. **PPP filter** — automatically drop causality-violating packets (entropy check)
2. **Human override** — operator can approve/block any flagged packet
3. **Audit log** — every decision recorded with timestamp and reason
4. **Ethics alert** — flags packets from conscious-structure nodes (QNode zone)

### HITL workflow

```
Packet arrives at HITL-GW
        ↓
PPP entropy check
        ↓
   Safe? ──Yes──→ Forward to destination
        │
       No
        ↓
Flag for human review
        ↓
Human operator decision
   Approve / Block
        ↓
Log to audit trail
```

### Governance metrics (tracked in metrics.md)
- PPP drop rate: target < 5% of all packets
- Human review latency: target < 30s
- Audit log retention: 100 simulated years
