import os
import sys
import subprocess
import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import json
import re

app = FastAPI(title="BRNA Galactic Command Portal")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulation state
simulation_status = {
    "running": False, 
    "last_logs": "", 
    "progress": 0, 
    "current_week": 0,
    "nodes": {},
    "events": [],
    "week_data": {
        "1": {"status": "pending", "nodes": []},
        "2": {"status": "pending", "handshake": None},
        "3": {"status": "pending", "routes": [], "storm": False},
        "4": {"status": "pending", "hitl": []}
    }
}

# Initial node status
NODES = ["NR-A", "NR-B", "NR-C", "NR-D", "NR-E", "DNA-Store", "NR-F", "HITL-GW", "Monitor-1", "Monitor-2", "QNode-A", "QNode-B", "QNode-C", "QNode-D", "SW-BIO", "SW-HITL"]

@app.on_event("startup")
async def startup_event():
    # Initialize node telemetry
    for node in NODES:
        simulation_status["nodes"][node] = {"fidelity": 0.0, "atp": 0.0, "status": "OFFLINE"}
    asyncio.create_task(simulate_telemetry())

async def simulate_telemetry():
    import random
    while True:
        if not simulation_status["running"]:
            # Idle jitter
            for node in NODES:
                if simulation_status["nodes"][node]["status"] != "OFFLINE":
                    f = simulation_status["nodes"][node]["fidelity"]
                    simulation_status["nodes"][node]["fidelity"] = round(max(0.1, min(1.0, f + random.uniform(-0.01, 0.01))), 3)
        await asyncio.sleep(2)

@app.get("/")
async def get_portal():
    # Fallback to index.html if it exists, otherwise return a simple message
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            return HTMLResponse(content=f.read())
    return {"message": "BRNA API Online. Use the Next.js frontend at port 3000."}

@app.post("/simulate")
async def run_simulation_api(background_tasks: BackgroundTasks):
    if simulation_status["running"]:
        return JSONResponse(status_code=400, content={"message": "Simulation already running"})
    
    # Reset state
    simulation_status["running"] = True
    simulation_status["last_logs"] = ""
    simulation_status["progress"] = 0
    simulation_status["current_week"] = 0
    simulation_status["events"] = []
    for week in simulation_status["week_data"]:
        simulation_status["week_data"][week]["status"] = "pending"
    
    background_tasks.add_task(execute_simulation)
    return {"message": "Simulation started"}

