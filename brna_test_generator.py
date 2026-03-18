#!/usr/bin/env python3
"""
BRNA Test Scenario Generator
Terminal-based UI for creating and running Bio-Quantum Network test scenarios
Compatible with BRNA Research Portfolio v2.0
"""

import os
import sys
import json
import time
import random
import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================

class NodeType(Enum):
    ROUTER = "router"
    SWITCH = "switch"
    PC = "pc"
    QNODE = "qnode"

class ZoneType(Enum):
    CORE = "core"
    BIO = "bio"
    HITL = "hitl"
    ENTANGLE = "entangle"

class ProtocolType(Enum):
    QSP = "QSP"
    MYCO_RIP = "MYCO-RIP"
    DNA_STORE = "DNA-STORE"
    HITL_CTRL = "HITL-CTRL"
    ICMP = "ICMP"
    PPP = "PPP"
    SPIN_BRIDGE = "SPIN-BRIDGE"
    BLAP = "BLAP"

class TestStatus(Enum):
    PENDING = "⏳ PENDING"
    RUNNING = "▶️ RUNNING"
    PASSED = "✅ PASSED"
    FAILED = "❌ FAILED"
    WARNING = "⚠️ WARNING"
    BLOCKED = "🚫 BLOCKED"

@dataclass
class QuantumState:
    """Quantum state of a bio-node"""
    coherence: float  # 0-100%
    spin_state: str  # ↑↓, ↑↑, ↓↓, superposition
    microtubule_class: str  # A, B, C, S
    frequency: float  # Hz
    decoherence_rate: float  # ns
    bell_state: Optional[str] = None  # |Φ+⟩, |Ψ-⟩, etc.
    entanglement_partner: Optional[str] = None

@dataclass
class BioMetrics:
    """Biological metrics for living nodes"""
    metabolic_rate: float  # ATP consumption
    temperature: float  # Celsius
    ph_level: float
    nutrient_level: float  # 0-100%
    neural_noise: float  # dB
    self_healing: bool = True

@dataclass
class NetworkNode:
    """Network node in BRNA topology"""
    node_id: str
    node_type: NodeType
    zone: ZoneType
    subnet: str
    role: str
    ios_version: str
    status: str  # Active, Standby, Idle, Error
    quantum: Optional[QuantumState] = None
    bio: Optional[BioMetrics] = None
    interfaces: List[Dict] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    protocols: List[ProtocolType] = field(default_factory=list)
    python_file: str = ""

@dataclass
class NetworkLink:
    """Link between nodes"""
    from_node: str
    to_node: str
    link_type: str  # serial, eth, quantum, swap
    label: str
    bandwidth: float = 1000  # Mbps
    latency: float = 1.0  # ms
    resonance_cost: float = 1.0
    active: bool = True

@dataclass
class TestScenario:
    """Complete test scenario definition"""
    name: str
    description: str
    author: str
    created: str
    nodes: Dict[str, NetworkNode] = field(default_factory=dict)
    links: List[NetworkLink] = field(default_factory=list)
    test_steps: List[Dict] = field(default_factory=list)
    expected_results: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

@dataclass
class TestResult:
    """Results from running a test scenario"""
    scenario_name: str
    timestamp: str
    status: TestStatus
    step_results: List[Dict]
    metrics: Dict[str, Any]
    log: List[str]
    error_message: Optional[str] = None


# ============================================================================
# DEFAULT TOPOLOGY (from the HTML simulator)
# ============================================================================

