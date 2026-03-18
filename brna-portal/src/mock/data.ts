export const mockTestScenarios = {
  test_1: {
    name: "Core Router Validation",
    description: "Verifies basic physical connectivity and latency between Core Routers NR-A, NR-B, and NR-C.",
    zone: "core",
    steps: [
      { name: "Ping NR-A to NR-B", command: "ping NR-B" },
      { name: "Ping NR-B to NR-C", command: "ping NR-C" },
    ],
  },
  test_2: {
    name: "Bio-Switch Handshake",
    description: "Ensures the biological gateway switch is properly connected to the core network and DNA-Store.",
    zone: "bio",
    steps: [
      { name: "Check Interface SW-BIO", command: "show interfaces" },
      { name: "Test DNA-Store Access", command: "curl http://dna-store:8080" },
    ],
  },
  test_3: {
    name: "Quantum Synchronization",
    description: "Runs a full QSP handshake between QNodes to establish entanglement pairs.",
    zone: "entangle",
    steps: [
      { name: "Initialize QNode-A", command: "qnode-init A" },
      { name: "Establish Entanglement Pair", command: "qsp-sync --nodes A,B" },
      { name: "Measure Coherence", command: "qsp-measure" },
    ],
  },
  test_4: {
    name: "HITL Monitoring Active",
    description: "Validates human-in-the-loop dashboard telemetry and gateway status.",
    zone: "hitl",
    steps: [
      { name: "Verify Monitor-1 Gateway", command: "check-gateway Monitor-1" },
      { name: "Verify Monitor-2 Load", command: "top -n 1 | grep Monitor-2" },
    ],
  },
  test_5: {
    name: "Mycelial Path Recovery",
    description: "Simulates a link failure and verifies the self-healing mycelial rerouting logic.",
    zone: "core",
    steps: [
      { name: "Shutdown NR-A Fa0/1", command: "interface Fa0/1 shutdown" },
      { name: "Wait for Convergence", command: "sleep 2" },
      { name: "Verify Alternative Path", command: "traceroute NR-D" },
    ],
  },
  test_6: {
    name: "ATP Level Optimization",
    description: "Optimizes the ATP metabolic levels across Bio-Nodes to balance power consumption.",
    zone: "bio",
    steps: [
      { name: "Query ATP Status", command: "atp-query --all" },
      { name: "Rebalance Metabolic Load", command: "atp-balance" },
    ],
  },
  test_7: {
    name: "QSP Swap Validation",
    description: "Performs a quantum swap operation between non-adjacent entangle nodes.",
    zone: "entangle",
    steps: [
      { name: "Prepare Swap QNode-B", command: "qsp-prep B" },
      { name: "Execute Quantum Swap", command: "qsp-swap B-C" },
      { name: "Verify End-to-End Link", command: "qsp-verify A-D" },
    ],
  },
  test_8: {
    name: "Gateway Audit Protocol",
    description: "Runs a full security audit on the HITL Gateway and monitoring stations.",
    zone: "hitl",
    steps: [
      { name: "Verify Audit Signature", command: "audit-check --sign" },
      { name: "Log Integrity Check", command: "check-logs --integrity" },
    ],
  },
  test_9: {
    name: "Bio-Physical Resonance",
    description: "Measures the resonance frequency between biological and electronic components.",
    zone: "bio",
    steps: [
      { name: "Sync Frequency Generators", command: "res-sync" },
      { name: "Measure Resonance Gap", command: "res-measure" },
    ],
  },
  test_10: {
    name: "Sub-Quantum Loopback",
    description: "Final validation of the sub-quantum messaging layer across all core zones.",
    zone: "core",
    steps: [
      { name: "Initiate Loopback Test", command: "sq-loopback --start" },
      { name: "Analyze Packet Fidelity", command: "sq-analyze" },
    ],
  },
};

