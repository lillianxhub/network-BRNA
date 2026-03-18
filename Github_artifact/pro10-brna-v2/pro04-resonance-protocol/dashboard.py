"""
pro04-resonance-protocol/dashboard.py
BRNA Layer 5 — Galactic Command Dashboard
Week 4 Deliverable: Real-time resonance fidelity monitoring

Displays live telemetry across all 14 BRNA nodes:
  - Coherence time (ms)
  - ATP metabolic level (%)
  - Resonance fidelity F_R
  - QSP packet throughput
  - HITL approval/drop rate
  - Entanglement pair status

Run: python dashboard.py
     python dashboard.py --static   (single snapshot, no live update)
     python dashboard.py --export   (save snapshot to JSON)
"""

import time
import json
import random
import argparse
import sys
from datetime import datetime
from typing import Dict, List

try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


# ---------------------------------------------------------------------------
# Node definitions — matches Packet Tracer topology
# ---------------------------------------------------------------------------

NODE_DEFINITIONS = {
    "NR-A":      {"ip": "10.0.1.1", "zone": "core",         "role": "neural-repeater"},
    "NR-B":      {"ip": "10.0.1.2", "zone": "core",         "role": "neural-repeater"},
    "NR-C":      {"ip": "10.0.1.3", "zone": "core",         "role": "neural-repeater"},
    "NR-D":      {"ip": "10.0.1.4", "zone": "core",         "role": "hub-router"},
    "NR-E":      {"ip": "10.0.2.1", "zone": "bio",          "role": "neural-repeater"},
    "DNA-Store": {"ip": "10.0.2.2", "zone": "bio",          "role": "dna-storage"},
    "NR-F":      {"ip": "10.0.2.3", "zone": "bio",          "role": "neural-repeater"},
    "HITL-GW":   {"ip": "10.0.3.1", "zone": "hitl",         "role": "hitl-gateway"},
    "Monitor-1": {"ip": "10.0.3.2", "zone": "hitl",         "role": "monitor"},
    "Monitor-2": {"ip": "10.0.3.3", "zone": "hitl",         "role": "monitor"},
    "QNode-A":   {"ip": "10.0.4.1", "zone": "entanglement", "role": "qnode"},
    "QNode-B":   {"ip": "10.0.4.2", "zone": "entanglement", "role": "qnode"},
    "QNode-C":   {"ip": "10.0.4.3", "zone": "entanglement", "role": "qnode"},
    "QNode-D":   {"ip": "10.0.4.4", "zone": "entanglement", "role": "qnode"},
}

ZONE_COLORS = {
    "core":         "cyan",
    "bio":          "green",
    "hitl":         "magenta",
    "entanglement": "yellow",
}


# ---------------------------------------------------------------------------
# Telemetry simulation
# ---------------------------------------------------------------------------

class NodeTelemetry:
    """Simulates live telemetry for a single BRNA node."""

    def __init__(self, node_id: str, definition: dict):
        self.node_id   = node_id
        self.ip        = definition["ip"]
        self.zone      = definition["zone"]
        self.role      = definition["role"]
        self._tick     = 0

        # Baseline values per role
        if self.role == "dna-storage":
            self._base_coherence = 250.0
            self._base_atp       = 95.0
        elif self.role == "hub-router":
            self._base_coherence = 140.0
            self._base_atp       = 88.0
        elif self.role == "hitl-gateway":
            self._base_coherence = 999.0   # classical node — no decoherence
            self._base_atp       = 100.0
        elif self.role == "monitor":
            self._base_coherence = 999.0
            self._base_atp       = 100.0
        elif self.role == "qnode":
            self._base_coherence = 55.0    # short coherence — entanglement only
            self._base_atp       = 70.0
        else:
            self._base_coherence = 110.0
            self._base_atp       = 82.0

        self.packets_sent     = 0
        self.packets_dropped  = 0

    def poll(self) -> dict:
        """Return a fresh telemetry reading."""
        self._tick += 1
        # Add realistic jitter
        noise = random.gauss(0, 0.05)
        coherence = max(10.0, self._base_coherence * (1.0 + noise))
        atp       = max(5.0, min(100.0, self._base_atp + random.gauss(0, 2)))
        fidelity  = min(1.0, (coherence / 100.0) * (atp / 100.0))
        fidelity  = round(fidelity, 4)

        # Simulate occasional packet traffic
        if random.random() < 0.4:
            self.packets_sent += random.randint(1, 5)
        if random.random() < 0.05:
            self.packets_dropped += 1

        status = "OK"
        if fidelity < 0.3:
            status = "CRIT"
        elif fidelity < 0.6:
            status = "WARN"

        return {
            "node_id":          self.node_id,
            "ip":               self.ip,
            "zone":             self.zone,
            "role":             self.role,
            "coherence_ms":     round(coherence, 1),
            "atp_pct":          round(atp, 1),
            "fidelity":         fidelity,
            "packets_sent":     self.packets_sent,
            "packets_dropped":  self.packets_dropped,
            "status":           status,
            "timestamp":        datetime.utcnow().isoformat(),
        }


