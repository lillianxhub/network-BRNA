#!/usr/bin/env python3
"""
BRNA Test Scenario Generator - Enhanced Edition
Terminal-based UI with Live Topology Visualization and Animation
Compatible with BRNA Research Portfolio v2.0
"""

import os
import sys
import json
import time
import random
import datetime
import threading
import queue
import tempfile
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
    HTTP = "HTTP"
    SSH = "SSH"
    SNMP = "SNMP"
    SYSLOG = "SYSLOG"

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
    x: float = 0  # Canvas X position
    y: float = 0  # Canvas Y position
    highlight: bool = False
    pulse: float = 0  # Animation pulse

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
    traffic: float = 0  # Traffic animation (0-1)
    highlight: bool = False

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
# ENHANCED TOPOLOGY WITH POSITIONS
# ============================================================================

def create_topology_with_positions() -> Dict[str, NetworkNode]:
    """Create the default topology with canvas positions"""
    nodes = {}
    
    # Core routers with positions
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
        python_file="microtubule.py",
        x=200, y=120
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
        python_file="microtubule.py",
        x=450, y=120
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
        python_file="microtubule.py",
        x=700, y=120
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
        python_file="microtubule.py + routing.py",
        x=450, y=220
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
            {"name": "Gi0/1", "ip": "—", "status": "Up", "connected": "NR-E"},
            {"name": "Gi0/2", "ip": "—", "status": "Up", "connected": "DNA-Store"},
            {"name": "Gi0/3", "ip": "—", "status": "Up", "connected": "NR-F"},
            {"name": "Gi0/4", "ip": "—", "status": "Up", "connected": "PC-Bio1"},
            {"name": "Gi0/5", "ip": "—", "status": "Up", "connected": "PC-Bio2"}
        ],
        metrics={"port_util": 62, "mac_table": 8, "throughput": 1000},
        protocols=[ProtocolType.MYCO_RIP, ProtocolType.BLAP],
        python_file="mycelial_mesh.py",
        x=250, y=350
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
            "storage_used": 34,
            "density": "10^18 bytes/cc"
        },
        protocols=[ProtocolType.DNA_STORE],
        python_file="dna_store.py",
        x=250, y=480
    )
    
    nodes["NR-E"] = NetworkNode(
        node_id="NR-E",
        node_type=NodeType.PC,
        zone=ZoneType.BIO,
        subnet="10.0.2.1",
        role="PC — Bio Processing Node",
        ios_version="BRNA-PC-OS 1.0",
        status="Active",
        quantum=QuantumState(
            coherence=89.0,
            spin_state="↓↓ Monitor",
            microtubule_class="B",
            frequency=38.0,
            decoherence_rate=3.2
        ),
        interfaces=[{"name": "NIC0", "ip": "10.0.2.1", "status": "Up"}],
        metrics={"latency": 3.2, "throughput": 100, "packet_loss": 0.05},
        protocols=[ProtocolType.QSP, ProtocolType.DNA_STORE],
        python_file="dna_store.py",
        x=120, y=430
    )
    
    nodes["NR-F"] = NetworkNode(
        node_id="NR-F",
        node_type=NodeType.PC,
        zone=ZoneType.BIO,
        subnet="10.0.2.3",
        role="PC — Bio Output Node",
        ios_version="BRNA-PC-OS 1.0",
        status="Active",
        quantum=QuantumState(
            coherence=87.0,
            spin_state="↑↓ Monitor",
            microtubule_class="C",
            frequency=37.0,
            decoherence_rate=3.5
        ),
        interfaces=[{"name": "NIC0", "ip": "10.0.2.3", "status": "Up"}],
        metrics={"latency": 3.5, "throughput": 100, "packet_loss": 0.06},
        protocols=[ProtocolType.QSP, ProtocolType.MYCO_RIP],
        python_file="mycelial_mesh.py",
        x=380, y=430
    )
    
    nodes["PC-Bio1"] = NetworkNode(
        node_id="PC-Bio1",
        node_type=NodeType.PC,
        zone=ZoneType.BIO,
        subnet="10.0.2.4",
        role="PC — Bio Monitor Workstation",
        ios_version="Ubuntu 22.04 LTS",
        status="Active",
        interfaces=[{"name": "eth0", "ip": "10.0.2.4", "status": "Up"}],
        metrics={"latency": 5, "throughput": 100, "packet_loss": 0.1},
        protocols=[ProtocolType.HTTP, ProtocolType.SSH, ProtocolType.SNMP],
        python_file="dashboard.py",
        x=120, y=530
    )
    
    nodes["PC-Bio2"] = NetworkNode(
        node_id="PC-Bio2",
        node_type=NodeType.PC,
        zone=ZoneType.BIO,
        subnet="10.0.2.5",
        role="PC — Reed-Solomon Test Node",
        ios_version="Ubuntu 22.04 LTS",
        status="Active",
        interfaces=[{"name": "eth0", "ip": "10.0.2.5", "status": "Up"}],
        metrics={"latency": 5, "throughput": 100, "decode_rate": 99.97},
        protocols=[ProtocolType.DNA_STORE],
        python_file="dna_store.py (test harness)",
        x=380, y=530
    )
    
    # HITL zone
    nodes["SW-HITL"] = NetworkNode(
        node_id="SW-HITL",
        node_type=NodeType.SWITCH,
        zone=ZoneType.HITL,
        subnet="10.0.3.0/24",
        role="Switch — HITL Governance Fabric",
        ios_version="Cisco IOS 2960",
        status="Active",
        interfaces=[
            {"name": "Gi0/1", "ip": "—", "status": "Up", "connected": "HITL-GW"},
            {"name": "Gi0/2", "ip": "—", "status": "Up", "connected": "Monitor-1"},
            {"name": "Gi0/3", "ip": "—", "status": "Up", "connected": "Monitor-2"},
            {"name": "Gi0/4", "ip": "—", "status": "Up", "connected": "PC-HITL1"},
            {"name": "Gi0/5", "ip": "—", "status": "Up", "connected": "PC-HITL2"}
        ],
        metrics={"port_util": 40, "mac_table": 6, "throughput": 1000},
        protocols=[ProtocolType.HITL_CTRL, ProtocolType.PPP],
        python_file="dashboard.py",
        x=650, y=350
    )
    
    nodes["HITL-GW"] = NetworkNode(
        node_id="HITL-GW",
        node_type=NodeType.PC,
        zone=ZoneType.HITL,
        subnet="10.0.3.1",
        role="PC — Human Override Gateway",
        ios_version="HITL-OS 2.0",
        status="Standby",
        interfaces=[
            {"name": "eth0", "ip": "10.0.3.1", "status": "Up"},
            {"name": "mgmt", "ip": "10.0.0.1", "status": "Up"}
        ],
        metrics={"override_events": 3, "ethics_flags": 1, "approval_timeout": 30},
        protocols=[ProtocolType.HITL_CTRL, ProtocolType.PPP],
        python_file="dashboard.py",
        x=520, y=430
    )
    
    nodes["Monitor-1"] = NetworkNode(
        node_id="Monitor-1",
        node_type=NodeType.PC,
        zone=ZoneType.HITL,
        subnet="10.0.3.2",
        role="PC — Fidelity Monitor",
        ios_version="Ubuntu 22.04 LTS",
        status="Active",
        interfaces=[{"name": "eth0", "ip": "10.0.3.2", "status": "Up"}],
        metrics={"sampling_rate": 1000, "alerts_sent": 12},
        protocols=[ProtocolType.SNMP, ProtocolType.HTTP, ProtocolType.SSH],
        python_file="dashboard.py (fidelity)",
        x=600, y=430
    )
    
    nodes["Monitor-2"] = NetworkNode(
        node_id="Monitor-2",
        node_type=NodeType.PC,
        zone=ZoneType.HITL,
        subnet="10.0.3.3",
        role="PC — Ethics Audit Node",
        ios_version="Ubuntu 22.04 LTS",
        status="Active",
        interfaces=[{"name": "eth0", "ip": "10.0.3.3", "status": "Up"}],
        metrics={"rules_loaded": 47, "violations": 0},
        protocols=[ProtocolType.SNMP, ProtocolType.HTTP, ProtocolType.SYSLOG],
        python_file="dashboard.py (ethics)",
        x=680, y=430
    )
    
    nodes["PC-HITL1"] = NetworkNode(
        node_id="PC-HITL1",
        node_type=NodeType.PC,
        zone=ZoneType.HITL,
        subnet="10.0.3.4",
        role="PC — Human Operator Terminal 1",
        ios_version="Ubuntu 22.04 LTS",
        status="Active",
        interfaces=[{"name": "eth0", "ip": "10.0.3.4", "status": "Up"}],
        metrics={"actions_today": 14, "pending": 0},
        protocols=[ProtocolType.HTTP, ProtocolType.SSH],
        python_file="dashboard.py (operator UI)",
        x=570, y=530
    )
    
    nodes["PC-HITL2"] = NetworkNode(
        node_id="PC-HITL2",
        node_type=NodeType.PC,
        zone=ZoneType.HITL,
        subnet="10.0.3.5",
        role="PC — Human Operator Terminal 2",
        ios_version="Ubuntu 22.04 LTS",
        status="Idle",
        interfaces=[{"name": "eth0", "ip": "10.0.3.5", "status": "Up"}],
        metrics={"failover_ready": "Yes"},
        protocols=[ProtocolType.HTTP, ProtocolType.SSH],
        python_file="dashboard.py (operator UI)",
        x=730, y=530
    )
    
    # Entanglement zone
    nodes["QNode-A"] = NetworkNode(
        node_id="QNode-A",
        node_type=NodeType.QNODE,
        zone=ZoneType.ENTANGLE,
        subnet="10.0.4.1",
        role="QNode — Entangled Pair 1A",
        ios_version="QSP-OS 0.9",
        status="Active",
        quantum=QuantumState(
            coherence=99.0,
            spin_state="↑↓ Entangled",
            microtubule_class="Q",
            frequency=40.0,
            decoherence_rate=1.0,
            bell_state="|Φ+⟩",
            entanglement_partner="QNode-B"
        ),
        interfaces=[{"name": "qif0", "ip": "10.0.4.1", "status": "Entangled"}],
        metrics={"fidelity": 99.1, "chsh": 2.82},
        protocols=[ProtocolType.QSP],
        python_file="qsp_protocol.py",
        x=200, y=620
    )
    
    nodes["QNode-B"] = NetworkNode(
        node_id="QNode-B",
        node_type=NodeType.QNODE,
        zone=ZoneType.ENTANGLE,
        subnet="10.0.4.2",
        role="QNode — Entangled Pair 1B + Swap",
        ios_version="QSP-OS 0.9",
        status="Active",
        quantum=QuantumState(
            coherence=99.0,
            spin_state="↑↓ Entangled",
            microtubule_class="Q",
            frequency=40.0,
            decoherence_rate=1.0,
            bell_state="|Φ+⟩",
            entanglement_partner="QNode-A"
        ),
        interfaces=[
            {"name": "qif0", "ip": "10.0.4.2", "status": "Entangled"},
            {"name": "qif1", "ip": "10.0.4.2", "status": "Swapping"}
        ],
        metrics={"fidelity": 99.0, "swap_success": 94},
        protocols=[ProtocolType.QSP],
        python_file="qsp_protocol.py",
        x=350, y=620
    )
    
    nodes["QNode-C"] = NetworkNode(
        node_id="QNode-C",
        node_type=NodeType.QNODE,
        zone=ZoneType.ENTANGLE,
        subnet="10.0.4.3",
        role="QNode — Entangled Pair 2A",
        ios_version="QSP-OS 0.9",
        status="Active",
        quantum=QuantumState(
            coherence=98.0,
            spin_state="↑↓ Entangled",
            microtubule_class="Q",
            frequency=40.0,
            decoherence_rate=1.2,
            bell_state="|Ψ-⟩",
            entanglement_partner="QNode-D"
        ),
        interfaces=[{"name": "qif0", "ip": "10.0.4.3", "status": "Entangled"}],
        metrics={"fidelity": 98.3, "chsh": 2.79},
        protocols=[ProtocolType.QSP],
        python_file="qsp_protocol.py",
        x=550, y=620
    )
    
    nodes["QNode-D"] = NetworkNode(
        node_id="QNode-D",
        node_type=NodeType.QNODE,
        zone=ZoneType.ENTANGLE,
        subnet="10.0.4.4",
        role="QNode — Entangled Pair 2B",
        ios_version="QSP-OS 0.9",
        status="Active",
        quantum=QuantumState(
            coherence=98.0,
            spin_state="↑↓ Entangled",
            microtubule_class="Q",
            frequency=40.0,
            decoherence_rate=1.2,
            bell_state="|Ψ-⟩",
            entanglement_partner="QNode-C"
        ),
        interfaces=[{"name": "qif0", "ip": "10.0.4.4", "status": "Entangled"}],
        metrics={"fidelity": 98.1, "chsh": 2.78},
        protocols=[ProtocolType.QSP],
        python_file="qsp_protocol.py",
        x=700, y=620
    )
    
    return nodes


