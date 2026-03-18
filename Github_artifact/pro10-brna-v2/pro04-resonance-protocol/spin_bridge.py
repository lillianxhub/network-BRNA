"""
pro04-resonance-protocol/spin_bridge.py
BRNA Layer 4 — Quantum-Digital Bridge
SpinToBit conversion: collapsed quantum spin states → classical bits

This module sits at the critical boundary between the bio-quantum substrate
(Layers 1-3) and the classical digital world (Layer 5 application).
Every piece of human-readable data that emerges from the BRNA network
passes through this bridge exactly once.

Key mechanism: Superdense Coding
  Using shared entanglement, Alice can transmit 2 classical bits by
  sending only 1 qubit to Bob. This doubles the effective bandwidth
  of every quantum channel in the BRNA network.
  
  Bell state encoding table:
    00 → I gate  (no operation) → |Φ+⟩
    01 → X gate  (bit flip)     → |Ψ+⟩
    10 → Z gate  (phase flip)   → |Φ-⟩
    11 → XZ gate (both)         → |Ψ-⟩
"""

import json
import struct
import hashlib
from typing import List, Tuple, Optional


# ---------------------------------------------------------------------------
# 1. Core SpinToBit conversion
# ---------------------------------------------------------------------------

def spin_to_bit(spin_state: int) -> int:
    """
    Direct mapping: collapsed qubit spin → classical bit.
    |0⟩ → 0,  |1⟩ → 1

    Parameters
    ----------
    spin_state : int  Measured qubit state (0 or 1)

    Returns
    -------
    int  Classical bit value
    """
    if spin_state not in (0, 1):
        raise ValueError(f"Invalid spin state: {spin_state}. Must be 0 or 1.")
    return spin_state


def spins_to_byte(eight_spins: List[int]) -> int:
    """
    Convert 8 spin measurements to a single byte.
    MSB first: spin[0] = bit 7, spin[7] = bit 0.

    Parameters
    ----------
    eight_spins : list[int]  Exactly 8 spin states (0 or 1)

    Returns
    -------
    int  Byte value (0–255)
    """
    if len(eight_spins) != 8:
        raise ValueError(f"Expected 8 spins, got {len(eight_spins)}")
    byte_val = 0
    for i, spin in enumerate(eight_spins):
        byte_val |= (spin_to_bit(spin) << (7 - i))
    return byte_val


def spins_to_bytes(spin_list: List[int],
                   pad_to_byte: bool = True) -> bytes:
    """
    Convert an arbitrary list of spin states to a bytes object.

    Pads with trailing 0s to reach a multiple of 8 if pad_to_byte=True.

    Parameters
    ----------
    spin_list   : list[int]  List of spin state measurements
    pad_to_byte : bool       Pad to byte boundary (default True)

    Returns
    -------
    bytes  Packed byte sequence
    """
    if pad_to_byte:
        remainder = len(spin_list) % 8
        if remainder:
            spin_list = spin_list + [0] * (8 - remainder)

    result = bytearray()
    for i in range(0, len(spin_list), 8):
        chunk = spin_list[i:i + 8]
        if len(chunk) == 8:
            result.append(spins_to_byte(chunk))
    return bytes(result)


def bytes_to_spins(data: bytes) -> List[int]:
    """
    Inverse of spins_to_bytes — unpack bytes back into spin list.
    Used for encoding data before injection into the quantum layer.

    Parameters
    ----------
    data : bytes  Input byte sequence

    Returns
    -------
    list[int]  Spin state list (MSB first per byte)
    """
    spins = []
    for byte in data:
        for shift in range(7, -1, -1):
            spins.append((byte >> shift) & 1)
    return spins


# ---------------------------------------------------------------------------
# 2. Superdense coding
# ---------------------------------------------------------------------------

def superdense_encode(bit_pair: Tuple[int, int]) -> str:
    """
    Superdense coding encoder: 2 classical bits → quantum gate operation.
    Alice applies this gate to her half of the entangled pair.

    Encoding table:
        (0,0) → 'I'   Identity — transmit as-is
        (0,1) → 'X'   Pauli-X (bit flip)
        (1,0) → 'Z'   Pauli-Z (phase flip)
        (1,1) → 'XZ'  Both X and Z

    Parameters
    ----------
    bit_pair : tuple(int, int)  Two classical bits to encode

    Returns
    -------
    str  Gate operation label
    """
    encoding = {(0, 0): 'I', (0, 1): 'X', (1, 0): 'Z', (1, 1): 'XZ'}
    if bit_pair not in encoding:
        raise ValueError(f"Invalid bit pair: {bit_pair}")
    return encoding[bit_pair]


def superdense_decode(gate_applied: str,
                      measured_pair: Tuple[int, int]) -> Tuple[int, int]:
    """
    Superdense coding decoder: Bob measures the Bell state after
    receiving Alice's qubit and decodes the 2 classical bits.

    Parameters
    ----------
    gate_applied  : str           Gate Alice applied ('I','X','Z','XZ')
    measured_pair : tuple(int,int) Bob's Bell state measurement

    Returns
    -------
    tuple(int, int)  Recovered 2 classical bits
    """
    decoding = {'I': (0, 0), 'X': (0, 1), 'Z': (1, 0), 'XZ': (1, 1)}
    if gate_applied not in decoding:
        raise ValueError(f"Unknown gate: {gate_applied}")
    return decoding[gate_applied]