class NetworkDashboard:
    """Manages telemetry collection across all nodes."""

    def __init__(self):
        self.nodes: Dict[str, NodeTelemetry] = {
            nid: NodeTelemetry(nid, defn)
            for nid, defn in NODE_DEFINITIONS.items()
        }
        self.tick = 0

    def poll_all(self) -> List[dict]:
        self.tick += 1
        return [node.poll() for node in self.nodes.values()]

    def summary_stats(self, readings: List[dict]) -> dict:
        fidelities   = [r["fidelity"] for r in readings]
        total_sent   = sum(r["packets_sent"] for r in readings)
        total_dropped= sum(r["packets_dropped"] for r in readings)
        drop_rate    = (total_dropped / total_sent * 100) if total_sent else 0
        return {
            "avg_fidelity":  round(sum(fidelities) / len(fidelities), 4),
            "min_fidelity":  round(min(fidelities), 4),
            "nodes_ok":      sum(1 for r in readings if r["status"] == "OK"),
            "nodes_warn":    sum(1 for r in readings if r["status"] == "WARN"),
            "nodes_crit":    sum(1 for r in readings if r["status"] == "CRIT"),
            "total_packets": total_sent,
            "drop_rate_pct": round(drop_rate, 2),
            "tick":          self.tick,
        }


# ---------------------------------------------------------------------------
# Rich rendering
# ---------------------------------------------------------------------------

def _status_style(status: str) -> str:
    return {"OK": "green", "WARN": "yellow", "CRIT": "red"}.get(status, "white")


def build_node_table(readings: List[dict]) -> Table:
    t = Table(
        title="BRNA node telemetry",
        box=box.SIMPLE_HEAD,
        show_header=True,
        header_style="bold",
        expand=True,
    )
    t.add_column("Node",        style="bold", width=12)
    t.add_column("Zone",        width=14)
    t.add_column("IP",          width=13)
    t.add_column("Coherence",   justify="right", width=12)
    t.add_column("ATP %",       justify="right", width=8)
    t.add_column("Fidelity",    justify="right", width=10)
    t.add_column("Pkts sent",   justify="right", width=10)
    t.add_column("Dropped",     justify="right", width=9)
    t.add_column("Status",      justify="center", width=8)

    for r in readings:
        zone_color = ZONE_COLORS.get(r["zone"], "white")
        st_color   = _status_style(r["status"])
        fid_bar    = "█" * int(r["fidelity"] * 10) + "░" * (10 - int(r["fidelity"] * 10))
        t.add_row(
            r["node_id"],
            f"[{zone_color}]{r['zone']}[/{zone_color}]",
            r["ip"],
            f"{r['coherence_ms']:.1f} ms",
            f"{r['atp_pct']:.1f}",
            f"[{st_color}]{fid_bar}[/{st_color}] {r['fidelity']:.3f}",
            str(r["packets_sent"]),
            str(r["packets_dropped"]),
            f"[{st_color}]{r['status']}[/{st_color}]",
        )
    return t


def build_summary_panel(stats: dict) -> Panel:
    lines = [
        f"Tick #{stats['tick']:04d}  |  "
        f"Avg fidelity: {stats['avg_fidelity']:.3f}  |  "
        f"Min fidelity: {stats['min_fidelity']:.3f}",
        f"Nodes — OK: {stats['nodes_ok']}  "
        f"WARN: {stats['nodes_warn']}  "
        f"CRIT: {stats['nodes_crit']}  |  "
        f"Total pkts: {stats['total_packets']}  "
        f"Drop rate: {stats['drop_rate_pct']:.2f}%",
    ]
    return Panel("\n".join(lines), title="Network summary", style="blue")