def create_default_topology() -> Dict[str, NetworkNode]:
    """Create the default 16-node topology from the HTML simulator"""
    nodes = {}
    
    # Core routers
    nodes["NR-A"] = NetworkNode(
        node_id="NR-A",
        node_type=NodeType.ROUTER,
        zone=ZoneType.CORE,
        subnet="10.0.1.1/24",
        role="Mesh Router — Neural Repeater A",
        ios_version="Cisco IOS 12.4 / BRNA-OS 3.2",
        status="Active",
        quantum=QuantumState(
            coherence=94.0,
            spin_state="↑↓ Coherent",
            microtubule_class="A",
            frequency=40.0,
            decoherence_rate=2.0
        ),
        bio=BioMetrics(
            metabolic_rate=0.8,
            temperature=37.2,
            ph_level=7.4,
            nutrient_level=92.0,
            neural_noise=0.02
        ),
        interfaces=[
            {"name": "Fa0/0", "ip": "10.0.1.1", "status": "Up"},
            {"name": "Se0/0", "ip": "10.0.1.5", "status": "Up"}
        ],
        metrics={"latency": 2.3, "throughput": 840, "packet_loss": 0.02},
        protocols=[ProtocolType.QSP, ProtocolType.MYCO_RIP, ProtocolType.SPIN_BRIDGE],
        python_file="microtubule.py"
    )
    
    nodes["NR-B"] = NetworkNode(
        node_id="NR-B",
        node_type=NodeType.ROUTER,
        zone=ZoneType.CORE,
        subnet="10.0.1.2/24",
        role="Mesh Router — Neural Repeater B",
        ios_version="Cisco IOS 12.4 / BRNA-OS 3.2",
        status="Active",
        quantum=QuantumState(
            coherence=91.0,
            spin_state="↑↑ Coherent",
            microtubule_class="A",
            frequency=40.0,
            decoherence_rate=2.2
        ),
        bio=BioMetrics(
            metabolic_rate=0.85,
            temperature=37.3,
            ph_level=7.4,
            nutrient_level=88.0,
            neural_noise=0.03
        ),
        interfaces=[
            {"name": "Fa0/0", "ip": "10.0.1.2", "status": "Up"},
            {"name": "Se0/0", "ip": "10.0.1.6", "status": "Up"},
            {"name": "Fa0/1", "ip": "10.0.1.2", "status": "Up"}
        ],
        metrics={"latency": 2.8, "throughput": 790, "packet_loss": 0.04},
        protocols=[ProtocolType.QSP, ProtocolType.MYCO_RIP, ProtocolType.SPIN_BRIDGE],
        python_file="microtubule.py"
    )
    
    nodes["NR-C"] = NetworkNode(
        node_id="NR-C",
        node_type=NodeType.ROUTER,
        zone=ZoneType.CORE,
        subnet="10.0.1.3/24",
        role="Mesh Router — Neural Repeater C",
        ios_version="Cisco IOS 12.4 / BRNA-OS 3.2",
        status="Active",
        quantum=QuantumState(
            coherence=88.0,
            spin_state="↑↓ Partial",
            microtubule_class="B",
            frequency=38.0,
            decoherence_rate=3.0
        ),
        bio=BioMetrics(
            metabolic_rate=0.92,
            temperature=37.5,
            ph_level=7.3,
            nutrient_level=76.0,
            neural_noise=0.07
        ),
        interfaces=[
            {"name": "Fa0/0", "ip": "10.0.1.3", "status": "Up"},
            {"name": "Se0/0", "ip": "10.0.1.7", "status": "Up"}
        ],
        metrics={"latency": 3.1, "throughput": 720, "packet_loss": 0.07},
        protocols=[ProtocolType.QSP, ProtocolType.MYCO_RIP],
        python_file="microtubule.py"
    )
    
    nodes["NR-D"] = NetworkNode(
        node_id="NR-D",
        node_type=NodeType.ROUTER,
        zone=ZoneType.CORE,
        subnet="10.0.1.4/24",
        role="Hub Router — Central Resonance Node",
        ios_version="Cisco IOS 12.4 / BRNA-OS 3.2 [HUB]",
        status="Active",
        quantum=QuantumState(
            coherence=97.0,
            spin_state="↑↓ Superposition",
            microtubule_class="S",
            frequency=42.0,
            decoherence_rate=1.2
        ),
        bio=BioMetrics(
            metabolic_rate=0.75,
            temperature=36.9,
            ph_level=7.4,
            nutrient_level=98.0,
            neural_noise=0.01
        ),
        interfaces=[
            {"name": "Fa0/0", "ip": "10.0.1.4", "status": "Up"},
            {"name": "Fa0/1", "ip": "10.0.1.4", "status": "Up"},
            {"name": "Fa0/2", "ip": "10.0.1.4", "status": "Up"},
            {"name": "Fa1/0", "ip": "10.0.2.254", "status": "Up"},
            {"name": "Fa1/1", "ip": "10.0.3.254", "status": "Up"}
        ],
        metrics={"latency": 1.8, "throughput": 980, "packet_loss": 0.01},
        protocols=[ProtocolType.QSP, ProtocolType.MYCO_RIP, ProtocolType.SPIN_BRIDGE,
                   ProtocolType.DNA_STORE, ProtocolType.HITL_CTRL],
        python_file="microtubule.py + routing.py"
    )
    
    # Bio zone
    nodes["SW-BIO"] = NetworkNode(
        node_id="SW-BIO",
        node_type=NodeType.SWITCH,
        zone=ZoneType.BIO,
        subnet="10.0.2.0/24",
        role="Switch — Mycelial Mesh Fabric",
        ios_version="Cisco IOS 2960",
        status="Active",
        bio=BioMetrics(
            metabolic_rate=0.3,
            temperature=36.5,
            ph_level=7.2,
            nutrient_level=95.0,
            neural_noise=0.01
        ),
        interfaces=[
            {"name": "Gi0/1", "ip": "—", "status": "Up"},
            {"name": "Gi0/2", "ip": "—", "status": "Up"},
            {"name": "Gi0/3", "ip": "—", "status": "Up"},
            {"name": "Gi0/4", "ip": "—", "status": "Up"},
            {"name": "Gi0/5", "ip": "—", "status": "Up"}
        ],
        metrics={"port_util": 62, "mac_table": 8, "throughput": 1000},
        protocols=[ProtocolType.MYCO_RIP, ProtocolType.BLAP],
        python_file="mycelial_mesh.py"
    )
    
    nodes["DNA-Store"] = NetworkNode(
        node_id="DNA-Store",
        node_type=NodeType.PC,
        zone=ZoneType.BIO,
        subnet="10.0.2.2",
        role="PC — DNA Data Lake",
        ios_version="DNA-OS 1.4",
        status="Active",
        interfaces=[
            {"name": "NIC0", "ip": "10.0.2.2", "status": "Up"},
            {"name": "BIO-NIC", "ip": "—", "status": "Up"}
        ],
        metrics={
            "write_latency": 800,
            "throughput": 2100,
            "error_rate": 1e-8,
            "storage_used": 34
        },
        protocols=[ProtocolType.DNA_STORE],
        python_file="dna_store.py"
    )
    
    # Add remaining nodes (simplified for brevity)
    node_names = ["NR-E", "NR-F", "PC-Bio1", "PC-Bio2", "SW-HITL", "HITL-GW",
                  "Monitor-1", "Monitor-2", "PC-HITL1", "PC-HITL2",
                  "QNode-A", "QNode-B", "QNode-C", "QNode-D"]
    
    for name in node_names:
        if name not in nodes:
            nodes[name] = NetworkNode(
                node_id=name,
                node_type=NodeType.PC if "PC" in name else 
                          NodeType.QNODE if "QNode" in name else
                          NodeType.SWITCH if "SW" in name else NodeType.PC,
                zone=ZoneType.BIO if "Bio" in name or "NR-E" in name or "NR-F" in name or "DNA" in name else
                      ZoneType.HITL if "HITL" in name or "Monitor" in name else
                      ZoneType.ENTANGLE if "QNode" in name else ZoneType.CORE,
                subnet=f"10.0.{random.randint(1,4)}.{random.randint(1,250)}",
                role=f"Test node {name}",
                ios_version="Generic",
                status="Active",
                metrics={},
                protocols=[ProtocolType.QSP],
                python_file="generic.py"
            )
    
    return nodes

