# pro03-dna-storage
## BRNA Storage Module — DNA Data Lake

**Status:** Supplementary (relegated from primary architecture — see ADR 0003)  
**TRL:** 6 (Proven storage density concept; simulated in Python)  
**Role:** Galactic Archive — long-term persistence, not primary routing  
**Packet Tracer device:** DNA-Store PC (10.0.2.2/24, hanging off SW-BIO)

---

## What this module does

The DNA-Store PC in Packet Tracer represents a biological fluid array — a container of synthetic DNA strands where each strand encodes a portion of the network's collapsed spin-state history.

Key properties that make DNA ideal for archival:
- **Density:** 10¹⁸ bytes per cubic millimeter (215 Petabytes per gram)
- **Persistence:** data survives for millennia under proper conditions
- **Error resilience:** Reed-Solomon ECC corrects up to 10% base corruption

The trade-off that prevents DNA from being a primary router: read/write requires DNA synthesis (writing) and sequencing (reading) — processes that take seconds to hours, not microseconds.

---

## Files

| File | Purpose |
|------|---------|
| `dna_store.py` | `DNAStore` class — encode/store/retrieve with Reed-Solomon ECC |

---

## DNA encoding scheme

Binary data is mapped to DNA bases using a 2-bit-per-base encoding:

```
00 → A (Adenine)
01 → T (Thymine)
10 → G (Guanine)
11 → C (Cytosine)
```

Reed-Solomon error correction symbols are appended before encoding, so that up to `ECC_SYMBOLS / 2` corrupted bases can be corrected on readback.

### Example

```python
from dna_store import DNAStore

store = DNAStore()
seq_id = store.write("packet-001", b"Hello from NR-A")
# Stored as DNA: ATGCTAGCATGC...

recovered = store.read(seq_id)                       # clean read
recovered = store.read(seq_id, corruption_rate=0.10) # 10% bases corrupted, still recovers
```

---

## Storage metrics

| Metric | Value |
|--------|-------|
| Encoding density | 2 bits per base |
| ECC symbols | 10 (Reed-Solomon) |
| Max correctable corruption | ~5% (practical) / 10% (theoretical) |
| Simulated persistence | Unlimited (in-memory dict) |
| Write latency (simulated) | Instant (models conceptual write) |
| Read latency (simulated) | Instant (real DNA sequencing = hours) |

---

## How to run

```bash
pip install reedsolo
cd pro03-dna-storage
python dna_store.py
```

Expected output:
```
[DNA-Store] Written: key=test-packet-01 seq_id=a3f2b901cd45 length=192 bases
--- Read back (no corruption) ---
Recovered: b'Hello from NR-A via QSP protocol v1.0'
Integrity check: PASSED
--- Read back with 10% corruption (Reed-Solomon test) ---
Reed-Solomon error correction: PASSED
```

---

## Connection to other modules

- Receives write commands from `pro04-resonance-protocol/hitl_gateway.py` (archiving approved packets)
- Feeds archived spin-state history to `pro04-resonance-protocol/dashboard.py` for long-term fidelity logs
- Sequence IDs stored in QSP frame `dna_checksum` field as integrity reference