export const generateMockStatusData = (isRunning: boolean, progress: number) => {
  const currentWeek = progress < 25 ? 1 : progress < 50 ? 2 : progress < 75 ? 3 : 4;
  
  return {
    running: isRunning,
    progress: progress,
    current_week: currentWeek,
    week_data: {
      1: { status: progress >= 25 ? "complete" : "in-progress" },
      2: { status: progress >= 50 ? "complete" : progress >= 25 ? "in-progress" : "pending" },
      3: { status: progress >= 75 ? "complete" : progress >= 50 ? "in-progress" : "pending" },
      4: { status: progress >= 100 ? "complete" : progress >= 75 ? "in-progress" : "pending" }
    },
    events: progress === 0 ? [] : [
      { msg: "System Boot Initialized", type: "system", week: 1 },
      { msg: "Bio-Physical Sync Started", type: "system", week: 1 },
      ...(progress >= 25 ? [{ msg: "QSP Handshake Established", type: "sync", week: 2 }] : []),
      ...(progress >= 50 ? [{ msg: "Mycelial Topology Mapping Complete", type: "system", week: 3 }] : []),
      ...(progress >= 75 ? [{ msg: "HITL Gateway Accessible", type: "system", week: 4 }] : []),
      ...(progress >= 100 ? [{ msg: "Simulation Completed Successfully", type: "heal", week: 4 }] : []),
    ],
    nodes: {
      "NR-A": { status: "ONLINE", fidelity: 0.99, atp: 88 + Math.random() * 5 },
      "NR-B": { status: "ONLINE", fidelity: 0.98, atp: 91 + Math.random() * 5 },
      "NR-C": { status: "ONLINE", fidelity: 0.95, atp: 85 + Math.random() * 5 },
      "NR-D": { status: "ONLINE", fidelity: 0.97, atp: 89 + Math.random() * 5 },
      "SW-BIO": { status: "ONLINE", fidelity: 0.92, atp: 75 + Math.random() * 5 },
      "DNA-Store": { status: "ONLINE", fidelity: 0.96, atp: 95 + Math.random() * 5 },
      "NR-E": { status: "ONLINE", fidelity: 0.89, atp: 82 + Math.random() * 5 },
      "NR-F": { status: "ONLINE", fidelity: 0.91, atp: 84 + Math.random() * 5 },
      "SW-HITL": { status: "ONLINE", fidelity: 0.94, atp: 88 + Math.random() * 5 },
      "HITL-GW": { status: "ONLINE", fidelity: 0.99, atp: 92 + Math.random() * 5 },
      "Monitor-1": { status: "ONLINE", fidelity: 0.98, atp: 90 + Math.random() * 5 },
      "Monitor-2": { status: "ONLINE", fidelity: 0.97, atp: 89 + Math.random() * 5 },
      "QNode-A": { status: progress >= 25 ? "ONLINE" : "OFFLINE", fidelity: 0.99, atp: 100 },
      "QNode-B": { status: progress >= 25 ? "ONLINE" : "OFFLINE", fidelity: 0.99, atp: 100 },
      "QNode-C": { status: progress >= 25 ? "ONLINE" : "OFFLINE", fidelity: 0.98, atp: 99 },
      "QNode-D": { status: progress >= 25 ? "ONLINE" : "OFFLINE", fidelity: 0.95, atp: 96 },
    }
  };
};

export const generateMockTestStatus = (running: boolean, testId: string | null, progress: number) => {
  if (!testId || !running) {
    if (testId && !running) {
        // Returned recently finished state
        const scenario: any = (mockTestScenarios as any)[testId];
        return {
          status: "passed",
          running: false,
          test_name: scenario?.name || "Unknown",
          current_step: scenario?.steps.length || 0,
          total_steps: scenario?.steps.length || 0,
          active_hop: -1,
          data_flow: [],
          step_results: scenario?.steps.map((s: any, idx: number) => ({
            step: idx + 1,
            name: s.name,
            status: "passed",
            command: s.command,
            measured: "success"
          })) || []
        };
    }
    return { status: "idle", running: false };
  }

  const scenario: any = (mockTestScenarios as any)[testId];
  const totalSteps = scenario?.steps.length || 2;
  const currentStep = Math.min(totalSteps, Math.floor((progress / 100) * totalSteps));
  
  const step_results = [];
  for (let i = 0; i < currentStep; i++) {
    step_results.push({
      step: i + 1,
      name: scenario.steps[i].name,
      status: "passed",
      command: scenario.steps[i].command,
      measured: "0.99ms" // mock measurement
    });
  }
  
  // Data flow animation mock 
  const mockFlows: Record<string, string[]> = {
    test_1: ["NR-A", "NR-B", "NR-C", "NR-D"],
    test_2: ["NR-D", "SW-BIO", "DNA-Store"],
    test_3: ["QNode-A", "QNode-B", "QNode-C", "QNode-D"],
    test_4: ["SW-HITL", "HITL-GW", "Monitor-1"],
    test_5: ["NR-A", "NR-D", "NR-B"],
    test_6: ["SW-BIO", "NR-E", "NR-F"],
    test_7: ["QNode-B", "QNode-C", "QNode-D"],
    test_8: ["HITL-GW", "Monitor-2", "SW-HITL"],
    test_9: ["DNA-Store", "SW-BIO", "NR-F"],
    test_10: ["NR-A", "NR-B", "NR-C", "NR-D", "SW-BIO", "SW-HITL"],
  };

  const data_flow = mockFlows[testId] || ["NR-A", "SW-HITL"];
  const maxActiveHop = Math.max(0, data_flow.length - 2);
  const active_hop = Math.floor((progress / 100) * (maxActiveHop + 1));

  return {
    status: "running",
    running: true,
    test_name: scenario?.name || "Mock Test",
    current_step: currentStep,
    total_steps: totalSteps,
    active_hop,
    data_flow,
    step_results
  };
};