def create_default_links() -> List[NetworkLink]:
    """Create default links from the HTML simulator"""
    return [
        NetworkLink("NR-A", "NR-B", "serial", "Serial", latency=2.5, resonance_cost=1.2),
        NetworkLink("NR-B", "NR-C", "serial", "Serial", latency=2.7, resonance_cost=1.3),
        NetworkLink("NR-A", "NR-D", "eth", "Fa0/1", latency=1.0, resonance_cost=0.8),
        NetworkLink("NR-B", "NR-D", "eth", "Fa1/0", latency=1.1, resonance_cost=0.9),
        NetworkLink("NR-C", "NR-D", "eth", "Fa1/0", latency=1.2, resonance_cost=1.0),
        NetworkLink("NR-D", "SW-BIO", "eth", "Fa1/0", latency=1.5, resonance_cost=1.1),
        NetworkLink("NR-D", "SW-HITL", "eth", "Fa1/1", latency=1.5, resonance_cost=1.1),
        NetworkLink("SW-BIO", "NR-E", "eth", "Gi0/1", latency=2.0, resonance_cost=1.5),
        NetworkLink("SW-BIO", "DNA-Store", "eth", "Gi0/2", latency=2.0, resonance_cost=1.5),
        NetworkLink("SW-BIO", "NR-F", "eth", "Gi0/3", latency=2.1, resonance_cost=1.6),
        NetworkLink("SW-BIO", "PC-Bio1", "eth", "Gi0/4", latency=2.2, resonance_cost=1.7),
        NetworkLink("SW-BIO", "PC-Bio2", "eth", "Gi0/5", latency=2.2, resonance_cost=1.7),
        NetworkLink("SW-HITL", "HITL-GW", "eth", "Gi0/1", latency=2.0, resonance_cost=1.5),
        NetworkLink("SW-HITL", "Monitor-1", "eth", "Gi0/2", latency=2.0, resonance_cost=1.5),
        NetworkLink("SW-HITL", "Monitor-2", "eth", "Gi0/3", latency=2.1, resonance_cost=1.6),
        NetworkLink("SW-HITL", "PC-HITL1", "eth", "Gi0/4", latency=2.1, resonance_cost=1.6),
        NetworkLink("SW-HITL", "PC-HITL2", "eth", "Gi0/5", latency=2.2, resonance_cost=1.7),
        NetworkLink("QNode-A", "QNode-B", "quantum", "QSP pair 1", latency=0.0, resonance_cost=0.1),
        NetworkLink("QNode-C", "QNode-D", "quantum", "QSP pair 2", latency=0.0, resonance_cost=0.1),
        NetworkLink("QNode-B", "QNode-C", "swap", "Swap", latency=0.5, resonance_cost=0.5),
    ]


# ============================================================================
# PRE-DEFINED TEST SCENARIOS
# ============================================================================

def get_scenario_orch_or_coherence() -> TestScenario:
    """Scenario 1: Test Orch OR coherence maintenance"""
    scenario = TestScenario(
        name="Orch OR Coherence Test",
        description="Verify that neural repeaters maintain quantum coherence above 85% under normal load",
        author="BRNA Research Team",
        created=datetime.datetime.now().isoformat(),
        tags=["core", "quantum", "coherence", "orch-or"]
    )
    
    scenario.nodes = create_default_topology()
    scenario.links = create_default_links()
    
    scenario.test_steps = [
        {
            "step": 1,
            "name": "Initialize microtubule bundles",
            "command": "init_microtubule()",
            "target": "NR-A",
            "expected": "Coherence > 90%"
        },
        {
            "step": 2,
            "name": "Apply Orch OR trigger",
            "command": "apply_orch_trigger(threshold=0.95)",
            "target": "NR-A,NR-B,NR-D",
            "expected": "OR collapse probability < 5%"
        },
        {
            "step": 3,
            "name": "Measure decoherence rate",
            "command": "measure_decoherence(duration=1000)",
            "target": "all_core_routers",
            "expected": "Decoherence < 3.0 ns"
        },
        {
            "step": 4,
            "name": "Apply metabolic stress",
            "command": "reduce_nutrients(level=50)",
            "target": "NR-C",
            "expected": "Coherence drop < 15%"
        }
    ]
    
    scenario.expected_results = {
        "min_coherence": 85.0,
        "max_decoherence": 3.0,
        "or_collapse_rate": 0.05,
        "recovery_time": 500  # ms
    }
    
    return scenario

def get_scenario_dna_store_recovery() -> TestScenario:
    """Scenario 2: Test DNA storage with error correction"""
    scenario = TestScenario(
        name="DNA Store Recovery Test",
        description="Verify Reed-Solomon error correction can recover data with 10% corruption",
        author="BRNA Research Team",
        created=datetime.datetime.now().isoformat(),
        tags=["bio", "storage", "dna", "error-correction"]
    )
    
    scenario.nodes = create_default_topology()
    scenario.links = create_default_links()
    
    scenario.test_steps = [
        {
            "step": 1,
            "name": "Write test data to DNA",
            "command": "dna_write(payload='TEST_PATTERN_0xF3A7')",
            "target": "DNA-Store",
            "expected": "Write successful"
        },
        {
            "step": 2,
            "name": "Apply Reed-Solomon encoding",
            "command": "rs_encode(symbols=(255,223))",
            "target": "DNA-Store",
            "expected": "Redundancy 14%"
        },
        {
            "step": 3,
            "name": "Simulate sequence corruption",
            "command": "corrupt_dna(rate=0.10, random=true)",
            "target": "DNA-Store",
            "expected": "10% errors introduced"
        },
        {
            "step": 4,
            "name": "Recover data with ECC",
            "command": "rs_decode()",
            "target": "DNA-Store",
            "expected": "100% recovery"
        }
    ]
    
    scenario.expected_results = {
        "recovery_rate": 100.0,
        "max_corruption_tolerated": 16,  # symbols
        "storage_density": "10^18 bytes/cc",
        "write_latency": 800  # ms
    }
    
    return scenario

def get_scenario_entanglement_swapping() -> TestScenario:
    """Scenario 3: Test entanglement swapping across nodes"""
    scenario = TestScenario(
        name="Entanglement Swapping Test",
        description="Create quantum link between non-adjacent nodes via swapping",
        author="BRNA Research Team",
        created=datetime.datetime.now().isoformat(),
        tags=["quantum", "entanglement", "swapping", "non-local"]
    )
    
    scenario.nodes = create_default_topology()
    scenario.links = create_default_links()
    
    scenario.test_steps = [
        {
            "step": 1,
            "name": "Create Bell pair A-B",
            "command": "create_bell_pair(state='|Φ+⟩')",
            "target": "QNode-A,QNode-B",
            "expected": "Fidelity > 98%"
        },
        {
            "step": 2,
            "name": "Create Bell pair C-D",
            "command": "create_bell_pair(state='|Ψ-⟩')",
            "target": "QNode-C,QNode-D",
            "expected": "Fidelity > 98%"
        },
        {
            "step": 3,
            "name": "Perform entanglement swap B-C",
            "command": "entanglement_swap(node_b, node_c)",
            "target": "QNode-B,QNode-C",
            "expected": "Swap success > 90%"
        },
        {
            "step": 4,
            "name": "Verify A-D entanglement",
            "command": "bell_test(node_a, node_d)",
            "target": "QNode-A,QNode-D",
            "expected": "CHSH > 2.7"
        }
    ]
    
    scenario.expected_results = {
        "swap_success_rate": 94.0,
        "chsh_value": 2.82,
        "fidelity": 99.1,
        "latency": 0.0  # ms
    }
    
    return scenario

