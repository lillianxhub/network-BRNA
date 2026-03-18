"""
pro02-mycelial-mesh/mycelial_mesh.py
BRNA Layer 2 — Sub-Network Link Layer
Simulates the mycelial mesh fabric using NetworkX.
Nodes addressed via Bio-Link Access Protocol (BLAP).
"""

import hashlib
import networkx as nx


def generate_blap_address(node_id: str) -> str:
    """
    BLAP: Bio-Link Access Protocol addressing.
    Derives a 64-bit node ID from a simulated mitochondrial DNA sequence.
    """
    dna_seed = f"mito-dna-{node_id}-brna2026"
    h = hashlib.sha256(dna_seed.encode()).hexdigest()
    return h[:16].upper()   # 64-bit hex = 16 hex chars


class MycelialMesh:
    """
    Represents the physical L2 substrate — the fungal mycelium fabric.
    Based on Physarum polycephalum growth logic:
    - Self-healing: if a link fails, reroutes automatically
    - Nutrient-powered: link weights represent metabolic cost
    """

    def __init__(self):
        self.graph = nx.Graph()
        self.blap_table = {}      # node_id → BLAP address
        self.failed_links = set()

    def add_node(self, node_id: str, ip: str, role: str = "neural-repeater"):
        blap = generate_blap_address(node_id)
        self.blap_table[node_id] = blap
        self.graph.add_node(node_id, ip=ip, role=role, blap=blap)
        print(f"[MESH] Node added: {node_id} | IP: {ip} | BLAP: {blap} | Role: {role}")

    def add_mycelial_link(self, node_a: str, node_b: str, metabolic_cost: float = 1.0):
        """Add a fungal strand between two nodes. Weight = metabolic overhead."""
        self.graph.add_edge(node_a, node_b, weight=metabolic_cost, link_type="mycelial")
        print(f"[MESH] Mycelial link: {node_a} ←→ {node_b}  cost={metabolic_cost}")

    def add_entanglement_link(self, node_a: str, node_b: str):
        """Quantum entanglement pair — zero classical cost, non-local."""
        self.graph.add_edge(node_a, node_b, weight=0.0, link_type="entanglement")
        print(f"[MESH] Entanglement pair: {node_a} ~~~ {node_b}  cost=0 (non-local)")

    def simulate_decoherence_storm(self, failed_links: list):
        """Simulate a decoherence event — remove links, trigger self-healing."""
        for a, b in failed_links:
            if self.graph.has_edge(a, b):
                self.graph.remove_edge(a, b)
                self.failed_links.add((a, b))
                print(f"[STORM] Link {a}↔{b} failed — decoherence storm.")
        print(f"[STORM] {len(failed_links)} links failed. Triggering mycelial reroute...")

    def heal(self):
        """Regrow failed mycelial links — self-healing behavior."""
        for a, b in list(self.failed_links):
            self.graph.add_edge(a, b, weight=1.5, link_type="mycelial-regrown")
            print(f"[HEAL] Regrown link: {a} ←→ {b}  (higher cost post-heal)")
        self.failed_links.clear()

    def topology_summary(self):
        print(f"\n[MESH] Nodes: {self.graph.number_of_nodes()} | Links: {self.graph.number_of_edges()}")
        for n, d in self.graph.nodes(data=True):
            print(f"  {n}: IP={d.get('ip')} BLAP={d.get('blap')} Role={d.get('role')}")


def build_brna_topology() -> MycelialMesh:
    """Build the full BRNA Packet Tracer topology as a MycelialMesh."""
    mesh = MycelialMesh()

    # Core router nodes (L1 neural repeaters)
    mesh.add_node("NR-A", ip="10.0.1.1", role="neural-repeater")
    mesh.add_node("NR-B", ip="10.0.1.2", role="neural-repeater")
    mesh.add_node("NR-C", ip="10.0.1.3", role="neural-repeater")
    mesh.add_node("NR-D", ip="10.0.1.4", role="hub-router")

    # Bio zone nodes
    mesh.add_node("NR-E",      ip="10.0.2.1", role="neural-repeater")
    mesh.add_node("DNA-Store", ip="10.0.2.2", role="dna-storage")
    mesh.add_node("NR-F",      ip="10.0.2.3", role="neural-repeater")

    # HITL zone
    mesh.add_node("HITL-GW",  ip="10.0.3.1", role="hitl-gateway")
    mesh.add_node("Monitor-1", ip="10.0.3.2", role="monitor")
    mesh.add_node("Monitor-2", ip="10.0.3.3", role="monitor")

    # Entanglement zone
    mesh.add_node("QNode-A", ip="10.0.4.1", role="qnode")
    mesh.add_node("QNode-B", ip="10.0.4.2", role="qnode")
    mesh.add_node("QNode-C", ip="10.0.4.3", role="qnode")
    mesh.add_node("QNode-D", ip="10.0.4.4", role="qnode")

    # Mycelial core mesh links
    mesh.add_mycelial_link("NR-A", "NR-B", metabolic_cost=1.0)
    mesh.add_mycelial_link("NR-B", "NR-C", metabolic_cost=1.0)
    mesh.add_mycelial_link("NR-A", "NR-D", metabolic_cost=1.2)
    mesh.add_mycelial_link("NR-B", "NR-D", metabolic_cost=0.8)
    mesh.add_mycelial_link("NR-C", "NR-D", metabolic_cost=1.1)

    # Bio zone links
    mesh.add_mycelial_link("NR-D", "NR-E",      metabolic_cost=1.3)
    mesh.add_mycelial_link("NR-D", "DNA-Store",  metabolic_cost=1.5)
    mesh.add_mycelial_link("NR-D", "NR-F",       metabolic_cost=1.3)

    # HITL links
    mesh.add_mycelial_link("NR-C", "HITL-GW",  metabolic_cost=0.5)
    mesh.add_mycelial_link("NR-D", "HITL-GW",  metabolic_cost=0.5)
    mesh.add_mycelial_link("HITL-GW", "Monitor-1", metabolic_cost=0.2)
    mesh.add_mycelial_link("HITL-GW", "Monitor-2", metabolic_cost=0.2)

    # Entanglement pairs (quantum links)
    mesh.add_entanglement_link("QNode-A", "QNode-B")
    mesh.add_entanglement_link("QNode-C", "QNode-D")

    return mesh


if __name__ == "__main__":
    print("=== BRNA Week 3: Mycelial Mesh Topology ===\n")
    mesh = build_brna_topology()
    mesh.topology_summary()

    print("\n--- Decoherence Storm Test ---")
    mesh.simulate_decoherence_storm([("NR-A", "NR-B"), ("NR-B", "NR-D")])
    mesh.heal()
    print("\nPost-heal topology:")
    mesh.topology_summary()
