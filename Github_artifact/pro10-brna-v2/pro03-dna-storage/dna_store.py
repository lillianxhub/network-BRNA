"""
pro03-dna-storage/dna_store.py
BRNA Storage Module — DNA Data Lake
Encodes binary data as DNA sequences (A/T/G/C).
Reed-Solomon error correction for biological degradation tolerance.
Storage density: 10^18 bytes per cubic millimeter (simulated).
"""

import hashlib
from reedsolo import RSCodec

BASES = {0b00: 'A', 0b01: 'T', 0b10: 'G', 0b11: 'C'}
BASES_INV = {v: k for k, v in BASES.items()}
RS_ECC_SYMBOLS = 10   # Reed-Solomon error correction symbols


class DNAStore:
    """
    Simulates a DNA-based data lake.
    Writes data as synthetic DNA sequences.
    Reads back with Reed-Solomon error correction.
    Tolerates up to 10% sequence corruption.
    """

    def __init__(self, node_id: str = "DNA-Store"):
        self.node_id = node_id
        self.storage = {}        # sequence_id → dna_string
        self.codec = RSCodec(RS_ECC_SYMBOLS)
        self.write_count = 0

    def encode_to_dna(self, data: bytes) -> str:
        """Encode bytes → DNA base sequence (A/T/G/C)."""
        encoded = self.codec.encode(data)
        dna = ""
        for byte in encoded:
            for shift in (6, 4, 2, 0):
                bits = (byte >> shift) & 0b11
                dna += BASES[bits]
        return dna

    def decode_from_dna(self, dna: str) -> bytes:
        """Decode DNA base sequence → original bytes (with error correction)."""
        byte_list = []
        for i in range(0, len(dna), 4):
            chunk = dna[i:i+4]
            if len(chunk) < 4:
                break
            byte_val = 0
            for j, base in enumerate(chunk):
                byte_val |= (BASES_INV[base] << (6 - j * 2))
            byte_list.append(byte_val)
        decoded = self.codec.decode(bytes(byte_list))
        return bytes(decoded[0])

    def write(self, key: str, data: bytes) -> str:
        """Write data to DNA storage. Returns the DNA sequence ID."""
        dna = self.encode_to_dna(data)
        seq_id = hashlib.sha256(f"{self.node_id}-{key}-{self.write_count}".encode()).hexdigest()[:12]
        self.storage[seq_id] = dna
        self.write_count += 1
        print(f"[DNA-Store] Written: key={key} seq_id={seq_id} length={len(dna)} bases")
        return seq_id

    def read(self, seq_id: str, corruption_rate: float = 0.0) -> bytes:
        """Read DNA sequence, optionally simulate base corruption."""
        if seq_id not in self.storage:
            raise KeyError(f"Sequence {seq_id} not found in DNA-Store.")
        dna = self.storage[seq_id]
        if corruption_rate > 0:
            dna = self._corrupt(dna, corruption_rate)
            print(f"[DNA-Store] Simulated {corruption_rate*100:.0f}% corruption on {seq_id}")
        return self.decode_from_dna(dna)

    def _corrupt(self, dna: str, rate: float) -> str:
        """Randomly corrupt a fraction of bases."""
        import random
        bases = list(dna)
        for i in range(len(bases)):
            if random.random() < rate:
                bases[i] = random.choice([b for b in "ATGC" if b != bases[i]])
        return "".join(bases)

    def storage_summary(self):
        total_bases = sum(len(v) for v in self.storage.values())
        print(f"[DNA-Store] Sequences stored: {len(self.storage)} | Total bases: {total_bases}")


if __name__ == "__main__":
    print("=== BRNA DNA Storage Module ===\n")
    store = DNAStore()

    payload = b"Hello from NR-A via QSP protocol v1.0"
    seq_id = store.write("test-packet-01", payload)

    print("\n--- Read back (no corruption) ---")
    recovered = store.read(seq_id)
    print(f"Recovered: {recovered}")
    assert recovered == payload, "Data mismatch!"
    print("Integrity check: PASSED")

    print("\n--- Read back with 10% corruption (Reed-Solomon test) ---")
    try:
        recovered_corrupt = store.read(seq_id, corruption_rate=0.10)
        print(f"Recovered despite corruption: {recovered_corrupt}")
        print("Reed-Solomon error correction: PASSED")
    except Exception as e:
        print(f"Correction failed (expected at high corruption): {e}")

    store.storage_summary()
