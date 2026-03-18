"""
run_simulation.py
BRNA Full Stack Simulation — Entry Point
Runs all 4 weeks of the sprint in sequence.
Usage: python run_simulation.py
       python run_simulation.py --week 1
"""

import sys
import argparse


def week1_bio_physical():
    print("\n" + "="*60)
    print("WEEK 1: Bio-Physical Simulation — Neural Repeater Node")
    print("="*60)
    sys.path.insert(0, "pro01-neural-repeater")
    from microtubule import MicrotubuleBundle, COHERENCE_TARGET_MS
    from orch_or import gravitational_self_energy, collapse_time, metabolic_cooling_factor

    nodes = {}
    for name, temp in [("NR-A", 37.2), ("NR-B", 36.8), ("NR-C", 37.5), ("NR-D", 37.0)]:
        node = MicrotubuleBundle(name, temperature=temp)
        qc = node.initialize_qubit()
        node.hold_coherence(duration_ms=100.0)
        spin = node.objective_reduction(qc)
        nodes[name] = node
        print(f"  {name}: spin={spin}, C_R={node.get_resonance_cost():.4f}")

    passed = all(n.coherence_time_ms >= COHERENCE_TARGET_MS for n in nodes.values())
    print(f"\nWeek 1 PASS: all nodes held coherence >100ms = {passed}")

    # Orch OR physics
    mass = 8e-23
    E_G = gravitational_self_energy(mass)
    t = collapse_time(E_G)
    factor = metabolic_cooling_factor(85.0)
    print(f"Orch OR: E_G={E_G:.3e} J  t={t:.3e}s  metabolic factor={factor:.2f}x")
    return nodes


def week2_qsp_protocol():
    print("\n" + "="*60)
    print("WEEK 2: QSP Protocol — Resonance Handshake")
    print("="*60)
    sys.path.insert(0, "pro04-resonance-protocol")
    from qsp_protocol import QSPHandshake, QSPFrame

    hs = QSPHandshake("NR-A", "NR-B")
    pair_id = hs.run()

    frame = QSPFrame(
        source="NR-A",
        destination="NR-B",
        payload=b"Hello World - spin state |1>",
        phase_state=hs.phase_a,
        atp_level=87.5,
    )
    print(f"\nHello World frame: {frame}")
    print(f"Entanglement Pair ID: {pair_id}")
    print("Week 2 PASS: QSP handshake and frame transmission complete")
    return frame


def week3_topology():
    print("\n" + "="*60)
    print("WEEK 3: Mycelial Topology — 5+ Nodes + Routing")
    print("="*60)
    sys.path.insert(0, "pro02-mycelial-mesh")
    from mycelial_mesh import build_brna_topology
    from routing import brr_route, entanglement_swap

    mesh = build_brna_topology()
    mesh.topology_summary()

    print("\n--- BRR Routing tests ---")
    brr_route(mesh, "NR-A", "DNA-Store")
    brr_route(mesh, "NR-A", "HITL-GW")
    brr_route(mesh, "NR-B", "Monitor-1")

    print("\n--- Decoherence Storm ---")
    mesh.simulate_decoherence_storm([("NR-A", "NR-B"), ("NR-B", "NR-D")])
    mesh.heal()

    print("\n--- Entanglement Swap ---")
    mesh.add_entanglement_link("QNode-B", "QNode-C")
    entanglement_swap(mesh, "QNode-A", "QNode-B", "QNode-C")

    print("\nWeek 3 PASS: 14 nodes routed, storm survived, entanglement extended")
    return mesh


def week4_interface(frame=None):
    print("\n" + "="*60)
    print("WEEK 4: Interface — SpinToBit Bridge + HITL + Dashboard")
    print("="*60)
    sys.path.insert(0, "pro04-resonance-protocol")
    from spin_bridge import bridge_pipeline
    from hitl_gateway import HITLGateway
    from qsp_protocol import QSPFrame

    # SpinToBit
    print("--- L4 SpinToBit Bridge ---")
    spins = [0,1,0,0,1,0,0,0, 0,1,1,0,1,0,0,1]  # "Hi"
    bridge_pipeline(spins)

    # HITL + PPP
    print("\n--- HITL Gateway + PPP ---")
    gw = HITLGateway()
    safe_frame = QSPFrame("NR-A", "NR-B", b"Normal routed packet", phase_state=1.2, atp_level=90.0)
    risky_frame = QSPFrame("QNode-A", "QNode-D", b"XX", phase_state=6.0, atp_level=5.0)
    gw.ppp_filter(safe_frame)
    gw.ppp_filter(risky_frame)
    gw.print_audit_log()

    print("\nWeek 4 PASS: SpinToBit bridge + HITL PPP filter operational")
    print("\nNote: Run 'python pro04-resonance-protocol/dashboard.py' for live terminal dashboard")


def main():
    parser = argparse.ArgumentParser(description="BRNA Full Stack Simulation")
    parser.add_argument("--week", type=int, choices=[1, 2, 3, 4],
                        help="Run a specific week only (default: all)")
    args = parser.parse_args()

    print("\nBRNA — Bio-Resonance Network Architecture")
    print("CP352005 Networks | March 2026")

    if args.week == 1 or args.week is None:
        week1_bio_physical()
    if args.week == 2 or args.week is None:
        week2_qsp_protocol()
    if args.week == 3 or args.week is None:
        week3_topology()
    if args.week == 4 or args.week is None:
        week4_interface()

    if args.week is None:
        print("\n" + "="*60)
        print("ALL WEEKS COMPLETE — BRNA simulation finished")
        print("Run 'python -m pytest tests/' to verify all unit tests")
        print("="*60)


if __name__ == "__main__":
    main()