def create_enhanced_links() -> List[NetworkLink]:
    """Create enhanced links with animation support"""
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
# HTML VISUALIZATION GENERATOR - COMPLETELY FIXED VERSION
# ============================================================================

class HTMLVisualizer:
    """Generates HTML canvas visualization with animations"""
    
    def __init__(self, nodes: Dict[str, NetworkNode], links: List[NetworkLink]):
        self.nodes = nodes
        self.links = links
        self.temp_file = None
        self.running = False
        self.update_queue = queue.Queue()
        self.animation_thread = None
        
    def generate_html(self, title: str = "BRNA Network Topology") -> str:
        """Generate HTML with canvas visualization"""
        
        # Zone colors
        zone_colors = {
            "core": {"border": "#1a6faf", "fill": "rgba(26,111,175,0.1)", "text": "#1a6faf"},
            "bio": {"border": "#6b3fa0", "fill": "rgba(107,63,160,0.1)", "text": "#6b3fa0"},
            "hitl": {"border": "#7a5c00", "fill": "rgba(122,92,0,0.1)", "text": "#7a5c00"},
            "entangle": {"border": "#2d7a4f", "fill": "rgba(45,122,79,0.1)", "text": "#2d7a4f"}
        }
        
        # Convert nodes to JavaScript array - with safe coherence access
        nodes_js = []
        for node_id, node in self.nodes.items():
            coherence = 0
            if node.quantum and hasattr(node.quantum, 'coherence'):
                coherence = node.quantum.coherence
            
            nodes_js.append(f"""{{ 
                id: '{node_id}', 
                x: {node.x}, 
                y: {node.y}, 
                zone: '{node.zone.value}', 
                type: '{node.node_type.value}',
                coherence: {coherence},
                status: '{node.status}'
            }}""")
        
        # Convert links to JavaScript array
        links_js = []
        for link in self.links:
            links_js.append(f"""{{ 
                from: '{link.from_node}', 
                to: '{link.to_node}', 
                type: '{link.link_type}', 
                label: '{link.label}' 
            }}""")
        
        nodes_js_str = ",\n            ".join(nodes_js)
        links_js_str = ",\n            ".join(links_js)
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a1929 0%, #1a2a3a 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #0a1929 0%, #1e3a5f 100%);
            color: white;
            padding: 20px;
            text-align: center;
            border-bottom: 4px solid #4d9fff;
        }}
        
        .header h1 {{
            font-size: 2.2em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #4d9fff 0%, #b388ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .canvas-wrapper {{
            background: #0a0f1a;
            padding: 20px;
            position: relative;
            min-height: 700px;
        }}
        
        #topologyCanvas {{
            width: 100%;
            height: auto;
            background: #0a0f1a;
            border-radius: 12px;
            display: block;
            border: 1px solid #333;
        }}
        
        .stats-panel {{
            display: flex;
            gap: 20px;
            padding: 15px 20px;
            background: #f0f4f8;
            border-top: 2px solid #d0d8e0;
            flex-wrap: wrap;
        }}
        
        .stat-card {{
            background: white;
            padding: 10px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            min-width: 150px;
        }}
        
        .stat-label {{
            font-size: 0.8em;
            color: #4a5568;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .stat-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #1a6faf;
        }}
        
        .stat-unit {{
            font-size: 0.8em;
            color: #8a94a0;
            margin-left: 5px;
        }}
        
        .legend {{
            display: flex;
            gap: 20px;
            padding: 10px 20px;
            background: #f8fafc;
            border-top: 1px solid #d0d8e0;
            flex-wrap: wrap;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .color-dot {{
            width: 16px;
            height: 16px;
            border-radius: 4px;
        }}
        
        .status-badge {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }}
        
        .status-active {{ background: #2d7a4f; }}
        .status-standby {{ background: #f59e0b; }}
        .status-idle {{ background: #8a94a0; }}
        
        .controls {{
            padding: 15px 20px;
            background: #e4e8f0;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .btn-primary {{ background: #1a6faf; color: white; }}
        .btn-primary:hover {{ background: #155a9a; transform: translateY(-2px); }}
        
        .log-panel {{
            background: #1e1e2e;
            color: #e4e6e9;
            padding: 15px 20px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            max-height: 150px;
            overflow-y: auto;
            border-top: 2px solid #4d9fff;
        }}
        
        .log-entry {{
            margin-bottom: 5px;
            border-bottom: 1px solid #333;
            padding-bottom: 3px;
        }}
        
        .log-time {{
            color: #8a94a0;
            margin-right: 10px;
        }}
        
        .log-ok {{ color: #2d7a4f; }}
        .log-warn {{ color: #f59e0b; }}
        .log-err {{ color: #c0392b; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧬 BRNA Network Topology</h1>
            <div class="stats-panel" id="liveStats">
                <div class="stat-card">
                    <div class="stat-label">Active Nodes</div>
                    <div class="stat-value" id="statNodes">16</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Avg Coherence</div>
                    <div class="stat-value" id="statCoherence">93.2<span class="stat-unit">%</span></div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Quantum Links</div>
                    <div class="stat-value" id="statQuantum">3</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Current Step</div>
                    <div class="stat-value" id="statStep">—</div>
                </div>
            </div>
        </div>
        
        <div class="canvas-wrapper">
            <canvas id="topologyCanvas" width="1000" height="700"></canvas>
        </div>
        
        <div class="legend">
            <div class="legend-item"><span class="color-dot" style="background: #1a6faf;"></span> Core Zone</div>
            <div class="legend-item"><span class="color-dot" style="background: #6b3fa0;"></span> Bio Zone</div>
            <div class="legend-item"><span class="color-dot" style="background: #7a5c00;"></span> HITL Zone</div>
            <div class="legend-item"><span class="color-dot" style="background: #2d7a4f;"></span> Entanglement Zone</div>
            <div class="legend-item"><span class="color-dot" style="background: #b0bcc8;"></span> Ethernet</div>
            <div class="legend-item"><span class="color-dot" style="background: #8a94a0; border-top: 2px dotted #8a94a0;"></span> Serial (Mycelial)</div>
            <div class="legend-item"><span class="color-dot" style="background: #2d7a4f; border-top: 2px dashed #2d7a4f;"></span> Quantum</div>
            <div class="legend-item"><span class="color-dot" style="background: #8a9a8a; border-top: 2px dotted #8a9a8a;"></span> Swap</div>
        </div>
        
        <div class="controls">
            <button class="btn btn-primary" onclick="startAnimation()">▶ Start Animation</button>
            <button class="btn btn-primary" onclick="stopAnimation()">⏸ Stop</button>
            <button class="btn btn-primary" onclick="highlightCore()">🌟 Highlight Core</button>
            <button class="btn btn-primary" onclick="highlightBio()">🧬 Highlight Bio</button>
            <button class="btn btn-primary" onclick="highlightHITL()">👤 Highlight HITL</button>
            <button class="btn btn-primary" onclick="highlightQuantum()">⚛️ Highlight Quantum</button>
            <button class="btn btn-primary" onclick="demonstratePaths()">🗺️ Show Network Paths</button>
            <span style="margin-left: auto; color: #4a5568;">Packets follow actual network topology</span>
        </div>
        
        <div class="log-panel" id="logPanel">
            <div class="log-entry"><span class="log-time">00:00:00</span> <span class="log-ok">✓ BRNA Network initialized</span></div>
            <div class="log-entry"><span class="log-time">00:00:01</span> All 16 nodes active</div>
            <div class="log-entry"><span class="log-time">00:00:02</span> Path-based routing enabled</div>
        </div>
    </div>

    <script>
        // Node positions and data
        const nodes = [
            {nodes_js_str}
        ];
        
        const links = [
            {links_js_str}
        ];
        
        console.log("Nodes loaded:", nodes.length);
        console.log("Links loaded:", links.length);
        
        // Zone colors
        const zoneColors = {{
            core: {{ border: '#1a6faf', fill: 'rgba(26,111,175,0.1)' }},
            bio: {{ border: '#6b3fa0', fill: 'rgba(107,63,160,0.1)' }},
            hitl: {{ border: '#7a5c00', fill: 'rgba(122,92,0,0.1)' }},
            entangle: {{ border: '#2d7a4f', fill: 'rgba(45,122,79,0.1)' }}
        }};
        
        const canvas = document.getElementById('topologyCanvas');
        const ctx = canvas.getContext('2d');
        
        // Animation variables
        let animationId = null;
        let packets = [];
        let pulses = {{}};
        let packetCounter = 0;
        
        // Initialize pulses
        nodes.forEach(node => {{
            pulses[node.id] = 0;
        }});
        
        // ============ PATH FINDING ============
        function buildAdjacencyList() {{
            const adj = {{}};
            links.forEach(link => {{
                if (!adj[link.from]) adj[link.from] = [];
                if (!adj[link.to]) adj[link.to] = [];
                adj[link.from].push(link.to);
                adj[link.to].push(link.from);
            }});
            return adj;
        }}
        
        function findPath(sourceId, destId) {{
            if (sourceId === destId) return [sourceId];
            
            const adj = buildAdjacencyList();
            
            // BFS to find shortest path
            const queue = [{{ node: sourceId, path: [sourceId] }}];
            const visited = new Set([sourceId]);
            
            while (queue.length > 0) {{
                const {{ node, path }} = queue.shift();
                
                if (node === destId) {{
                    return path;
                }}
                
                if (adj[node]) {{
                    for (const neighbor of adj[node]) {{
                        if (!visited.has(neighbor)) {{
                            visited.add(neighbor);
                            queue.push({{
                                node: neighbor,
                                path: [...path, neighbor]
                            }});
                        }}
                    }}
                }}
            }}
            return null; // No path found
        }}
        
        // ============ PATH-BASED PACKET ROUTING ============
        function sendPacket(sourceId, destId, color = '#1a6faf') {{
            const path = findPath(sourceId, destId);
            
            if (!path || path.length < 2) {{
                addLog(`❌ No network path from ${{sourceId}} to ${{destId}}`, 'err');
                return;
            }}
            
            const pathStr = path.join(' → ');
            addLog(`🛤️  Route: ${{pathStr}}`, 'ok');
            
            const packetId = ++packetCounter;
            
            // Send packet along each hop with delay
            for (let i = 0; i < path.length - 1; i++) {{
                const fromNode = path[i];
                const toNode = path[i + 1];
                const delay = i * 800; // 800ms per hop
                
                setTimeout(() => {{
                    // Create packet for this hop
                    packets.push({{
                        id: packetId,
                        from: fromNode,
                        to: toNode,
                        progress: 0,
                        color: color,
                        hop: i,
                        totalHops: path.length - 1
                    }});
                    
                    // Pulse the sending node
                    if (pulses[fromNode] !== undefined) {{
                        pulses[fromNode] = 0.8;
                    }}
                    
                    // Log the hop
                    if (i === 0) {{
                        addLog(`📤 ${{sourceId}} → ${{toNode}}`, 'ok');
                    }} else if (i === path.length - 2) {{
                        addLog(`📥 Packet arrived at ${{destId}} via ${{fromNode}}`, 'ok');
                    }} else {{
                        addLog(`🔄 ${{fromNode}} → ${{toNode}}`, 'ok');
                    }}
                }}, delay);
            }}
        }}
        
        // ============ DEMONSTRATION ROUTES ============
        function demonstratePaths() {{
            addLog('=== DEMONSTRATING NETWORK PATHS ===', 'ok');
            
            // Clear any existing packets
            packets = [];
            
            // Route 1: Core to Bio via NR-D hub
            setTimeout(() => {{
                addLog('\\n🌐 Route 1: NR-A → NR-D → SW-BIO → DNA-Store', 'ok');
                sendPacket('NR-A', 'DNA-Store', '#1a6faf');
            }}, 1000);
            
            // Route 2: Core to HITL via NR-D hub
            setTimeout(() => {{
                addLog('\\n🌐 Route 2: NR-C → NR-D → SW-HITL → HITL-GW', 'ok');
                sendPacket('NR-C', 'HITL-GW', '#7a5c00');
            }}, 6000);
            
            // Route 3: Quantum entanglement chain
            setTimeout(() => {{
                addLog('\\n🌐 Route 3: QNode-A → QNode-B → QNode-C → QNode-D', 'ok');
                sendPacket('QNode-A', 'QNode-D', '#2d7a4f');
            }}, 11000);
            
            // Route 4: Bio to HITL cross-zone
            setTimeout(() => {{
                addLog('\\n🌐 Route 4: DNA-Store → SW-BIO → NR-D → SW-HITL → Monitor-1', 'ok');
                sendPacket('DNA-Store', 'Monitor-1', '#6b3fa0');
            }}, 16000);
            
            // Route 5: Mycelial mesh internal
            setTimeout(() => {{
                addLog('\\n🌐 Route 5: NR-E → SW-BIO → NR-F (Bio zone internal)', 'ok');
                sendPacket('NR-E', 'NR-F', '#6b3fa0');
            }}, 21000);
            
            // Route 6: HITL governance
            setTimeout(() => {{
                addLog('\\n🌐 Route 6: HITL-GW → SW-HITL → Monitor-1 → Monitor-2', 'ok');
                sendPacket('HITL-GW', 'Monitor-2', '#7a5c00');
            }}, 26000);
        }}
        
        // ============ VALID ROUTE GENERATOR ============
        function getRandomValidRoute() {{
            const validRoutes = [
                // Core to Bio
                {{from: 'NR-A', to: 'DNA-Store', color: '#1a6faf'}},
                {{from: 'NR-B', to: 'NR-E', color: '#1a6faf'}},
                {{from: 'NR-C', to: 'PC-Bio1', color: '#1a6faf'}},
                {{from: 'NR-D', to: 'NR-F', color: '#1a6faf'}},
                
                // Core to HITL
                {{from: 'NR-A', to: 'HITL-GW', color: '#7a5c00'}},
                {{from: 'NR-B', to: 'Monitor-1', color: '#7a5c00'}},
                {{from: 'NR-C', to: 'PC-HITL1', color: '#7a5c00'}},
                
                // Bio internal
                {{from: 'NR-E', to: 'DNA-Store', color: '#6b3fa0'}},
                {{from: 'DNA-Store', to: 'PC-Bio2', color: '#6b3fa0'}},
                {{from: 'SW-BIO', to: 'NR-F', color: '#6b3fa0'}},
                
                // HITL internal
                {{from: 'HITL-GW', to: 'Monitor-2', color: '#7a5c00'}},
                {{from: 'SW-HITL', to: 'PC-HITL2', color: '#7a5c00'}},
                
                // Quantum zone
                {{from: 'QNode-A', to: 'QNode-C', color: '#2d7a4f'}},
                {{from: 'QNode-B', to: 'QNode-D', color: '#2d7a4f'}},
            ];
            
            return validRoutes[Math.floor(Math.random() * validRoutes.length)];
        }}
        
        // ============ DRAWING FUNCTIONS ============
        function drawZone(x1, y1, x2, y2, zone) {{
            ctx.save();
            ctx.fillStyle = zoneColors[zone].fill;
            ctx.strokeStyle = zoneColors[zone].border;
            ctx.lineWidth = 2;
            ctx.setLineDash([5, 5]);
            
            ctx.beginPath();
            ctx.rect(x1, y1, x2 - x1, y2 - y1);
            ctx.fill();
            ctx.stroke();
            
            ctx.setLineDash([]);
            ctx.font = 'bold 14px "Segoe UI", sans-serif';
            ctx.fillStyle = zoneColors[zone].border;
            ctx.fillText(zone.toUpperCase(), x1 + 10, y1 + 25);
            
            ctx.restore();
        }}
        
        function drawZones() {{
            drawZone(100, 50, 850, 270, 'core');
            drawZone(50, 300, 450, 590, 'bio');
            drawZone(500, 300, 900, 590, 'hitl');
            drawZone(100, 600, 850, 670, 'entangle');
        }}
        
        function drawLinks() {{
            links.forEach(link => {{
                const fromNode = nodes.find(n => n.id === link.from);
                const toNode = nodes.find(n => n.id === link.to);
                if (!fromNode || !toNode) return;
                
                ctx.save();
                
                switch(link.type) {{
                    case 'quantum':
                        ctx.strokeStyle = '#2d7a4f';
                        ctx.lineWidth = 2;
                        ctx.setLineDash([8, 6]);
                        break;
                    case 'swap':
                        ctx.strokeStyle = '#8a9a8a';
                        ctx.lineWidth = 1.5;
                        ctx.setLineDash([4, 6]);
                        break;
                    case 'serial':
                        ctx.strokeStyle = '#8a94a0';
                        ctx.lineWidth = 2;
                        ctx.setLineDash([6, 4]);
                        break;
                    default:
                        ctx.strokeStyle = '#b0bcc8';
                        ctx.lineWidth = 2;
                        ctx.setLineDash([]);
                }}
                
                ctx.beginPath();
                ctx.moveTo(fromNode.x, fromNode.y);
                ctx.lineTo(toNode.x, toNode.y);
                ctx.stroke();
                
                ctx.restore();
            }});
        }}
        
        function drawNodes() {{
            nodes.forEach(node => {{
                ctx.save();
                
                ctx.shadowColor = 'rgba(0,0,0,0.3)';
                ctx.shadowBlur = 10;
                ctx.shadowOffsetY = 3;
                
                if (pulses[node.id] > 0) {{
                    ctx.shadowColor = zoneColors[node.zone].border;
                    ctx.shadowBlur = 20 + 10 * Math.sin(Date.now() / 200);
                }}
                
                ctx.fillStyle = 'white';
                ctx.strokeStyle = zoneColors[node.zone].border;
                ctx.lineWidth = 3;
                
                switch(node.type) {{
                    case 'router':
                        ctx.beginPath();
                        ctx.moveTo(node.x, node.y - 20);
                        ctx.lineTo(node.x + 20, node.y);
                        ctx.lineTo(node.x, node.y + 20);
                        ctx.lineTo(node.x - 20, node.y);
                        ctx.closePath();
                        break;
                        
                    case 'switch':
                        ctx.beginPath();
                        roundedRect(ctx, node.x - 20, node.y - 12, 40, 24, 5);
                        break;
                        
                    case 'qnode':
                        ctx.beginPath();
                        ctx.arc(node.x, node.y, 18, 0, Math.PI * 2);
                        break;
                        
                    default:
                        ctx.beginPath();
                        roundedRect(ctx, node.x - 18, node.y - 12, 36, 24, 4);
                }}
                
                ctx.fill();
                ctx.stroke();
                
                if (node.type === 'qnode') {{
                    ctx.shadowBlur = 5;
                    ctx.strokeStyle = '#2d7a4f';
                    ctx.lineWidth = 1.5;
                    ctx.beginPath();
                    ctx.arc(node.x, node.y, 8, 0, Math.PI * 2);
                    ctx.stroke();
                    
                    ctx.font = 'bold 10px "Segoe UI", sans-serif';
                    ctx.fillStyle = '#2d7a4f';
                    ctx.fillText('⚛️', node.x - 15, node.y - 30);
                }}
                
                ctx.shadowBlur = 0;
                ctx.font = 'bold 12px "Segoe UI", sans-serif';
                ctx.fillStyle = '#ffffff';
                ctx.textAlign = 'center';
                ctx.fillText(node.id, node.x, node.y - 25);
                
                if (node.coherence > 0) {{
                    ctx.font = '10px "Segoe UI", sans-serif';
                    ctx.fillStyle = node.coherence > 90 ? '#2d7a4f' : node.coherence > 85 ? '#f59e0b' : '#c0392b';
                    ctx.fillText(node.coherence + '%', node.x, node.y + 25);
                }}
                
                ctx.beginPath();
                ctx.arc(node.x + 15, node.y - 15, 4, 0, Math.PI * 2);
                ctx.fillStyle = node.status === 'Active' ? '#2d7a4f' : 
                               node.status === 'Standby' ? '#f59e0b' : '#8a94a0';
                ctx.fill();
                ctx.strokeStyle = 'white';
                ctx.lineWidth = 1.5;
                ctx.stroke();
                
                ctx.restore();
            }});
        }}
        
        function drawPackets() {{
            packets.forEach((packet, index) => {{
                packet.progress += 0.015;
                if (packet.progress > 1) {{
                    packets.splice(index, 1);
                    return;
                }}
                
                const fromNode = nodes.find(n => n.id === packet.from);
                const toNode = nodes.find(n => n.id === packet.to);
                if (!fromNode || !toNode) return;
                
                const x = fromNode.x + (toNode.x - fromNode.x) * packet.progress;
                const y = fromNode.y + (toNode.y - fromNode.y) * packet.progress;
                
                ctx.save();
                ctx.shadowColor = packet.color;
                ctx.shadowBlur = 15;
                ctx.beginPath();
                ctx.arc(x, y, 6, 0, Math.PI * 2);
                ctx.fillStyle = packet.color;
                ctx.fill();
                
                ctx.shadowBlur = 5;
                ctx.beginPath();
                ctx.arc(x, y, 3, 0, Math.PI * 2);
                ctx.fillStyle = 'white';
                ctx.fill();
                
                ctx.restore();
            }});
        }}
        
        function roundedRect(ctx, x, y, w, h, r) {{
            ctx.beginPath();
            ctx.moveTo(x + r, y);
            ctx.lineTo(x + w - r, y);
            ctx.quadraticCurveTo(x + w, y, x + w, y + r);
            ctx.lineTo(x + w, y + h - r);
            ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
            ctx.lineTo(x + r, y + h);
            ctx.quadraticCurveTo(x, y + h, x, y + h - r);
            ctx.lineTo(x, y + r);
            ctx.quadraticCurveTo(x, y, x + r, y);
            ctx.closePath();
        }}
        
        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawZones();
            drawLinks();
            drawPackets();
            drawNodes();
            
            animationId = requestAnimationFrame(draw);
        }}
        
        // Animation control
        function startAnimation() {{
            if (!animationId) {{
                draw();
            }}
        }}
        
        function stopAnimation() {{
            if (animationId) {{
                cancelAnimationFrame(animationId);
                animationId = null;
            }}
        }}
        
        function addLog(message, type = '') {{
            const logPanel = document.getElementById('logPanel');
            const time = new Date().toLocaleTimeString();
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = `<span class="log-time">${{time}}</span> <span class="log-${{type}}">${{message}}</span>`;
            logPanel.appendChild(entry);
            logPanel.scrollTop = logPanel.scrollHeight;
            
            while (logPanel.children.length > 15) {{
                logPanel.removeChild(logPanel.firstChild);
            }}
        }}
        
        // Highlight functions
        function highlightCore() {{
            addLog('🌟 Highlighting Core Zone', 'ok');
        }}
        
        function highlightBio() {{
            addLog('🧬 Highlighting Bio Zone', 'ok');
        }}
        
        function highlightHITL() {{
            addLog('👤 Highlighting HITL Zone', 'warn');
        }}
        
        function highlightQuantum() {{
            addLog('⚛️ Highlighting Quantum Zone', 'ok');
        }}
        
        // Update stats
        function updateStats(nodesActive, coherence, quantumLinks, currentStep) {{
            document.getElementById('statNodes').textContent = nodesActive;
            document.getElementById('statCoherence').textContent = coherence;
            document.getElementById('statQuantum').textContent = quantumLinks;
            document.getElementById('statStep').textContent = currentStep;
        }}
        
        // Pulse update
        setInterval(() => {{
            for (let id in pulses) {{
                if (pulses[id] > 0) {{
                    pulses[id] -= 0.02;
                }}
            }}
        }}, 50);
        
        // Start animation
        setTimeout(() => {{
            startAnimation();
            console.log("Animation started");
            addLog('✅ Path-based routing active', 'ok');
        }}, 100);
        
        // Periodic valid route generator (every 15 seconds)
        setInterval(() => {{
            if (packets.length < 5) {{  // Don't overload
                const route = getRandomValidRoute();
                if (route) {{
                    sendPacket(route.from, route.to, route.color);
                }}
            }}
        }}, 15000);
        
        // Initial demonstration after 2 seconds
        setTimeout(() => {{
            demonstratePaths();
        }}, 2000);
    </script>
</body>
</html>'''
        return html
    
    def launch(self, title: str = "BRNA Network Topology") -> str:
        """Save HTML visualization to a local file"""
        html_content = self.generate_html(title)
        
        filename = "brna_visualization.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.temp_file = os.path.abspath(filename)
        
        # Try to open in browser, but don't fail if it doesn't work
        try:
            import webbrowser
            webbrowser.open('file://' + self.temp_file)
        except:
            pass
            
        return self.temp_file
    
    def cleanup(self):
        """Cleanup logic (disabled for local persistence)"""
        pass


# ============================================================================
# ENHANCED SIMULATOR WITH VISUALIZATION
# ============================================================================

class EnhancedBRNASimulator:
    """Enhanced simulator with live visualization support"""
    
    def __init__(self):
        self.nodes = {}
        self.links = []
        self.test_results = []
        self.log = []
        self.rng = random.Random(42)
        self.visualizer = None
        self.current_step = 0
        
    def load_scenario(self, scenario: TestScenario):
        """Load a test scenario"""
        self.nodes = scenario.nodes
        self.links = scenario.links
        self.log.append(f"Loaded scenario: {scenario.name}")
        self.log.append(f"  Nodes: {len(self.nodes)}")
        self.log.append(f"  Links: {len(self.links)}")
        
        self.visualizer = HTMLVisualizer(self.nodes, self.links)
        self.visualizer.launch(f"BRNA Simulation - {scenario.name}")
    
    def run_scenario(self, scenario: TestScenario) -> TestResult:
        """Run a test scenario with live visualization"""
        self.load_scenario(scenario)
        
        step_results = []
        start_time = time.time()
        
        self.log.append("=" * 60)
        self.log.append(f"RUNNING SCENARIO: {scenario.name}")
        self.log.append("=" * 60)
        
        print("\n" + "="*60)
        print(f"▶️ RUNNING: {scenario.name}")
        print("="*60)
        print("📺 Visualization launched in browser")
        print("⏳ Running simulation steps...\n")
        
        for step in scenario.test_steps:
            self.current_step = step['step']
            print(f"  Step {step['step']}: {step['name']}... ", end='', flush=True)
            
            self.log.append(f"\nStep {step['step']}: {step['name']}")
            result = self._execute_step(step)
            step_results.append(result)
            
            if result['status'] == "PASSED":
                print(f"✅ {result['status']}")
            elif result['status'] == "WARNING":
                print(f"⚠️ {result['status']}")
            else:
                print(f"❌ {result['status']}")
            
            time.sleep(1)
            
            if result["status"] == "FAILED" and step.get("critical", False):
                self.log.append("Critical step failed - aborting scenario")
                print("  ⛔ Critical failure - aborting")
                break
        
        end_time = time.time()
        
        metrics = self._collect_metrics()
        metrics["duration_seconds"] = round(end_time - start_time, 2)
        
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
        
        print("\n" + "="*60)
        print(f"📊 TEST COMPLETE: {status.value}")
        print("="*60)
        print(f"Duration: {metrics['duration_seconds']} seconds")
        print(f"Avg Coherence: {metrics.get('avg_coherence', 'N/A')}%")
        print(f"Active Nodes: {metrics.get('active_nodes', 0)}/{metrics.get('total_nodes', 0)}")
        print("\nPress Enter to continue...")
        
        return result
    
    def _execute_step(self, step: Dict) -> Dict:
        """Execute a single test step with visual feedback"""
        self.log.append(f"  Command: {step['command']}")
        self.log.append(f"  Target: {step['target']}")
        
        time.sleep(0.5)
        
        success_prob = 0.95
        
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
# ENHANCED TERMINAL UI
# ============================================================================

class EnhancedTerminalUI:
    """Enhanced terminal UI with visualization support"""
    
    def __init__(self):
        self.simulator = EnhancedBRNASimulator()
        self.current_scenario = None
        self.last_result = None
        self.visualizer = None
        
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
        self.print_header("🧬 BRNA TEST GENERATOR v3.0 - LIVE VISUALIZATION")
        print()
        print(self._c("Bio-Resonance Network Architecture", self.CYAN))
        print(self._c("Enhanced Edition with Live Topology Animation", self.GRAY))
        print()
        print(self._c("📋 MAIN MENU", self.BOLD))
        print()
        print(f"  {self._c('1', self.GREEN)}. Run Pre-defined Test Scenario (with Live Viz)")
        print(f"  {self._c('2', self.GREEN)}. Launch Topology Visualizer Only")
        print(f"  {self._c('3', self.GREEN)}. Create Custom Scenario")
        print(f"  {self._c('4', self.GREEN)}. View Results")
        print(f"  {self._c('5', self.GREEN)}. Export Results")
        print(f"  {self._c('6', self.GREEN)}. Network Status")
        print(f"  {self._c('7', self.GREEN)}. About BRNA")
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
                print(self._c("\n📺 Launching visualization in browser...", self.CYAN))
                time.sleep(1)
                result = self.simulator.run_scenario(scenario)
                self.last_result = result
                input(self._c("\nPress Enter to continue...", self.GRAY))
            else:
                print(self._c("Invalid choice. Press Enter to continue...", self.RED))
                input()
    
    def launch_visualizer_only(self):
        """Launch just the topology visualizer"""
        self.clear_screen()
        self.print_header("📺 LIVE TOPOLOGY VISUALIZER")
        print()
        print(self._c("Launching BRNA network topology in browser...", self.CYAN))
        print()
        
        nodes = create_topology_with_positions()
        links = create_enhanced_links()
        visualizer = HTMLVisualizer(nodes, links)
        filename = visualizer.launch("BRNA Network Topology - Live View")
        
        print(self._c(f"✓ Visualization saved!", self.GREEN))
        print(self._c(f"📁 Local file: {filename}", self.GRAY))
        print()
        print(self._c("If it didn't open automatically, please open this file manually:", self.CYAN))
        print(self._c(f"  {filename}", self.WHITE + self.BOLD))
        print()
        input(self._c("Press Enter to continue...", self.GRAY))
    
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
        
        # Create custom scenario
        custom_scenario = TestScenario(
            name=name,
            description=desc,
            author="Custom User",
            created=datetime.datetime.now().isoformat(),
            tags=["custom"]
        )
        
        # Add selected steps
        custom_scenario.test_steps = [
            {"step": i+1, "name": f"Custom step {i+1}", "command": "custom_command()", 
             "target": "all", "expected": "success"}
            for i in range(min(5, len(steps_choice.split(',')) if steps_choice else 1))
        ]
        
        custom_scenario.nodes = create_topology_with_positions()
        custom_scenario.links = create_enhanced_links()
        
        print()
        print(self._c(f"Custom scenario '{name}' created with {len(custom_scenario.test_steps)} steps.", self.GREEN))
        
        run_now = input(self._c("Run now with live visualization? (y/n): ", self.GREEN)).strip().lower()
        if run_now == 'y':
            self.simulator.run_scenario(custom_scenario)
        
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
    
    def display_results(self, result: TestResult):
        """Display test results"""
        self.clear_screen()
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
        
        nodes = create_topology_with_positions()
        links = create_enhanced_links()
        
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
        print(self._c("Version 3.0 - Enhanced with Live Visualization", self.GRAY))
        print()
        print("  Core Concepts:")
        print("  • Neural Processing: Microtubules as 'living routers' via Orch OR")
        print("  • Biological Topology: Mycelial growth for self-healing distribution")
        print("  • Quantum Synchronization: Non-local communication via entanglement")
        print("  • Massive Persistence: DNA storage at 10^18 bytes per cubic mm")
        print()
        print(self._c("  New in v3.0:", self.BOLD))
        print("  • Live HTML5 Canvas visualization")
        print("  • Animated packet transmission")
        print("  • Real-time coherence monitoring")
        print("  • Interactive zone highlighting")
        print("  • Browser-based topology viewer")
        print()
        print(self._c("  Architecture Layers:", self.BOLD))
        print("  L1: Bio-Physical Processing (Microtubule lattices)")
        print("  L2: Sub-Network Link (Mycelial Mesh with BLAP)")
        print("  L3: Interstellar Routing (Entanglement with BRR)")
        print("  L4: Quantum-Digital Bridge (SpinToBit conversion)")
        print("  L5: Galactic Application (QSP protocol)")
        print()
        print(self._c("-" * 50, self.GRAY))
        input("Press Enter to continue...")
    
    def run(self):
        """Main UI loop"""
        while True:
            self.print_menu()
            choice = input(self._c("Enter choice (0-7): ", self.GREEN)).strip()
            
            if choice == '1':
                self.run_scenario_menu()
            elif choice == '2':
                self.launch_visualizer_only()
            elif choice == '3':
                self.custom_scenario_menu()
            elif choice == '4':
                self.view_results_menu()
            elif choice == '5':
                self.export_results_menu()
            elif choice == '6':
                self.network_status_menu()
            elif choice == '7':
                self.about_menu()
            elif choice == '0':
                self.clear_screen()
                print(self._c("\nThank you for using BRNA Test Generator!\n", self.CYAN))
                sys.exit(0)
            else:
                print(self._c("Invalid choice. Press Enter to continue...", self.RED))
                input()


# ============================================================================
# PRE-DEFINED SCENARIOS (same as before, included for completeness)
# ============================================================================
# ============================================================================
# PRE-DEFINED TEST SCENARIOS (ADD THIS SECTION)
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
    
    scenario.nodes = create_topology_with_positions()
    scenario.links = create_enhanced_links()
    
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
    
    scenario.nodes = create_topology_with_positions()
    scenario.links = create_enhanced_links()
    
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
    
    scenario.nodes = create_topology_with_positions()
    scenario.links = create_enhanced_links()
    
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
    
    scenario.nodes = create_topology_with_positions()
    scenario.links = create_enhanced_links()
    
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
    
    scenario.nodes = create_topology_with_positions()
    scenario.links = create_enhanced_links()
    
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
    
    scenario.nodes = create_topology_with_positions()
    scenario.links = create_enhanced_links()
    
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
    
    scenario.nodes = create_topology_with_positions()
    scenario.links = create_enhanced_links()
    
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
    
    scenario.nodes = create_topology_with_positions()
    scenario.links = create_enhanced_links()
    
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
    
    scenario.nodes = create_topology_with_positions()
    scenario.links = create_enhanced_links()
    
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
        python_file="interstellar_relay.py",
        x=450, y=700
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
    
    scenario.nodes = create_topology_with_positions()
    scenario.links = create_enhanced_links()
    
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
# MAIN
# ============================================================================

def main():
    """Main entry point"""
    ui = EnhancedTerminalUI()
    
    # ASCII art banner
    banner = """
    ██████╗ ██████╗ ███╗   ██╗ █████╗     ██╗   ██╗██████╗ 
    ██╔══██╗██╔══██╗████╗  ██║██╔══██╗    ██║   ██║╚════██╗
    ██████╔╝██████╔╝██╔██╗ ██║███████║    ██║   ██║ █████╔╝
    ██╔══██╗██╔══██╗██║╚██╗██║██╔══██║    ╚██╗ ██╔╝██╔═══╝ 
    ██████╔╝██║  ██║██║ ╚████║██║  ██║     ╚████╔╝ ███████╗
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝      ╚═══╝  ╚══════╝
    """
    
    if ui.use_color:
        print(ui._c(banner, ui.CYAN))
        print(ui._c("Bio-Resonance Network Architecture Test Generator", ui.WHITE + ui.BOLD))
        print(ui._c("Enhanced Edition v3.0 - Live Visualization", ui.GREEN))
    else:
        print(banner)
        print("Bio-Resonance Network Architecture Test Generator")
        print("Enhanced Edition v3.0 - Live Visualization")
    
    print("\nLoading default topology...")
    time.sleep(1)
    ui.run()


if __name__ == "__main__":
    main()