"""
pro02-mycelial-mesh/routing.py
BRNA Layer 3 — Interstellar Routing
Modified Dijkstra with Resonance Cost (C_R).
Bio-Resonance Routing (BRR) protocol.
"""

import networkx as nx
from mycelial_mesh import build_brna_topology


def resonance_cost(coherence_time_ms: float, metabolic_overhead: float) -> float:
    """
    C_R = sum(1/CoherenceTime + MetabolicOverhead)
    Lower C_R = better path (more coherent, less metabolic drain).
    """
    coherence = max(coherence_time_ms, 0.001)
    return (1.0 / coherence) + metabolic_overhead


def brr_route(mesh, source: str, destination: str,
              coherence_map: dict = None, metabolic_map: dict = None) -> list:
    """
    Bio-Resonance Routing: find lowest resonance-cost path.
    Falls back to standard shortest path if no coherence data.
    """
    if coherence_map is None:
        coherence_map = {n: 100.0 for n in mesh.graph.nodes()}
    if metabolic_map is None:
        metabolic_map = {n: 0.1 for n in mesh.graph.nodes()}

    # Build weighted graph using C_R as edge weight
    weighted = nx.Graph()
    for u, v, data in mesh.graph.edges(data=True):
        if data.get("link_type") == "entanglement":
            cost = 0.0   # Entanglement pairs: zero routing cost
        else:
            node_cost = resonance_cost(
                coherence_map.get(v, 100.0),
                metabolic_map.get(v, 0.1)
            )
            cost = data.get("weight", 1.0) + node_cost
        weighted.add_edge(u, v, weight=cost)

    try:
        path = nx.dijkstra_path(weighted, source, destination, weight="weight")
        cost = nx.dijkstra_path_length(weighted, source, destination, weight="weight")
        print(f"[BRR] Route {source} → {destination}: {' → '.join(path)}  C_R={cost:.4f}")
        return path
    except nx.NetworkXNoPath:
        print(f"[BRR] No path found: {source} → {destination}")
        return []


def entanglement_swap(mesh, node_a: str, node_b: str, node_c: str) -> bool:
    """
    Entanglement swapping: if A~~B and B~~C exist, create virtual A~~C link.
    Extends quantum network range via intermediate nodes.
    """
    ab = mesh.graph.has_edge(node_a, node_b)
    bc = mesh.graph.has_edge(node_b, node_c)
    if ab and bc:
        mesh.graph.add_edge(node_a, node_c, weight=0.0, link_type="entanglement-swapped")
        print(f"[SWAP] Entanglement swap: {node_a} ~~~ {node_b} ~~~ {node_c} → {node_a} ~~~ {node_c}")
        return True
    print(f"[SWAP] Cannot swap: missing link(s).")
    return False


if __name__ == "__main__":
    print("=== BRNA Week 3: BRR Routing ===\n")
    mesh = build_brna_topology()

    coherence_map = {
        "NR-A": 120.0, "NR-B": 95.0, "NR-C": 110.0, "NR-D": 150.0,
        "NR-E": 80.0,  "NR-F": 90.0, "DNA-Store": 200.0,
        "HITL-GW": 999.0, "Monitor-1": 999.0, "Monitor-2": 999.0,
        "QNode-A": 50.0, "QNode-B": 50.0, "QNode-C": 50.0, "QNode-D": 50.0,
    }
    metabolic_map = {n: 0.1 for n in mesh.graph.nodes()}
    metabolic_map["NR-B"] = 0.4   # Simulated high metabolic load on NR-B

    print("--- Route: NR-A to DNA-Store ---")
    brr_route(mesh, "NR-A", "DNA-Store", coherence_map, metabolic_map)

    print("\n--- Route: NR-A to HITL-GW ---")
    brr_route(mesh, "NR-A", "HITL-GW", coherence_map, metabolic_map)

    print("\n--- Entanglement Swap: QNode-A via QNode-B to QNode-C ---")
    mesh.add_entanglement_link("QNode-B", "QNode-C")
    entanglement_swap(mesh, "QNode-A", "QNode-B", "QNode-C")