def build_entanglement_panel(readings: List[dict]) -> Panel:
    qnodes = [r for r in readings if r["zone"] == "entanglement"]
    lines = []
    pairs = [("QNode-A", "QNode-B"), ("QNode-C", "QNode-D")]
    node_map = {r["node_id"]: r for r in qnodes}
    for a, b in pairs:
        ra = node_map.get(a, {})
        rb = node_map.get(b, {})
        fa = ra.get("fidelity", 0)
        fb = rb.get("fidelity", 0)
        pair_fid = round((fa + fb) / 2, 3)
        status = "ENTANGLED" if pair_fid > 0.4 else "DECOHERENT"
        color = "green" if status == "ENTANGLED" else "red"
        lines.append(f"  {a} ~~~ {b}   pair_F_R={pair_fid:.3f}  [{color}]{status}[/{color}]")
    return Panel("\n".join(lines), title="Entanglement pairs (QSP Layer 3)", style="yellow")


# ---------------------------------------------------------------------------
# Fallback plain-text display
# ---------------------------------------------------------------------------

def plain_snapshot(readings: List[dict], stats: dict):
    print(f"\n{'='*70}")
    print(f"BRNA Dashboard  tick={stats['tick']}  {datetime.utcnow().isoformat()}")
    print(f"{'='*70}")
    print(f"{'Node':<12} {'Zone':<14} {'IP':<14} {'Coh(ms)':<10} {'ATP%':<7} {'F_R':<8} {'Status'}")
    print("-" * 70)
    for r in readings:
        print(f"{r['node_id']:<12} {r['zone']:<14} {r['ip']:<14} "
              f"{r['coherence_ms']:<10.1f} {r['atp_pct']:<7.1f} "
              f"{r['fidelity']:<8.4f} {r['status']}")
    print(f"\nAvg F_R: {stats['avg_fidelity']}  "
          f"Nodes OK/WARN/CRIT: {stats['nodes_ok']}/{stats['nodes_warn']}/{stats['nodes_crit']}")


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

def run_live(seconds: int = 30):
    """Live dashboard with rich rendering."""
    dashboard = NetworkDashboard()
    readings  = dashboard.poll_all()

    with Live(refresh_per_second=1) as live:
        for _ in range(seconds):
            readings = dashboard.poll_all()
            stats    = dashboard.summary_stats(readings)
            layout   = Table.grid(expand=True)
            layout.add_row(build_summary_panel(stats))
            layout.add_row(build_node_table(readings))
            layout.add_row(build_entanglement_panel(readings))
            live.update(layout)
            time.sleep(1)


def run_static():
    """Single snapshot."""
    dashboard = NetworkDashboard()
    readings  = dashboard.poll_all()
    stats     = dashboard.summary_stats(readings)
    if RICH_AVAILABLE:
        console.print(build_summary_panel(stats))
        console.print(build_node_table(readings))
        console.print(build_entanglement_panel(readings))
    else:
        plain_snapshot(readings, stats)


def run_export(path: str = "dashboard_snapshot.json"):
    """Export snapshot to JSON file."""
    dashboard = NetworkDashboard()
    readings  = dashboard.poll_all()
    stats     = dashboard.summary_stats(readings)
    output    = {"summary": stats, "nodes": readings}
    with open(path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Snapshot exported to {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BRNA Galactic Command Dashboard")
    parser.add_argument("--static", action="store_true", help="Single snapshot")
    parser.add_argument("--export", action="store_true", help="Export JSON snapshot")
    parser.add_argument("--seconds", type=int, default=30, help="Live duration (default 30)")
    args = parser.parse_args()

    if args.export:
        run_export()
    elif args.static or not RICH_AVAILABLE:
        run_static()
    else:
        console.print(Panel(
            "BRNA — Bio-Resonance Network Architecture\n"
            "Galactic Command Dashboard v1.0  |  Press Ctrl+C to exit",
            style="bold blue"
        ))
        try:
            run_live(seconds=args.seconds)
        except KeyboardInterrupt:
            console.print("\n[bold red]Dashboard stopped.[/bold red]")
