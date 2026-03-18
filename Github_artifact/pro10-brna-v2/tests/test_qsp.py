"""
tests/test_qsp.py
Unit tests for pro04-resonance-protocol/qsp_protocol.py and spin_bridge.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pro04-resonance-protocol'))

import pytest
from qsp_protocol import QSPFrame, QSPHandshake
from spin_bridge import (
    spin_to_bit, spins_to_bytes, bytes_to_spins,
    superdense_encode, superdense_decode,
    bridge_pipeline, encode_for_transmission,
    superdense_bandwidth_bits
)


class TestQSPFrame:

    def test_frame_creation_basic(self):
        frame = QSPFrame("NR-A", "NR-B", b"test payload")
        assert frame.source == "NR-A"
        assert frame.destination == "NR-B"

    def test_resonance_id_length(self):
        frame = QSPFrame("NR-A", "NR-B", b"test")
        assert len(frame.resonance_id) == 16

    def test_dna_checksum_length(self):
        frame = QSPFrame("NR-A", "NR-B", b"test")
        assert len(frame.dna_checksum) == 64

    def test_entanglement_pair_id_symmetric(self):
        f1 = QSPFrame("NR-A", "NR-B", b"data")
        f2 = QSPFrame("NR-B", "NR-A", b"data")
        assert f1.entanglement_pair_id == f2.entanglement_pair_id

    def test_different_pairs_different_ids(self):
        f1 = QSPFrame("NR-A", "NR-B", b"data")
        f2 = QSPFrame("NR-A", "NR-C", b"data")
        assert f1.entanglement_pair_id != f2.entanglement_pair_id

    def test_dna_checksum_changes_with_payload(self):
        f1 = QSPFrame("NR-A", "NR-B", b"payload 1")
        f2 = QSPFrame("NR-A", "NR-B", b"payload 2")
        assert f1.dna_checksum != f2.dna_checksum

    def test_to_dict_keys(self):
        frame = QSPFrame("NR-A", "NR-B", b"test", phase_state=1.5, atp_level=85.0)
        d = frame.to_dict()
        for key in ["qsp_version", "resonance_id", "source", "destination",
                    "phase_state", "atp_level", "dna_checksum", "payload"]:
            assert key in d

    def test_phase_state_stored(self):
        frame = QSPFrame("NR-A", "NR-B", b"test", phase_state=2.718)
        assert frame.phase_state == pytest.approx(2.718)

    def test_atp_level_stored(self):
        frame = QSPFrame("NR-A", "NR-B", b"test", atp_level=77.5)
        assert frame.atp_level == pytest.approx(77.5)


class TestQSPHandshake:

    def test_handshake_completes(self):
        hs = QSPHandshake("NR-A", "NR-B")
        pair_id = hs.run()
        assert pair_id is not None
        assert len(pair_id) == 16

    def test_handshake_synchronized_flag(self):
        hs = QSPHandshake("NR-A", "NR-B")
        hs.run()
        assert hs.synchronized is True

    def test_resonate_returns_float(self):
        hs = QSPHandshake("NR-A", "NR-B")
        phase = hs.resonate()
        assert isinstance(phase, float)
        assert 0 <= phase <= 6.29   # 0 to 2π

    def test_phase_sync_tight_tolerance(self):
        hs = QSPHandshake("NR-A", "NR-B")
        phase = hs.resonate()
        result = hs.phase_sync(phase, tolerance=10.0)   # very wide tolerance
        assert result is True

    def test_entangle_raises_without_sync(self):
        hs = QSPHandshake("NR-A", "NR-B")
        hs.synchronized = False
        with pytest.raises(RuntimeError):
            hs.entangle()


class TestSpinBridge:

    def test_spin_to_bit_zero(self):
        assert spin_to_bit(0) == 0

    def test_spin_to_bit_one(self):
        assert spin_to_bit(1) == 1

    def test_spin_to_bit_invalid(self):
        with pytest.raises(ValueError):
            spin_to_bit(2)

    def test_spins_to_bytes_roundtrip(self):
        original = b"Hi"
        spins = bytes_to_spins(original)
        recovered = spins_to_bytes(spins)
        assert recovered == original

    def test_bytes_to_spins_length(self):
        data = b"A"   # 1 byte = 8 bits
        spins = bytes_to_spins(data)
        assert len(spins) == 8

    def test_superdense_encode_all_pairs(self):
        assert superdense_encode((0, 0)) == 'I'
        assert superdense_encode((0, 1)) == 'X'
        assert superdense_encode((1, 0)) == 'Z'
        assert superdense_encode((1, 1)) == 'XZ'

    def test_superdense_decode_roundtrip(self):
        for pair in [(0,0), (0,1), (1,0), (1,1)]:
            gate = superdense_encode(pair)
            recovered = superdense_decode(gate, pair)
            assert recovered == pair

    def test_superdense_bandwidth(self):
        assert superdense_bandwidth_bits(8)  == 16
        assert superdense_bandwidth_bits(64) == 128

    def test_bridge_pipeline_utf8(self):
        text = "Hi!"
        spins = encode_for_transmission(text)
        result = bridge_pipeline(spins, output_format="utf8")
        assert result["error"] is None
        assert result["data"] == text

    def test_bridge_pipeline_hex(self):
        spins = encode_for_transmission("A")
        result = bridge_pipeline(spins, output_format="hex")
        assert result["error"] is None
        assert isinstance(result["data"], str)
        assert len(result["data"]) > 0

    def test_bridge_pipeline_metadata(self):
        spins = encode_for_transmission("X")
        result = bridge_pipeline(spins, output_format="utf8")
        assert result["input_spins"] == len(spins)
        assert result["superdense_bits"] == len(spins) * 2
        assert len(result["checksum"]) == 16