async def execute_simulation():
    core_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Github_artifact", "pro10-brna-v2"))
    venv_python = os.path.join(core_dir, ".venv/bin/python3")
    
    process = await asyncio.create_subprocess_exec(
        venv_python, os.path.join(core_dir, "run_simulation.py"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=core_dir
    )
    
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        decoded_line = line.decode().strip()
        if not decoded_line: continue
        
        simulation_status["last_logs"] += decoded_line + "\n"
        
        # Week markers
        if "WEEK 1" in decoded_line: 
            simulation_status["current_week"] = 1
            simulation_status["progress"] = 10
            simulation_status["week_data"]["1"]["status"] = "running"
        elif "WEEK 2" in decoded_line: 
            simulation_status["current_week"] = 2
            simulation_status["progress"] = 35
            simulation_status["week_data"]["2"]["status"] = "running"
            simulation_status["week_data"]["1"]["status"] = "complete"
        elif "WEEK 3" in decoded_line: 
            simulation_status["current_week"] = 3
            simulation_status["progress"] = 60
            simulation_status["week_data"]["3"]["status"] = "running"
            simulation_status["week_data"]["2"]["status"] = "complete"
            # Activate BIO and HITL switches visually
            simulation_status["nodes"]["SW-BIO"]["status"] = "ONLINE"
            simulation_status["nodes"]["SW-HITL"]["status"] = "ONLINE"
        elif "WEEK 4" in decoded_line: 
            simulation_status["current_week"] = 4
            simulation_status["progress"] = 85
            simulation_status["week_data"]["4"]["status"] = "running"
            simulation_status["week_data"]["3"]["status"] = "complete"
        elif "ALL WEEKS COMPLETE" in decoded_line: 
            simulation_status["current_week"] = 4
            simulation_status["progress"] = 100
            simulation_status["week_data"]["4"]["status"] = "complete"

        # Node Telemetry (Week 1)
        # Match: [NR-A] Held coherence for 100.0ms. ATP: 99.5%
        node_match = re.search(r"\[(NR-\w|DNA-Store|HITL-GW|Monitor-\d|QNode-\w)\] Held coherence for ([\d.]+)ms\. ATP: ([\d.]+)%", decoded_line)
        if node_match:
            node_id, coherence, atp = node_match.groups()
            simulation_status["nodes"][node_id] = {
                "fidelity": float(coherence)/120.0, # Scale to 0-1
                "atp": float(atp),
                "status": "ONLINE"
            }
            simulation_status["events"].append({"week": 1, "msg": f"Node {node_id} synchronized", "type": "node"})

        # Mesh Activation (Week 3)
        if "[MESH] Node added: " in decoded_line:
            mesh_match = re.search(r"Node added: ([\w-]+)", decoded_line)
            if mesh_match:
                n_id = mesh_match.group(1)
                simulation_status["nodes"][n_id]["status"] = "ONLINE"
                simulation_status["nodes"][n_id]["atp"] = 100.0
                simulation_status["nodes"][n_id]["fidelity"] = 0.9

        # Handshake (Week 2)
        if "[QSP] Handshake: " in decoded_line:
            simulation_status["week_data"]["2"]["handshake"] = decoded_line.replace("[QSP] Handshake: ", "")
            simulation_status["events"].append({"week": 2, "msg": "Quantum handshake initialized", "type": "sync"})

        # Storm/Heal (Week 3)
        if "[STORM]" in decoded_line:
            simulation_status["week_data"]["3"]["storm"] = True
            simulation_status["events"].append({"week": 3, "msg": "DECOHERENCE STORM DETECTED", "type": "alert"})
        if "[HEAL]" in decoded_line:
            simulation_status["events"].append({"week": 3, "msg": "Mycelial network self-healed", "type": "heal"})
        
        # Routing (Week 3)
        if "[BRR] Route" in decoded_line:
            simulation_status["week_data"]["3"]["routes"].append(decoded_line)

        # HITL (Week 4)
        if "[HITL]" in decoded_line:
            simulation_status["week_data"]["4"]["hitl"].append(decoded_line)
            res = "APPROVED" if "APPROVED" in decoded_line else "DROPPED"
            simulation_status["events"].append({"week": 4, "msg": f"Package {res} by HITL Gateway", "type": "gw"})

    await process.wait()
    simulation_status["running"] = False

@app.get("/status")
async def get_status():
    return simulation_status

@app.post("/test")
async def run_tests():
    core_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Github_artifact", "pro10-brna-v2"))
    venv_python = os.path.join(core_dir, ".venv/bin/python3")
    
    result = subprocess.run([venv_python, "-m", "pytest", os.path.join(core_dir, "tests/")], 
                            capture_output=True, text=True,
                            cwd=core_dir)
    return {"exit_code": result.returncode, "summary": result.stdout}

# ============================================================================
# TEST SCENARIOS (from mock_up.py)
# ============================================================================
import random as _rng

TEST_SCENARIOS = {
    "1": {
        "name": "Orch OR Coherence Test",
        "description": "Verify neural repeaters maintain quantum coherence above 85% under normal load",
        "zone": "core",
        "tags": ["core", "quantum", "coherence", "orch-or"],
        "dataFlow": ["NR-A", "NR-B", "NR-D", "NR-C"],
        "steps": [
            {"step": 1, "name": "Initialize microtubule bundles", "command": "init_microtubule()", "target": "NR-A", "expected": "Coherence > 90%"},
            {"step": 2, "name": "Apply Orch OR trigger", "command": "apply_orch_trigger(threshold=0.95)", "target": "NR-A,NR-B,NR-D", "expected": "OR collapse probability < 5%"},
            {"step": 3, "name": "Measure decoherence rate", "command": "measure_decoherence(duration=1000)", "target": "all_core_routers", "expected": "Decoherence < 3.0 ns"},
            {"step": 4, "name": "Apply metabolic stress", "command": "reduce_nutrients(level=50)", "target": "NR-C", "expected": "Coherence drop < 15%"},
        ]
    },
    "2": {
        "name": "DNA Store Recovery Test",
        "description": "Verify Reed-Solomon error correction can recover data with 10% corruption",
        "zone": "bio",
        "tags": ["bio", "storage", "dna", "error-correction"],
        "dataFlow": ["NR-D", "SW-BIO", "DNA-Store", "SW-BIO", "NR-F"],
        "steps": [
            {"step": 1, "name": "Write test data to DNA", "command": "dna_write(payload='TEST_PATTERN_0xF3A7')", "target": "DNA-Store", "expected": "Write successful"},
            {"step": 2, "name": "Apply Reed-Solomon encoding", "command": "rs_encode(symbols=(255,223))", "target": "DNA-Store", "expected": "Redundancy 14%"},
            {"step": 3, "name": "Simulate sequence corruption", "command": "corrupt_dna(rate=0.10)", "target": "DNA-Store", "expected": "10% errors introduced"},
            {"step": 4, "name": "Recover data with ECC", "command": "rs_decode()", "target": "DNA-Store", "expected": "100% recovery"},
        ]
    },
    "3": {
        "name": "Entanglement Swapping Test",
        "description": "Create quantum link between non-adjacent nodes via swapping",
        "zone": "entangle",
        "tags": ["quantum", "entanglement", "swapping", "non-local"],
        "dataFlow": ["QNode-A", "QNode-B", "QNode-C", "QNode-D"],
        "steps": [
            {"step": 1, "name": "Create Bell pair A-B", "command": "create_bell_pair(state='|Φ+⟩')", "target": "QNode-A,QNode-B", "expected": "Fidelity > 98%"},
            {"step": 2, "name": "Create Bell pair C-D", "command": "create_bell_pair(state='|Ψ-⟩')", "target": "QNode-C,QNode-D", "expected": "Fidelity > 98%"},
            {"step": 3, "name": "Perform entanglement swap B-C", "command": "entanglement_swap(B, C)", "target": "QNode-B,QNode-C", "expected": "Swap success > 90%"},
            {"step": 4, "name": "Verify A-D entanglement", "command": "bell_test(A, D)", "target": "QNode-A,QNode-D", "expected": "CHSH > 2.7"},
        ]
    },
    "4": {
        "name": "HITL Override Test",
        "description": "Verify human operator can override critical routing decisions",
        "zone": "hitl",
        "tags": ["hitl", "governance", "ethics", "override"],
        "dataFlow": ["NR-A", "NR-D", "SW-HITL", "HITL-GW", "SW-HITL", "Monitor-1"],
        "steps": [
            {"step": 1, "name": "Generate critical packet", "command": "send_critical(priority='CRITICAL')", "target": "NR-A", "expected": "Ethics engine flags packet"},
            {"step": 2, "name": "Queue for HITL review", "command": "hitl_queue()", "target": "HITL-GW", "expected": "Packet queued, operator notified"},
            {"step": 3, "name": "Simulate operator approval", "command": "operator_override(decision='APPROVE')", "target": "HITL-GW", "expected": "Override recorded"},
            {"step": 4, "name": "Verify packet delivery", "command": "check_delivery()", "target": "NR-D", "expected": "Packet delivered"},
        ]
    },
    "5": {
        "name": "Mycelial Self-Healing Test",
        "description": "Verify mesh reroutes around failed links using fungal growth algorithms",
        "zone": "bio",
        "tags": ["mycelial", "mesh", "self-healing", "resilience"],
        "dataFlow": ["NR-A", "NR-D", "SW-BIO", "NR-E", "SW-BIO", "NR-F"],
        "steps": [
            {"step": 1, "name": "Establish baseline routing", "command": "compute_all_paths()", "target": "SW-BIO", "expected": "All paths optimal"},
            {"step": 2, "name": "Simulate link failure", "command": "fail_link(link='SW-BIO-NR-E')", "target": "SW-BIO", "expected": "Link down, rerouting triggered"},
            {"step": 3, "name": "Measure healing time", "command": "monitor_reroute()", "target": "mycelial_mesh", "expected": "Healing < 50 ms"},
            {"step": 4, "name": "Verify new path", "command": "trace_route('NR-A','NR-E')", "target": "network", "expected": "Alternative path active"},
        ]
    },
    "6": {
        "name": "QSP Handshake Test",
        "description": "Verify Quantum Sync Protocol establishes connection via phase synchronization",
        "zone": "core",
        "tags": ["protocol", "qsp", "handshake", "phase-sync"],
        "dataFlow": ["NR-A", "NR-D", "NR-B", "NR-D", "NR-A"],
        "steps": [
            {"step": 1, "name": "Send QSP SYN", "command": "qsp_send(flags='SYN')", "target": "NR-A", "expected": "SYN sent"},
            {"step": 2, "name": "Receive SYN-ACK", "command": "qsp_receive()", "target": "NR-D", "expected": "SYN-ACK with fidelity 97%"},
            {"step": 3, "name": "Complete handshake", "command": "qsp_send(flags='ACK')", "target": "NR-A", "expected": "Session established"},
            {"step": 4, "name": "Verify phase sync", "command": "measure_phase_coherence()", "target": "NR-A,NR-D", "expected": "Phase diff < 0.1 rad"},
        ]
    },
    "7": {
        "name": "Paradox Prevention Test",
        "description": "Verify PPP drops causality-violating packets",
        "zone": "hitl",
        "tags": ["paradox", "causality", "ppp", "chronological"],
        "dataFlow": ["NR-A", "NR-D", "SW-HITL", "HITL-GW", "SW-HITL", "Monitor-2"],
        "steps": [
            {"step": 1, "name": "Generate normal packet", "command": "send_packet(timestamp='+10ms')", "target": "NR-A", "expected": "Packet allowed"},
            {"step": 2, "name": "Generate causality violation", "command": "send_packet(timestamp='-50ms')", "target": "NR-B", "expected": "Packet flagged"},
            {"step": 3, "name": "Verify PPP drop", "command": "check_ppp_filter()", "target": "HITL-GW", "expected": "Packet dropped, violation logged"},
            {"step": 4, "name": "Check entropy guard", "command": "measure_entropy_change()", "target": "destination", "expected": "Local entropy unchanged"},
        ]
    },
    "8": {
        "name": "Metabolic Cooling Test",
        "description": "Verify temperature control maintains coherence",
        "zone": "core",
        "tags": ["bio", "metabolic", "cooling", "temperature"],
        "dataFlow": ["NR-A", "NR-B", "NR-C", "NR-D"],
        "steps": [
            {"step": 1, "name": "Set baseline temperature", "command": "set_temperature(temp=37.0)", "target": "NR-A", "expected": "Coherence 94%"},
            {"step": 2, "name": "Simulate overheating", "command": "increase_temp(delta=3.5)", "target": "NR-A", "expected": "Coherence drops"},
            {"step": 3, "name": "Activate metabolic cooling", "command": "metabolic_cooling(intensity=0.8)", "target": "NR-A", "expected": "Temperature decreases"},
            {"step": 4, "name": "Verify recovery", "command": "measure_coherence()", "target": "NR-A", "expected": "Coherence > 90%"},
        ]
    },
    "9": {
        "name": "Galactic Routing Test",
        "description": "Simulate routing from Earth to Proxima with zero latency",
        "zone": "entangle",
        "tags": ["interstellar", "routing", "zero-latency", "entanglement"],
        "dataFlow": ["NR-A", "NR-D", "SW-BIO", "DNA-Store", "SW-BIO", "NR-D", "QNode-A", "QNode-B", "QNode-C", "QNode-D"],
        "steps": [
            {"step": 1, "name": "Establish entanglement chain", "command": "create_entanglement_chain(A->B->C->D)", "target": "entanglement_zone", "expected": "Chain length 4, all entangled"},
            {"step": 2, "name": "Send packet via QSP", "command": "send_packet_qsp(payload='HELLO')", "target": "NR-A", "expected": "Packet synchronized"},
            {"step": 3, "name": "Measure arrival time", "command": "measure_arrival()", "target": "QNode-D", "expected": "Δt ≈ 0 ms"},
            {"step": 4, "name": "Verify data integrity", "command": "compare_payload()", "target": "QNode-D", "expected": "Payload match"},
        ]
    },
    "10": {
        "name": "Resonance Cost Routing Test",
        "description": "Verify modified Dijkstra with C_R metric finds optimal path",
        "zone": "bio",
        "tags": ["routing", "resonance", "dijkstra", "cost"],
        "dataFlow": ["NR-A", "NR-D", "SW-BIO", "DNA-Store"],
        "steps": [
            {"step": 1, "name": "Calculate resonance costs", "command": "compute_resonance_costs()", "target": "all_links", "expected": "C_R values computed"},
            {"step": 2, "name": "Run modified Dijkstra", "command": "dijkstra_resonance(src='NR-A',dst='DNA-Store')", "target": "NR-D", "expected": "Path found with min C_R"},
            {"step": 3, "name": "Compare with shortest path", "command": "compare_paths()", "target": "routing_engine", "expected": "Resonance path differs if coherence low"},
            {"step": 4, "name": "Verify path quality", "command": "measure_path_fidelity()", "target": "selected_path", "expected": "F_R > 90%"},
        ]
    },
}

# Test execution state
test_execution_status = {
    "running": False,
    "test_id": None,
    "test_name": "",
    "current_step": 0,
    "total_steps": 0,
    "step_results": [],
    "data_flow": [],
    "active_hop": -1,  # which hop index is currently being animated
    "status": "idle",  # idle, running, passed, failed, warning
}

@app.get("/test-scenarios")
async def get_test_scenarios():
    """Return all 10 test scenarios for the UI"""
    return TEST_SCENARIOS

@app.post("/run-test/{test_id}")
async def run_test_scenario(test_id: str, background_tasks: BackgroundTasks):
    """Run a specific test scenario"""
    if test_id not in TEST_SCENARIOS:
        return JSONResponse(status_code=404, content={"message": f"Test {test_id} not found"})
    if test_execution_status["running"]:
        return JSONResponse(status_code=400, content={"message": "A test is already running"})
    
    scenario = TEST_SCENARIOS[test_id]
    test_execution_status["running"] = True
    test_execution_status["test_id"] = test_id
    test_execution_status["test_name"] = scenario["name"]
    test_execution_status["current_step"] = 0
    test_execution_status["total_steps"] = len(scenario["steps"])
    test_execution_status["step_results"] = []
    test_execution_status["data_flow"] = scenario["dataFlow"]
    test_execution_status["active_hop"] = -1
    test_execution_status["status"] = "running"
    
    background_tasks.add_task(execute_test_scenario, test_id)
    return {"message": f"Test '{scenario['name']}' started", "data_flow": scenario["dataFlow"]}

async def execute_test_scenario(test_id: str):
    """Execute each step of a test scenario with delays for visualization"""
    scenario = TEST_SCENARIOS[test_id]
    data_flow = scenario["dataFlow"]
    
    for i, step in enumerate(scenario["steps"]):
        test_execution_status["current_step"] = step["step"]
        # Animate data flow hop for this step
        hop_index = min(i, len(data_flow) - 2)
        test_execution_status["active_hop"] = hop_index
        
        await asyncio.sleep(2)  # simulate step execution time
        
        # Determine result (high success probability)
        roll = _rng.random()
        if roll < 0.90:
            status = "passed"
            measured = step["expected"]
        elif roll < 0.97:
            status = "warning"
            measured = f"Near threshold: {step['expected']}"
        else:
            status = "failed"
            measured = f"Below expected: {step['expected']}"
        
        test_execution_status["step_results"].append({
            "step": step["step"],
            "name": step["name"],
            "command": step["command"],
            "target": step["target"],
            "expected": step["expected"],
            "measured": measured,
            "status": status,
        })
    
    # Final status
    failed = any(r["status"] == "failed" for r in test_execution_status["step_results"])
    warned = any(r["status"] == "warning" for r in test_execution_status["step_results"])
    test_execution_status["status"] = "failed" if failed else ("warning" if warned else "passed")
    test_execution_status["active_hop"] = -1
    test_execution_status["running"] = False

@app.get("/test-status")
async def get_test_status():
    """Return current test execution status"""
    return test_execution_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