def superdense_bandwidth_bits(num_qubits: int) -> int:
    """
    Classical bit capacity of a superdense-coded quantum channel.
    Each qubit carries 2 classical bits via superdense coding.
    """
    return num_qubits * 2


# ---------------------------------------------------------------------------
# 3. Full L4 bridge pipeline
# ---------------------------------------------------------------------------

def bridge_pipeline(spin_states: List[int],
                     output_format: str = "utf8") -> dict:
    """
    Full Layer 4 pipeline:
        spin states → bytes → decoded output

    Supports three output formats:
        'utf8'  : decode as UTF-8 text
        'json'  : decode as JSON object
        'hex'   : return hex string
        'raw'   : return raw bytes

    Parameters
    ----------
    spin_states   : list[int]  Collapsed qubit spin measurements
    output_format : str        Output encoding format

    Returns
    -------
    dict  Pipeline result with metadata
    """
    raw_bytes = spins_to_bytes(spin_states)
    checksum = hashlib.sha256(raw_bytes).hexdigest()[:16]

    result = {
        "input_spins": len(spin_states),
        "output_bytes": len(raw_bytes),
        "superdense_bits": superdense_bandwidth_bits(len(spin_states)),
        "checksum": checksum,
        "format": output_format,
        "data": None,
        "error": None,
    }

    try:
        if output_format == "utf8":
            result["data"] = raw_bytes.decode("utf-8", errors="replace")
        elif output_format == "json":
            result["data"] = json.loads(raw_bytes.decode("utf-8"))
        elif output_format == "hex":
            result["data"] = raw_bytes.hex()
        elif output_format == "raw":
            result["data"] = list(raw_bytes)
        else:
            raise ValueError(f"Unknown format: {output_format}")
    except Exception as e:
        result["error"] = str(e)

    print(f"[L4 Bridge] {len(spin_states)} spins → {len(raw_bytes)} bytes "
          f"→ format={output_format}  checksum={checksum}")
    return result


def encode_for_transmission(text: str) -> List[int]:
    """
    Encode a UTF-8 string into spin states for injection into
    the quantum layer (reverse pipeline — digital → quantum).

    Parameters
    ----------
    text : str  Message to encode

    Returns
    -------
    list[int]  Spin state sequence for QSP frame payload
    """
    raw = text.encode("utf-8")
    spins = bytes_to_spins(raw)
    print(f"[L4 Bridge] Encode: '{text}' → {len(raw)} bytes → {len(spins)} spins")
    return spins


# ---------------------------------------------------------------------------
# 4. Fidelity-aware decoding
# ---------------------------------------------------------------------------

def decode_with_fidelity_check(spin_states: List[int],
                                 fidelity_threshold: float = 0.7) -> Optional[str]:
    """
    Decode spin states only if the node's resonance fidelity is
    above the threshold. Below threshold, the signal is too noisy
    to produce reliable classical output — return None.

    Parameters
    ----------
    spin_states         : list[int]  Spin measurements
    fidelity_threshold  : float      Minimum F_R required (0–1)

    Returns
    -------
    str or None  Decoded text, or None if fidelity too low
    """
    # Estimate fidelity from spin variance (high variance = noisy node)
    import statistics
    if len(spin_states) < 2:
        return None
    variance = statistics.variance(spin_states)
    estimated_fidelity = 1.0 - min(1.0, variance * 2)

    print(f"[L4 Bridge] Estimated fidelity: {estimated_fidelity:.3f} "
          f"(threshold: {fidelity_threshold})")

    if estimated_fidelity < fidelity_threshold:
        print(f"[L4 Bridge] WARN: Fidelity below threshold — output suppressed")
        return None

    result = bridge_pipeline(spin_states, output_format="utf8")
    return result["data"]


# ---------------------------------------------------------------------------
# 5. Main demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("BRNA Layer 4 — Quantum-Digital Bridge (SpinToBit)")
    print("=" * 60)

    # Demo 1: encode "Hi!" and decode it back
    print("\n--- Demo 1: Encode text → spins → decode ---")
    original = "Hi BRNA!"
    spins = encode_for_transmission(original)
    result = bridge_pipeline(spins, output_format="utf8")
    print(f"  Original : '{original}'")
    print(f"  Decoded  : '{result['data']}'")
    print(f"  Match    : {original == result['data']}")

    # Demo 2: superdense coding table
    print("\n--- Demo 2: Superdense coding encoding table ---")
    for pair in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        gate = superdense_encode(pair)
        decoded = superdense_decode(gate, pair)
        print(f"  Bits {pair} → gate '{gate}' → recovered {decoded}")

    # Demo 3: bandwidth calculation
    print("\n--- Demo 3: Channel bandwidth ---")
    for qubits in [8, 64, 256, 1024]:
        classical_bits = superdense_bandwidth_bits(qubits)
        print(f"  {qubits:4d} qubits → {classical_bits:4d} classical bits "
              f"({classical_bits // 8} bytes)")

    # Demo 4: fidelity-aware decode
    print("\n--- Demo 4: Fidelity-aware decode ---")
    clean_spins = encode_for_transmission("Test")
    noisy_spins = [0, 1, 0, 1, 0, 1, 0, 1] * 4  # alternating = high variance
    print("  Clean signal:")
    decode_with_fidelity_check(clean_spins, fidelity_threshold=0.3)
    print("  Noisy signal:")
    decode_with_fidelity_check(noisy_spins, fidelity_threshold=0.7)