def get_scenario_hitl_override() -> TestScenario:
    """Scenario 4: Test HITL governance and override"""
    scenario = TestScenario(
        name="HITL Override Test",
        description="Verify human operator can override critical routing decisions",
        author="BRNA Research Team",
        created=datetime.datetime.now().isoformat(),
        tags=["hitl", "governance", "ethics", "override"]
    )
    
    scenario.nodes = create_default_topology()
    scenario.links = create_default_links()
    
    scenario.test_steps = [
        {
            "step": 1,
            "name": "Generate critical packet",
            "command": "send_critical(priority='CRITICAL', orch_collapse=0.98)",
            "target": "NR-A",
            "expected": "Ethics engine flags packet"
        },
        {
            "step": 2,
            "name": "Queue for HITL review",
            "command": "hitl_queue()",
            "target": "HITL-GW",
            "expected": "Packet queued, operator notified"
        },
        {
            "step": 3,
            "name": "Simulate operator approval",
            "command": "operator_override(decision='APPROVE')",
            "target": "PC-HITL1",
            "expected": "Override recorded"
        },
        {
            "step": 4,
            "name": "Verify packet delivery",
            "command": "check_delivery()",
            "target": "NR-D",
            "expected": "Packet delivered"
        }
    ]
    
    scenario.expected_results = {
        "override_latency": 30.0,  # seconds max
        "audit_log_updated": True,
        "ethics_violations": 0
    }
    
    return scenario

def get_scenario_mycelial_self_heal() -> TestScenario:
    """Scenario 5: Test mycelial mesh self-healing"""
    scenario = TestScenario(
        name="Mycelial Self-Healing Test",
        description="Verify mesh reroutes around failed links using fungal growth algorithms",
        author="BRNA Research Team",
        created=datetime.datetime.now().isoformat(),
        tags=["mycelial", "mesh", "self-healing", "resilience"]
    )
    
    scenario.nodes = create_default_topology()
    scenario.links = create_default_links()
    
    scenario.test_steps = [
        {
            "step": 1,
            "name": "Establish baseline routing",
            "command": "compute_all_paths()",
            "target": "SW-BIO",
            "expected": "All paths optimal"
        },
        {
            "step": 2,
            "name": "Simulate link failure",
            "command": "fail_link(link='SW-BIO-NR-E')",
            "target": "SW-BIO",
            "expected": "Link down, rerouting triggered"
        },
        {
            "step": 3,
            "name": "Measure healing time",
            "command": "monitor_reroute()",
            "target": "mycelial_mesh",
            "expected": "Healing < 50 ms"
        },
        {
            "step": 4,
            "name": "Verify new path",
            "command": "trace_route(from='NR-A', to='NR-E')",
            "target": "network",
            "expected": "Alternative path active"
        }
    ]
    
    scenario.expected_results = {
        "healing_time": 50,  # ms
        "path_redundancy": 3,
        "packet_loss_during_failover": 0.5  # %
    }
    
    return scenario

def get_scenario_qsp_handshake() -> TestScenario:
    """Scenario 6: Test QSP 3-way handshake"""
    scenario = TestScenario(
        name="QSP Handshake Test",
        description="Verify Quantum Sensory Protocol establishes connection via phase synchronization",
        author="BRNA Research Team",
        created=datetime.datetime.now().isoformat(),
        tags=["protocol", "qsp", "handshake", "phase-sync"]
    )
    
    scenario.nodes = create_default_topology()
    scenario.links = create_default_links()
    
    scenario.test_steps = [
        {
            "step": 1,
            "name": "Send QSP SYN",
            "command": "qsp_send(flags='SYN', resonance_id='0x4A2F')",
            "target": "NR-A",
            "expected": "SYN sent"
        },
        {
            "step": 2,
            "name": "Receive SYN-ACK",
            "command": "qsp_receive()",
            "target": "NR-D",
            "expected": "SYN-ACK with fidelity 97%"
        },
        {
            "step": 3,
            "name": "Complete handshake",
            "command": "qsp_send(flags='ACK')",
            "target": "NR-A",
            "expected": "Session established"
        },
        {
            "step": 4,
            "name": "Verify phase sync",
            "command": "measure_phase_coherence()",
            "target": "NR-A,NR-D",
            "expected": "Phase difference < 0.1 rad"
        }
    ]
    
    scenario.expected_results = {
        "handshake_time": 2.3,  # ms
        "phase_coherence": 0.99,
        "fidelity": 97.0  # %
    }
    
    return scenario

def get_scenario_paradox_prevention() -> TestScenario:
    """Scenario 7: Test Paradox Prevention Protocol"""
    scenario = TestScenario(
        name="Paradox Prevention Test",
        description="Verify PPP drops causality-violating packets",
        author="BRNA Research Team",
        created=datetime.datetime.now().isoformat(),
        tags=["paradox", "causality", "ppp", "chronological"]
    )
    
    scenario.nodes = create_default_topology()
    scenario.links = create_default_links()
    
    scenario.test_steps = [
        {
            "step": 1,
            "name": "Generate normal packet",
            "command": "send_packet(timestamp='+10ms')",
            "target": "NR-A",
            "expected": "Packet allowed"
        },
        {
            "step": 2,
            "name": "Generate causality violation",
            "command": "send_packet(timestamp='-50ms', entropy_decrease=0.2)",
            "target": "NR-B",
            "expected": "Packet flagged"
        },
        {
            "step": 3,
            "name": "Verify PPP drop",
            "command": "check_ppp_filter()",
            "target": "HITL-GW",
            "expected": "Packet dropped, violation logged"
        },
        {
            "step": 4,
            "name": "Check entropy guard",
            "command": "measure_entropy_change()",
            "target": "destination",
            "expected": "Local entropy unchanged"
        }
    ]
    
    scenario.expected_results = {
        "drop_rate_violations": 100.0,  # %
        "false_positive_rate": 0.0,
        "audit_log_entries": 1
    }
    
    return scenario

def get_scenario_metabolic_cooling() -> TestScenario:
    """Scenario 8: Test metabolic cooling simulation"""
    scenario = TestScenario(
        name="Metabolic Cooling Test",
        description="Verify temperature control maintains coherence",
        author="BRNA Research Team",
        created=datetime.datetime.now().isoformat(),
        tags=["bio", "metabolic", "cooling", "temperature"]
    )
    
    scenario.nodes = create_default_topology()
    scenario.links = create_default_links()
    
    scenario.test_steps = [
        {
            "step": 1,
            "name": "Set baseline temperature",
            "command": "set_temperature(temp=37.0)",
            "target": "NR-A",
            "expected": "Coherence 94%"
        },
        {
            "step": 2,
            "name": "Simulate overheating",
            "command": "increase_temp(delta=3.5)",
            "target": "NR-A",
            "expected": "Coherence drops"
        },
        {
            "step": 3,
            "name": "Activate metabolic cooling",
            "command": "metabolic_cooling(intensity=0.8)",
            "target": "NR-A",
            "expected": "Temperature decreases"
        },
        {
            "step": 4,
            "name": "Verify recovery",
            "command": "measure_coherence()",
            "target": "NR-A",
            "expected": "Coherence > 90%"
        }
    ]
    
    scenario.expected_results = {
        "max_temp": 39.0,  # Celsius
        "cooling_rate": 0.5,  # °C/s
        "min_coherence_during_stress": 70.0  # %
    }
    
    return scenario

