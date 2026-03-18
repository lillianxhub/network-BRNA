"""
tests/test_routing.py
Unit tests for pro02-mycelial-mesh/mycelial_mesh.py and routing.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pro02-mycelial-mesh'))

import pytest
from mycelial_mesh import MycelialMesh, build_brna_topology, generate_blap_address
from routing import brr_route, entanglement_swap, resonance_cost


class TestBLAP:

    def test_blap_address_length(self):
        addr = generate_blap_address("NR-A")
        assert len(addr) == 16

    def test_blap_address_deterministic(self):
        a1 = generate_blap_address("NR-A")
        a2 = generate_blap_address("NR-A")
        assert a1 == a2

    def test_blap_address_unique_per_node(self):
        addrs = [generate_blap_address(f"NR-{x}") for x in "ABCDEF"]
        assert len(set(addrs)) == 6   # all unique


class TestMycelialMesh:

    def test_add_node(self):
        mesh = MycelialMesh()
        mesh.add_node("NR-A", ip="10.0.1.1", role="neural-repeater")
        assert "NR-A" in mesh.graph.nodes
        assert mesh.graph.nodes["NR-A"]["ip"] == "10.0.1.1"

    def test_blap_assigned_on_add(self):
        mesh = MycelialMesh()
        mesh.add_node("NR-A", ip="10.0.1.1")
        assert "NR-A" in mesh.blap_table
        assert len(mesh.blap_table["NR-A"]) == 16

    def test_add_mycelial_link(self):
        mesh = MycelialMesh()
        mesh.add_node("NR-A", ip="10.0.1.1")
        mesh.add_node("NR-B", ip="10.0.1.2")
        mesh.add_mycelial_link("NR-A", "NR-B", metabolic_cost=1.0)
        assert mesh.graph.has_edge("NR-A", "NR-B")
        assert mesh.graph["NR-A"]["NR-B"]["link_type"] == "mycelial"

    def test_add_entanglement_link_zero_cost(self):
        mesh = MycelialMesh()
        mesh.add_node("QNode-A", ip="10.0.4.1")
        mesh.add_node("QNode-B", ip="10.0.4.2")
        mesh.add_entanglement_link("QNode-A", "QNode-B")
        assert mesh.graph["QNode-A"]["QNode-B"]["weight"] == 0.0
        assert mesh.graph["QNode-A"]["QNode-B"]["link_type"] == "entanglement"

    def test_decoherence_storm_removes_links(self):
        mesh = build_brna_topology()
        assert mesh.graph.has_edge("NR-A", "NR-B")
        mesh.simulate_decoherence_storm([("NR-A", "NR-B")])
        assert not mesh.graph.has_edge("NR-A", "NR-B")

    def test_heal_restores_links(self):
        mesh = build_brna_topology()
        mesh.simulate_decoherence_storm([("NR-A", "NR-B")])
        mesh.heal()
        assert mesh.graph.has_edge("NR-A", "NR-B")
        assert mesh.graph["NR-A"]["NR-B"]["link_type"] == "mycelial-regrown"

    def test_healed_link_has_higher_cost(self):
        mesh = build_brna_topology()
        original_cost = mesh.graph["NR-A"]["NR-B"]["weight"]
        mesh.simulate_decoherence_storm([("NR-A", "NR-B")])
        mesh.heal()
        healed_cost = mesh.graph["NR-A"]["NR-B"]["weight"]
        assert healed_cost > original_cost

    def test_full_topology_node_count(self):
        mesh = build_brna_topology()
        assert mesh.graph.number_of_nodes() == 14

    def test_full_topology_all_zones_present(self):
        mesh = build_brna_topology()
        roles = {data["role"] for _, data in mesh.graph.nodes(data=True)}
        assert "neural-repeater" in roles
        assert "dna-storage" in roles
        assert "hitl-gateway" in roles
        assert "qnode" in roles


class TestBRRRouting:

    def test_route_exists_core_to_bio(self):
        mesh = build_brna_topology()
        path = brr_route(mesh, "NR-A", "DNA-Store")
        assert len(path) >= 2
        assert path[0] == "NR-A"
        assert path[-1] == "DNA-Store"

    def test_route_exists_core_to_hitl(self):
        mesh = build_brna_topology()
        path = brr_route(mesh, "NR-A", "HITL-GW")
        assert "HITL-GW" in path

    def test_route_exists_bio_to_monitor(self):
        mesh = build_brna_topology()
        path = brr_route(mesh, "NR-E", "Monitor-1")
        assert path[-1] == "Monitor-1"

    def test_route_prefers_high_coherence_nodes(self):
        mesh = build_brna_topology()
        coherence_map = {n: 100.0 for n in mesh.graph.nodes()}
        coherence_map["NR-B"] = 10.0   # NR-B is very low coherence
        coherence_map["NR-D"] = 200.0  # NR-D is excellent
        path = brr_route(mesh, "NR-A", "DNA-Store", coherence_map)
        # Should route via NR-D not NR-B
        assert "NR-D" in path

    def test_entanglement_swap_creates_link(self):
        mesh = build_brna_topology()
        mesh.add_entanglement_link("QNode-B", "QNode-C")
        result = entanglement_swap(mesh, "QNode-A", "QNode-B", "QNode-C")
        assert result is True
        assert mesh.graph.has_edge("QNode-A", "QNode-C")
        assert mesh.graph["QNode-A"]["QNode-C"]["link_type"] == "entanglement-swapped"

    def test_entanglement_swap_fails_missing_link(self):
        mesh = build_brna_topology()
        result = entanglement_swap(mesh, "QNode-A", "QNode-B", "QNode-C")
        assert result is False   # QNode-B~~QNode-C not in default topology

    def test_resonance_cost_formula(self):
        c = resonance_cost(coherence_time_ms=100.0, metabolic_overhead=0.1)
        assert c == pytest.approx(0.01 + 0.1)

    def test_resonance_cost_zero_coherence_clipped(self):
        c = resonance_cost(coherence_time_ms=0.0, metabolic_overhead=0.0)
        assert c > 0   # clips to 0.001 minimum