def get_scenario_galactic_routing() -> TestScenario:
    """Scenario 9: Test interstellar routing"""
    scenario = TestScenario(
        name="Galactic Routing Test",
        description="Simulate routing from Earth to Proxima Centauri with zero latency",
        author="BRNA Research Team",
        created=datetime.datetime.now().isoformat(),
        tags=["interstellar", "routing", "zero-latency", "entanglement"]
    )
    
    scenario.nodes = create_default_topology()
    scenario.links = create_default_links()
    
    # Add simulated Proxima node
    scenario.nodes["Proxima-Centauri"] = NetworkNode(
        node_id="Proxima-Centauri",
        node_type=NodeType.QNODE,
        zone=ZoneType.ENTANGLE,
        subnet="10.0.5.1/32",
        role="Interstellar Relay — Proxima Centauri",
        ios_version="BRNA-OS Interstellar",
        status="Active",
        quantum=QuantumState(
            coherence=92.0,
            spin_state="↑↓ Entangled",
            microtubule_class="X",
            frequency=40.0,
            decoherence_rate=5.0,
            bell_state="|Φ+⟩"
        ),
        protocols=[ProtocolType.QSP, ProtocolType.PPP],
        python_file="interstellar_relay.py"
    )
    
    scenario.links.append(
        NetworkLink("QNode-D", "Proxima-Centauri", "quantum", "Interstellar QSP", 
                    latency=0.0, resonance_cost=0.01)
    )
    
    scenario.test_steps = [
        {
            "step": 1,
            "name": "Establish entanglement chain",
            "command": "create_entanglement_chain(A->B->C->D->Proxima)",
            "target": "entanglement_zone",
            "expected": "Chain length 5, all entangled"
        },
        {
            "step": 2,
            "name": "Send packet to Proxima",
            "command": "send_packet_qsp(payload='HELLO_PROXIMA')",
            "target": "NR-A",
            "expected": "Packet synchronized"
        },
        {
            "step": 3,
            "name": "Measure arrival time",
            "command": "measure_arrival()",
            "target": "Proxima-Centauri",
            "expected": "Δt ≈ 0 ms"
        },
        {
            "step": 4,
            "name": "Verify data integrity",
            "command": "compare_payload()",
            "target": "Proxima-Centauri",
            "expected": "Payload match"
        }
    ]
    
    scenario.expected_results = {
        "latency": 0.0,  # ms
        "distance": "4.24 light years",
        "fidelity": 92.0,  # %
        "throughput": 840  # Mbps
    }
    
    return scenario

def get_scenario_resonance_cost_routing() -> TestScenario:
    """Scenario 10: Test resonance cost routing algorithm"""
    scenario = TestScenario(
        name="Resonance Cost Routing Test",
        description="Verify modified Dijkstra with C_R metric finds optimal path",
        author="BRNA Research Team",
        created=datetime.datetime.now().isoformat(),
        tags=["routing", "resonance", "dijkstra", "cost"]
    )
    
    scenario.nodes = create_default_topology()
    scenario.links = create_default_links()
    
    scenario.test_steps = [
        {
            "step": 1,
            "name": "Calculate resonance costs",
            "command": "compute_resonance_costs()",
            "target": "all_links",
            "expected": "C_R values computed"
        },
        {
            "step": 2,
            "name": "Run modified Dijkstra",
            "command": "dijkstra_resonance(source='NR-A', target='DNA-Store')",
            "target": "NR-D",
            "expected": "Path found with min C_R"
        },
        {
            "step": 3,
            "name": "Compare with shortest path",
            "command": "compare_paths()",
            "target": "routing_engine",
            "expected": "Resonance path differs if coherence low"
        },
        {
            "step": 4,
            "name": "Verify path quality",
            "command": "measure_path_fidelity()",
            "target": "selected_path",
            "expected": "F_R > 90%"
        }
    ]
    
    scenario.expected_results = {
        "resonance_cost_formula": "C_R = sum(1/coherence_time + metabolic_overhead)",
        "optimal_path": "NR-A → NR-D → SW-BIO → DNA-Store",
        "total_cost": 4.6,
        "fidelity": 94.0  # %
    }
    
    return scenario


# ============================================================================
# SCENARIO DATABASE
# ============================================================================

SCENARIO_DATABASE = {
    "1": get_scenario_orch_or_coherence,
    "2": get_scenario_dna_store_recovery,
    "3": get_scenario_entanglement_swapping,
    "4": get_scenario_hitl_override,
    "5": get_scenario_mycelial_self_heal,
    "6": get_scenario_qsp_handshake,
    "7": get_scenario_paradox_prevention,
    "8": get_scenario_metabolic_cooling,
    "9": get_scenario_galactic_routing,
    "10": get_scenario_resonance_cost_routing
}


# ============================================================================
# SIMULATION ENGINE
# ============================================================================

class BRNASimulator:
    """Simulates BRNA network behavior for test scenarios"""
    
    def __init__(self):
        self.nodes = {}
        self.links = []
        self.test_results = []
        self.log = []
        self.rng = random.Random(42)  # Seed for reproducibility
    
    def load_scenario(self, scenario: TestScenario):
        """Load a test scenario"""
        self.nodes = scenario.nodes
        self.links = scenario.links
        self.log.append(f"Loaded scenario: {scenario.name}")
        self.log.append(f"  Nodes: {len(self.nodes)}")
        self.log.append(f"  Links: {len(self.links)}")
    
    def run_scenario(self, scenario: TestScenario) -> TestResult:
        """Run a test scenario and return results"""
        self.load_scenario(scenario)
        
        step_results = []
        start_time = time.time()
        
        self.log.append("=" * 60)
        self.log.append(f"RUNNING SCENARIO: {scenario.name}")
        self.log.append("=" * 60)
        
        for step in scenario.test_steps:
            self.log.append(f"\nStep {step['step']}: {step['name']}")
            result = self._execute_step(step)
            step_results.append(result)
            
            if result["status"] == "FAILED" and step.get("critical", False):
                self.log.append("Critical step failed - aborting scenario")
                break
        
        end_time = time.time()
        
        # Collect metrics
        metrics = self._collect_metrics()
        metrics["duration_seconds"] = round(end_time - start_time, 2)
        
        # Determine overall status
        failed_steps = [s for s in step_results if s["status"] == "FAILED"]
        warning_steps = [s for s in step_results if s["status"] == "WARNING"]
        
        if failed_steps:
            status = TestStatus.FAILED
        elif warning_steps:
            status = TestStatus.WARNING
        else:
            status = TestStatus.PASSED
        
        result = TestResult(
            scenario_name=scenario.name,
            timestamp=datetime.datetime.now().isoformat(),
            status=status,
            step_results=step_results,
            metrics=metrics,
            log=self.log.copy()
        )
        
        self.test_results.append(result)
        return result
    
    def _execute_step(self, step: Dict) -> Dict:
        """Execute a single test step"""
        self.log.append(f"  Command: {step['command']}")
        self.log.append(f"  Target: {step['target']}")
        
        # Simulate execution time
        time.sleep(0.5)
        
        # Generate result based on step type and randomness
        success_prob = 0.95  # 95% success rate for simulation
        
        if "decoherence" in step['name'].lower():
            success_prob = 0.90
        elif "corruption" in step['name'].lower():
            success_prob = 0.98
        elif "swap" in step['name'].lower():
            success_prob = 0.94
        
        if self.rng.random() < success_prob:
            status = "PASSED"
            details = f"✓ {step['expected']} achieved"
            self.log.append(f"  Result: {details}")
        else:
            status = "FAILED" if self.rng.random() < 0.5 else "WARNING"
            details = f"✗ Expected: {step['expected']}, got: {self.rng.uniform(50, 95):.1f}%"
            self.log.append(f"  Result: {details}")
        
        # Collect metrics
        measured = {}
        if "coherence" in step['command']:
            measured["coherence"] = round(self.rng.uniform(85, 98), 1)
        if "latency" in step['command']:
            measured["latency"] = round(self.rng.uniform(0, 5), 2)
        if "fidelity" in step['command']:
            measured["fidelity"] = round(self.rng.uniform(90, 99), 1)
        
        return {
            "step": step['step'],
            "name": step['name'],
            "status": status,
            "details": details,
            "measured": measured
        }
    
    def _collect_metrics(self) -> Dict:
        """Collect network metrics"""
        metrics = {
            "avg_coherence": 0,
            "total_nodes": len(self.nodes),
            "active_nodes": 0,
            "avg_latency": 0,
            "entanglement_pairs": 0
        }
        
        coherence_sum = 0
        coherence_count = 0
        latency_sum = 0
        latency_count = 0
        
        for node in self.nodes.values():
            if node.status == "Active":
                metrics["active_nodes"] += 1
            
            if node.quantum and node.quantum.coherence:
                coherence_sum += node.quantum.coherence
                coherence_count += 1
            
            if node.quantum and node.quantum.bell_state:
                metrics["entanglement_pairs"] += 1
        
        for link in self.links:
            if hasattr(link, 'latency'):
                latency_sum += link.latency
                latency_count += 1
        
        if coherence_count > 0:
            metrics["avg_coherence"] = round(coherence_sum / coherence_count, 1)
        
        if latency_count > 0:
            metrics["avg_latency"] = round(latency_sum / latency_count, 2)
        
        metrics["total_links"] = len(self.links)
        metrics["quantum_links"] = sum(1 for l in self.links if l.link_type in ["quantum", "swap"])
        
        return metrics


# ============================================================================
# TERMINAL UI
# ============================================================================

class TerminalUI:
    """Text-based terminal UI for BRNA test scenario generator"""
    
    def __init__(self):
        self.simulator = BRNASimulator()
        self.current_scenario = None
        self.last_result = None
        
        # ANSI color codes
        self.CLEAR = "\033[2J\033[H"
        self.RESET = "\033[0m"
        self.BOLD = "\033[1m"
        self.RED = "\033[91m"
        self.GREEN = "\033[92m"
        self.YELLOW = "\033[93m"
        self.BLUE = "\033[94m"
        self.PURPLE = "\033[95m"
        self.CYAN = "\033[96m"
        self.GRAY = "\033[90m"
        self.WHITE = "\033[97m"
        
        self.use_color = sys.stdout.isatty()
    
    def _c(self, text: str, color: str = "") -> str:
        """Add color to text if supported"""
        if self.use_color and color:
            return f"{color}{text}{self.RESET}"
        return text
    
    def clear_screen(self):
        """Clear the terminal screen"""
        if self.use_color:
            print(self.CLEAR, end="")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Print a header"""
        width = 80
        print(self._c("=" * width, self.BLUE))
        print(self._c(f"{title:^{width}}", self.BOLD + self.WHITE))
        print(self._c("=" * width, self.BLUE))
    
    def print_menu(self):
        """Print main menu"""
        self.clear_screen()
        self.print_header("🧬 BRNA TEST SCENARIO GENERATOR v2.0")
        print()
        print(self._c("Bio-Resonance Network Architecture", self.CYAN))
        print(self._c("Terminal-based Test & Simulation Interface", self.GRAY))
        print()
        print(self._c("📋 MAIN MENU", self.BOLD))
        print()
        print(f"  {self._c('1', self.GREEN)}. Run Pre-defined Test Scenario")
        print(f"  {self._c('2', self.GREEN)}. Create Custom Scenario")
        print(f"  {self._c('3', self.GREEN)}. View Results")
        print(f"  {self._c('4', self.GREEN)}. Export Results")
        print(f"  {self._c('5', self.GREEN)}. Network Status")
        print(f"  {self._c('6', self.GREEN)}. About BRNA")
        print(f"  {self._c('0', self.RED)}. Exit")
        print()
        print(self._c("-" * 50, self.GRAY))
    
    def list_scenarios(self):
        """List all pre-defined scenarios"""
        self.clear_screen()
        self.print_header("📋 PRE-DEFINED TEST SCENARIOS")
        print()
        
        for key, scenario_func in SCENARIO_DATABASE.items():
            scenario = scenario_func()
            status = ""
            if self.last_result and self.last_result.scenario_name == scenario.name:
                status = self._c(f" [{self.last_result.status.value}]", 
                                 self.GREEN if self.last_result.status == TestStatus.PASSED else
                                 self.RED if self.last_result.status == TestStatus.FAILED else
                                 self.YELLOW)
            
            print(f"  {self._c(key, self.YELLOW)}. {scenario.name}{status}")
            print(f"     {self._c(scenario.description, self.GRAY)}")
            print(f"     Tags: {', '.join(scenario.tags)}")
            print()
        
        print(self._c("-" * 50, self.GRAY))
        print(f"  {self._c('b', self.BLUE)}. Back to Main Menu")
        print()
    
    def run_scenario_menu(self):
        """Menu for running pre-defined scenarios"""
        while True:
            self.list_scenarios()
            choice = input(self._c("Select scenario (1-10, b): ", self.GREEN)).strip().lower()
            
            if choice == 'b':
                return
            
            if choice in SCENARIO_DATABASE:
                scenario = SCENARIO_DATABASE[choice]()
                self.run_scenario_with_progress(scenario)
                input(self._c("\nPress Enter to continue...", self.GRAY))
            else:
                print(self._c("Invalid choice. Press Enter to continue...", self.RED))
                input()
    
    def run_scenario_with_progress(self, scenario: TestScenario):
        """Run a scenario with progress display"""
        self.clear_screen()
        self.print_header(f"▶️ RUNNING: {scenario.name}")
        print()
        print(self._c(f"Description: {scenario.description}", self.GRAY))
        print(self._c(f"Author: {scenario.author}", self.GRAY))
        print(self._c(f"Steps: {len(scenario.test_steps)}", self.GRAY))
        print()
        
        # Progress bar
        for i in range(4):
            print(self._c("█" * (i+1) + "▒" * (3-i) + f"  Initializing...", self.CYAN))
            time.sleep(0.2)
            print(f"\033[F\033[K", end="")  # Move up and clear line
        
        # Run simulation
        result = self.simulator.run_scenario(scenario)
        self.last_result = result
        
        # Display results
        self.display_results(result)
    
    def display_results(self, result: TestResult):
        """Display test results"""
        print()
        self.print_header(f"📊 TEST RESULTS: {result.scenario_name}")
        print()
        
        # Status
        status_color = self.GREEN if result.status == TestStatus.PASSED else \
                       self.RED if result.status == TestStatus.FAILED else \
                       self.YELLOW
        print(f"  Overall Status: {self._c(result.status.value, status_color)}")
        print(f"  Timestamp: {result.timestamp}")
        print(f"  Duration: {result.metrics.get('duration_seconds', 0)} seconds")
        print()
        
        # Step results
        print(self._c("  Step Results:", self.BOLD))
        for step in result.step_results:
            step_color = self.GREEN if step['status'] == "PASSED" else \
                        self.RED if step['status'] == "FAILED" else \
                        self.YELLOW
            status_symbol = "✓" if step['status'] == "PASSED" else "✗" if step['status'] == "FAILED" else "⚠"
            print(f"    {self._c(status_symbol, step_color)} Step {step['step']}: {step['name']} - {step['status']}")
            if step.get('measured'):
                for k, v in step['measured'].items():
                    print(f"      {k}: {v}")
        
        print()
        
        # Network metrics
        print(self._c("  Network Metrics:", self.BOLD))
        for key, value in result.metrics.items():
            if key != "duration_seconds":
                print(f"    {key}: {value}")
        
        print()
        
        # Last few log entries
        print(self._c("  Recent Log:", self.BOLD))
        for entry in result.log[-5:]:
            print(f"    {entry}")
    
    def custom_scenario_menu(self):
        """Menu for creating custom scenarios"""
        self.clear_screen()
        self.print_header("🔧 CREATE CUSTOM SCENARIO")
        print()
        print(self._c("This feature allows you to create custom test scenarios.", self.GRAY))
        print(self._c("You'll be guided through the process step by step.", self.GRAY))
        print()
        
        name = input(self._c("Scenario name: ", self.GREEN)).strip()
        if not name:
            print(self._c("Cancelled.", self.RED))
            input("Press Enter to continue...")
            return
        
        desc = input(self._c("Description: ", self.GREEN)).strip()
        
        print()
        print(self._c("Select test steps to include (comma-separated):", self.YELLOW))
        print("  1. Orch OR Coherence Test")
        print("  2. DNA Store Recovery")
        print("  3. Entanglement Swapping")
        print("  4. HITL Override")
        print("  5. Mycelial Self-Healing")
        print("  6. QSP Handshake")
        print("  7. Paradox Prevention")
        print("  8. Metabolic Cooling")
        print("  9. Galactic Routing")
        print("  10. Resonance Cost Routing")
        
        steps_choice = input(self._c("Steps: ", self.GREEN)).strip()
        
        # Create custom scenario (simplified)
        custom_scenario = TestScenario(
            name=name,
            description=desc,
            author="Custom User",
            created=datetime.datetime.now().isoformat(),
            tags=["custom"]
        )
        
        # Add selected steps (simplified - would need full implementation)
        custom_scenario.test_steps = [
            {"step": i+1, "name": f"Custom step {i+1}", "command": "custom_command()", 
             "target": "all", "expected": "success"}
            for i in range(min(5, len(steps_choice.split(',')) if steps_choice else 1))
        ]
        
        custom_scenario.nodes = create_default_topology()
        custom_scenario.links = create_default_links()
        
        print()
        print(self._c(f"Custom scenario '{name}' created with {len(custom_scenario.test_steps)} steps.", self.GREEN))
        
        run_now = input(self._c("Run now? (y/n): ", self.GREEN)).strip().lower()
        if run_now == 'y':
            self.run_scenario_with_progress(custom_scenario)
        
        input(self._c("\nPress Enter to continue...", self.GRAY))
    
    def view_results_menu(self):
        """View saved results"""
        self.clear_screen()
        self.print_header("📜 TEST RESULTS HISTORY")
        print()
        
        if not self.simulator.test_results:
            print(self._c("  No test results available.", self.YELLOW))
            print("  Run a test scenario first to see results.")
        else:
            for i, result in enumerate(self.simulator.test_results, 1):
                status_color = self.GREEN if result.status == TestStatus.PASSED else \
                              self.RED if result.status == TestStatus.FAILED else \
                              self.YELLOW
                print(f"  {i}. {result.scenario_name}")
                print(f"     {self._c(result.status.value, status_color)} - {result.timestamp[:19]}")
                print(f"     Duration: {result.metrics.get('duration_seconds', 0)}s, "
                      f"Nodes: {result.metrics.get('active_nodes', 0)}/{result.metrics.get('total_nodes', 0)}")
                print()
        
        print(self._c("-" * 50, self.GRAY))
        print(f"  {self._c('b', self.BLUE)}. Back to Main Menu")
        print()
        
        choice = input(self._c("Enter number to view details, or b: ", self.GREEN)).strip().lower()
        
        if choice != 'b' and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.simulator.test_results):
                self.display_results(self.simulator.test_results[idx])
                input(self._c("\nPress Enter to continue...", self.GRAY))
    
    def export_results_menu(self):
        """Export results to file"""
        self.clear_screen()
        self.print_header("💾 EXPORT RESULTS")
        print()
        
        if not self.simulator.test_results:
            print(self._c("  No test results to export.", self.YELLOW))
            input("Press Enter to continue...")
            return
        
        filename = f"brna_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "exported": datetime.datetime.now().isoformat(),
            "results": []
        }
        
        for result in self.simulator.test_results:
            export_data["results"].append({
                "scenario": result.scenario_name,
                "timestamp": result.timestamp,
                "status": result.status.value,
                "metrics": result.metrics,
                "step_count": len(result.step_results)
            })
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(self._c(f"  Results exported to: {filename}", self.GREEN))
        print(f"  File size: {os.path.getsize(filename)} bytes")
        print()
        input("Press Enter to continue...")
    
    def network_status_menu(self):
        """Display network status"""
        self.clear_screen()
        self.print_header("🌐 NETWORK STATUS")
        print()
        
        # Load default topology if none loaded
        if not self.simulator.nodes:
            self.simulator.nodes = create_default_topology()
            self.simulator.links = create_default_links()
        
        nodes = self.simulator.nodes
        links = self.simulator.links
        
        # Zone counts
        zone_counts = {}
        for node in nodes.values():
            zone_counts[node.zone.value] = zone_counts.get(node.zone.value, 0) + 1
        
        print(self._c("  Zone Distribution:", self.BOLD))
        for zone, count in zone_counts.items():
            zone_color = self.BLUE if zone == "core" else \
                        self.PURPLE if zone == "bio" else \
                        self.YELLOW if zone == "hitl" else \
                        self.GREEN
            print(f"    {self._c(zone.upper(), zone_color)}: {count} nodes")
        print()
        
        # Node types
        type_counts = {}
        for node in nodes.values():
            type_counts[node.node_type.value] = type_counts.get(node.node_type.value, 0) + 1
        
        print(self._c("  Node Types:", self.BOLD))
        for ntype, count in type_counts.items():
            print(f"    {ntype.upper()}: {count}")
        print()
        
        # Link types
        link_types = {}
        for link in links:
            link_types[link.link_type] = link_types.get(link.link_type, 0) + 1
        
        print(self._c("  Links:", self.BOLD))
        for ltype, count in link_types.items():
            print(f"    {ltype}: {count}")
        print(f"    TOTAL: {len(links)}")
        print()
        
        # Quantum stats
        quantum_nodes = sum(1 for n in nodes.values() if n.quantum and n.quantum.coherence)
        if quantum_nodes > 0:
            avg_coherence = sum(n.quantum.coherence for n in nodes.values() 
                              if n.quantum and n.quantum.coherence) / quantum_nodes
            print(self._c("  Quantum Status:", self.BOLD))
            print(f"    Nodes with quantum state: {quantum_nodes}")
            print(f"    Average coherence: {avg_coherence:.1f}%")
        
        print()
        print(self._c("-" * 50, self.GRAY))
        input("Press Enter to continue...")
    
    def about_menu(self):
        """Display about information"""
        self.clear_screen()
        self.print_header("🧬 ABOUT BRNA")
        print()
        print(self._c("Bio-Resonance Network Architecture", self.CYAN + self.BOLD))
        print(self._c("Version 2.0 - Research Prototype", self.GRAY))
        print()
        print("  Core Concepts:")
        print("  • Neural Processing: Microtubules as 'living routers' via Orch OR")
        print("  • Biological Topology: Mycelial growth for self-healing distribution")
        print("  • Quantum Synchronization: Non-local communication via entanglement")
        print("  • Massive Persistence: DNA storage at 10^18 bytes per cubic mm")
        print()
        print(self._c("  Architecture Layers:", self.BOLD))
        print("  L1: Bio-Physical Processing (Microtubule lattices)")
        print("  L2: Sub-Network Link (Mycelial Mesh with BLAP)")
        print("  L3: Interstellar Routing (Entanglement with BRR)")
        print("  L4: Quantum-Digital Bridge (SpinToBit conversion)")
        print("  L5: Galactic Application (QSP protocol)")
        print()
        print(self._c("  Key Protocols:", self.BOLD))
        print("  • QSP: Quantum Sensory Protocol - intent-focused messaging")
        print("  • PPP: Paradox Prevention Protocol - causality guardrails")
        print("  • BLAP: Bio-Link Access Protocol - mitochondrial addressing")
        print("  • BRR: Bio-Resonance Routing - resonance cost metric")
        print()
        print(self._c("  Research Domains:", self.BOLD))
        print("  • Bio-Quantum Network Engineering")
        print("  • Orchestrated Objective Reduction (Orch OR)")
        print("  • Synthetic Biology & DNA Storage")
        print("  • Entanglement-based Quantum Networks")
        print()
        print(self._c("-" * 50, self.GRAY))
        input("Press Enter to continue...")
    
    def run(self):
        """Main UI loop"""
        while True:
            self.print_menu()
            choice = input(self._c("Enter choice (0-6): ", self.GREEN)).strip()
            
            if choice == '1':
                self.run_scenario_menu()
            elif choice == '2':
                self.custom_scenario_menu()
            elif choice == '3':
                self.view_results_menu()
            elif choice == '4':
                self.export_results_menu()
            elif choice == '5':
                self.network_status_menu()
            elif choice == '6':
                self.about_menu()
            elif choice == '0':
                self.clear_screen()
                print(self._c("\nThank you for using BRNA Test Generator!\n", self.CYAN))
                sys.exit(0)
            else:
                print(self._c("Invalid choice. Press Enter to continue...", self.RED))
                input()


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""
    ui = TerminalUI()
    
    # ASCII art banner
    banner = """
    ██████╗ ██████╗ ███╗   ██╗ █████╗ 
    ██╔══██╗██╔══██╗████╗  ██║██╔══██╗
    ██████╔╝██████╔╝██╔██╗ ██║███████║
    ██╔══██╗██╔══██╗██║╚██╗██║██╔══██║
    ██████╔╝██║  ██║██║ ╚████║██║  ██║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
    """
    
    if ui.use_color:
        print(ui._c(banner, ui.CYAN))
    else:
        print(banner)
    
    print("Bio-Resonance Network Architecture Test Generator")
    print("Loading default topology...")
    
    # Pre-load default topology
    ui.simulator.nodes = create_default_topology()
    ui.simulator.links = create_default_links()
    
    time.sleep(1)
    ui.run()


if __name__ == "__main__":
    main()