"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Layers,
  Cpu,
  Zap,
  Globe,
  Database,
  ShieldCheck,
  Activity,
  ArrowRight,
  ChevronDown,
  Network,
  Dna,
  Radio,
  Lock,
} from "lucide-react";

/* ── 5-layer Bio-Quantum Stack data ── */
const LAYERS = [
  {
    id: "L1",
    name: "Bio-Physical Layer (Orch OR)",
    shortName: "L1 — Orch OR",
    icon: <Cpu className="w-5 h-5" />,
    color: "#3b82f6",
    gradient: "from-blue-600 to-blue-400",
    ptDevice: "Core Routers (NR-A … NR-D)",
    pythonModule: "microtubule.py, orch_or.py",
    description:
      "The Bio-Physical layer simulates quantum coherence inside neuronal microtubules. Each Neural Repeater node maintains a qubit in superposition for ≥ 100 ms and then triggers Orchestrated Objective Reduction (Orch OR), collapsing the qubit to a definite spin state (|0⟩ or |1⟩).",
    keyMetrics: ["Coherence Time ≥ 100 ms", "ATP Reserve > 95 %", "Resonance Cost (C_R)"],
    howItWorks: [
      "Initialize a qubit in superposition |ψ⟩ = α|0⟩ + β|1⟩",
      "Hold coherence using metabolic cooling (ATP hydrolysis)",
      "Gravitational self-energy triggers objective collapse",
      "Collapsed spin state becomes the routing basis for upper layers",
    ],
  },
  {
    id: "L2",
    name: "Mycelial Mesh Layer (BLAP)",
    shortName: "L2 — BLAP",
    icon: <Network className="w-5 h-5" />,
    color: "#8b5cf6",
    gradient: "from-purple-600 to-purple-400",
    ptDevice: "SW-BIO Switch",
    pythonModule: "mycelial_mesh.py",
    description:
      "The Mycelial Mesh emulates a living network fabric inspired by fungal mycelia. Each node is assigned a Bio-Layered Address Protocol (BLAP) address. The mesh self-heals when links fail due to decoherence storms.",
    keyMetrics: ["BLAP Address (64-bit)", "Link Cost (resonance-weighted)", "Self-Heal Latency"],
    howItWorks: [
      "Nodes register with unique BLAP addresses and IP assignments",
      "Mycelial links are added with resonance-weighted costs",
      "Decoherence storms can sever links between nodes",
      "Mycelial self-healing regrows links at a higher cost post-repair",
    ],
  },
  {
    id: "L3",
    name: "Interstellar Routing Layer (BRR)",
    shortName: "L3 — BRR",
    icon: <Globe className="w-5 h-5" />,
    color: "#10b981",
    gradient: "from-emerald-600 to-emerald-400",
    ptDevice: "Routers (NR-A to NR-D)",
    pythonModule: "routing.py",
    description:
      "The Bio-Resonance Routing (BRR) protocol finds the optimal path through the mycelial mesh. It computes the cheapest resonance-weighted path, factoring in the Resonance Cost (C_R) of each hop. Entanglement swapping extends quantum channels.",
    keyMetrics: ["Total Route C_R", "Hop Count", "Entanglement Swap Success"],
    howItWorks: [
      "Dijkstra-based shortest-path using resonance cost weights",
      "Routes are validated against ATP thresholds at each hop",
      "Entanglement swap extends non-local links: A↔B↔C → A↔C",
      "Routing table updates after mycelial healing events",
    ],
  },
  {
    id: "L4",
    name: "Quantum-Digital Bridge",
    shortName: "L4 — SpinToBit",
    icon: <Zap className="w-5 h-5" />,
    color: "#f59e0b",
    gradient: "from-amber-600 to-amber-400",
    ptDevice: "HITL-GW PC",
    pythonModule: "spin_bridge.py, hitl_gateway.py",
    description:
      "The SpinToBit Bridge converts quantum spin states into classical digital data. It groups spins into bytes, applies Reed-Solomon error correction, and formats the output as UTF-8. The HITL Gateway applies PPP ethical filtering.",
    keyMetrics: ["Bit Error Rate", "Entropy Delta (ΔS)", "PPP Decision (Approve / Drop)"],
    howItWorks: [
      "Collect 8 spin states → group into 1 byte",
      "Apply Reed-Solomon forward error correction",
      "Compute Shannon entropy checksum for integrity",
      "HITL Gateway checks entropy delta: ΔS > 0 → approve, else drop (PPP violation)",
    ],
  },
  {
    id: "L5",
    name: "Galactic Application Layer (QSP)",
    shortName: "L5 — QSP",
    icon: <Radio className="w-5 h-5" />,
    color: "#ec4899",
    gradient: "from-pink-600 to-pink-400",
    ptDevice: "Monitor PCs",
    pythonModule: "qsp_protocol.py, dashboard.py",
    description:
      "The Quantum Synchronization Protocol (QSP) orchestrates resonance handshakes between nodes. It establishes entanglement pairs, synchronizes phase states, and frames data for transmission across the bio-quantum network.",
    keyMetrics: ["Phase Sync Δ < 0.1 rad", "Entanglement Pair ID", "QSP Frame Integrity"],
    howItWorks: [
      "Source node broadcasts a RESONATE signal with its phase state",
      "Destination node replies with PHASE-SYNC if phase delta < threshold",
      "ENTANGLE step generates a shared pair ID via Bell measurement",
      "Data is framed as QSPFrame with payload, phase, and ATP metadata",
    ],
  },
];

/* ── Topology Zones ── */
const ZONES = [
  {
    name: "Core Fabric",
    color: "#3b82f6",
    nodes: ["NR-A (10.0.1.1)", "NR-B (10.0.1.2)", "NR-C (10.0.1.3)", "NR-D (10.0.1.4)"],
    role: "Central neural routing mesh. NR-D acts as the hub-router connecting all subnets.",
  },
  {
    name: "Bio Fabric",
    color: "#8b5cf6",
    nodes: ["NR-E (10.0.2.1)", "DNA-Store (10.0.2.2)", "NR-F (10.0.2.3)"],
    role: "Biological processing zone with DNA-encoded persistent storage.",
  },
  {
    name: "HITL Fabric",
    color: "#f59e0b",
    nodes: ["HITL-GW (10.0.3.1)", "Monitor-1 (10.0.3.2)", "Monitor-2 (10.0.3.3)"],
    role: "Human-in-the-Loop oversight. Ethical PPP filtering and real-time dashboards.",
  },
  {
    name: "Entangle Fabric",
    color: "#10b981",
    nodes: ["QNode-A (10.0.4.1)", "QNode-B (10.0.4.2)", "QNode-C (10.0.4.3)", "QNode-D (10.0.4.4)"],
    role: "Quantum entanglement backbone for zero-latency non-local data transfer.",
  },
];

const SPRINT = [
  { week: 1, title: "Bio-Physical Simulation", focus: "MicrotubuleBundle class, Orch OR trigger, coherence hold" },
  { week: 2, title: "QSP Protocol", focus: "Resonance handshake, QSPFrame framing, entanglement pairs" },
  { week: 3, title: "Mycelial Topology", focus: "14-node mesh, BRR routing, decoherence storm + self-healing" },
  { week: 4, title: "Interface & Dashboard", focus: "SpinToBit bridge, HITL PPP filter, live terminal dashboard" },
];

/* ──────────────── PAGE ──────────────── */
export default function ArchitecturePage() {
  const [expandedLayer, setExpandedLayer] = useState<string | null>("L1");

  return (
    <main className="min-h-screen bg-[#050a14] text-slate-200">
      {/* HERO */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-blue-500/5 via-purple-500/5 to-transparent pointer-events-none" />
        <div className="max-w-5xl mx-auto px-6 py-20 text-center relative z-10">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <p className="text-xs font-bold text-blue-400 uppercase tracking-[0.3em] mb-4 flex items-center justify-center gap-2">
              <Dna className="w-4 h-4" /> CP352005 Networks — March 2026
            </p>
            <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent leading-tight">
              Bio-Resonance Network<br />Architecture
            </h1>
            <p className="text-slate-400 text-lg mt-6 max-w-2xl mx-auto leading-relaxed">
              A paradigm shift from mechanical silicon-based networking to <strong className="text-slate-200">living, bio-quantum systems</strong>.
              BRNA orchestrates Objective Reduction across a biological fabric to achieve near-infinite data persistence
              and zero-latency interstellar communication.
            </p>
          </motion.div>
        </div>
      </section>

      <div className="max-w-5xl mx-auto px-6 pb-20 space-y-20">

        {/* ─── 5-LAYER STACK ─── */}
        <section>
          <SectionHeader icon={<Layers className="w-5 h-5 text-blue-400" />} title="5-Layer Bio-Quantum Stack" />

          {/* Quick overview table */}
          <div className="overflow-x-auto mb-8">
            <table className="w-full text-xs font-mono">
              <thead>
                <tr className="border-b border-slate-800 text-slate-500 uppercase tracking-widest">
                  <th className="text-left py-3 px-4">Layer</th>
                  <th className="text-left py-3 px-4">Name</th>
                  <th className="text-left py-3 px-4 hidden md:table-cell">PT Device</th>
                  <th className="text-left py-3 px-4 hidden md:table-cell">Python Module</th>
                </tr>
              </thead>
              <tbody>
                {[...LAYERS].reverse().map(l => (
                  <tr key={l.id} className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
                    <td className="py-3 px-4 font-bold" style={{ color: l.color }}>{l.id}</td>
                    <td className="py-3 px-4 text-slate-300">{l.name}</td>
                    <td className="py-3 px-4 text-slate-500 hidden md:table-cell">{l.ptDevice}</td>
                    <td className="py-3 px-4 text-slate-500 hidden md:table-cell">{l.pythonModule}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Expandable layer cards */}
          <div className="space-y-3">
            {LAYERS.map((layer, idx) => (
              <motion.div
                key={layer.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.05 }}
              >
                <button
                  onClick={() => setExpandedLayer(expandedLayer === layer.id ? null : layer.id)}
                  className={`w-full text-left p-5 rounded-2xl border transition-all ${
                    expandedLayer === layer.id
                      ? "bg-slate-900/80 border-slate-700"
                      : "bg-slate-900/40 border-slate-800/50 hover:bg-slate-900/60 hover:border-slate-700/50"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div
                        className="w-10 h-10 rounded-xl flex items-center justify-center"
                        style={{ backgroundColor: `${layer.color}20`, color: layer.color }}
                      >
                        {layer.icon}
                      </div>
                      <div>
                        <span className="text-[10px] font-bold uppercase tracking-widest" style={{ color: layer.color }}>
                          {layer.id}
                        </span>
                        <h3 className="text-sm font-bold text-slate-200">{layer.name}</h3>
                      </div>
                    </div>
                    <ChevronDown
                      className={`w-4 h-4 text-slate-500 transition-transform ${expandedLayer === layer.id ? "rotate-180" : ""}`}
                    />
                  </div>
                </button>

                <AnimatePresence>
                  {expandedLayer === layer.id && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.25 }}
                      className="overflow-hidden"
                    >
                      <div className="px-5 pb-5 pt-2 bg-slate-900/60 rounded-b-2xl border border-t-0 border-slate-800/50 space-y-5">
                        <p className="text-sm text-slate-400 leading-relaxed">{layer.description}</p>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {/* Key Metrics */}
                          <div className="bg-slate-800/40 rounded-xl p-4 border border-slate-700/30">
                            <h4 className="text-[10px] font-bold uppercase tracking-widest text-slate-500 mb-3">Key Metrics</h4>
                            <ul className="space-y-2">
                              {layer.keyMetrics.map((m, i) => (
                                <li key={i} className="flex items-center gap-2 text-xs text-slate-300">
                                  <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: layer.color }} />
                                  {m}
                                </li>
                              ))}
                            </ul>
                          </div>

                          {/* How It Works */}
                          <div className="bg-slate-800/40 rounded-xl p-4 border border-slate-700/30">
                            <h4 className="text-[10px] font-bold uppercase tracking-widest text-slate-500 mb-3">How It Works</h4>
                            <ol className="space-y-2">
                              {layer.howItWorks.map((step, i) => (
                                <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                                  <span className="flex-shrink-0 w-5 h-5 rounded-full bg-slate-700 flex items-center justify-center text-[10px] font-bold text-slate-400 mt-0.5">
                                    {i + 1}
                                  </span>
                                  {step}
                                </li>
                              ))}
                            </ol>
                          </div>
                        </div>

                        <div className="flex gap-3 text-[10px] font-mono text-slate-500">
                          <span className="px-2 py-1 bg-slate-800 rounded border border-slate-700">{layer.ptDevice}</span>
                          <span className="px-2 py-1 bg-slate-800 rounded border border-slate-700">{layer.pythonModule}</span>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            ))}
          </div>
        </section>

        {/* ─── TOPOLOGY ZONES ─── */}
        <section>
          <SectionHeader icon={<Activity className="w-5 h-5 text-purple-400" />} title="Network Topology & IP Plan" />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {ZONES.map(zone => (
              <div
                key={zone.name}
                className="p-5 rounded-2xl bg-slate-900/50 border border-slate-800/50 hover:border-slate-700/50 transition-colors"
              >
                <div className="flex items-center gap-3 mb-3">
                  <span className="w-3 h-3 rounded-full" style={{ backgroundColor: zone.color }} />
                  <h3 className="text-sm font-bold text-white">{zone.name}</h3>
                </div>
                <p className="text-xs text-slate-400 mb-4">{zone.role}</p>
                <div className="flex flex-wrap gap-2">
                  {zone.nodes.map(node => (
                    <span key={node} className="text-[10px] font-mono px-2 py-1 bg-slate-800/80 rounded border border-slate-700/50 text-slate-300">
                      {node}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ─── DATA FLOW DIAGRAM ─── */}
        <section>
          <SectionHeader icon={<ArrowRight className="w-5 h-5 text-emerald-400" />} title="End-to-End Data Flow" />
          <div className="bg-slate-900/50 border border-slate-800/50 rounded-2xl p-6">
            <div className="flex flex-col md:flex-row items-stretch gap-2">
              {[
                { label: "Spin Superposition", sub: "L1: microtubule.py", color: "#3b82f6" },
                { label: "QSP Handshake", sub: "L5: qsp_protocol.py", color: "#ec4899" },
                { label: "Mycelial Routing", sub: "L2/L3: routing.py", color: "#8b5cf6" },
                { label: "SpinToBit Bridge", sub: "L4: spin_bridge.py", color: "#f59e0b" },
                { label: "HITL PPP Filter", sub: "L4: hitl_gateway.py", color: "#10b981" },
                { label: "Classical Data", sub: "Output: UTF-8 bytes", color: "#06b6d4" },
              ].map((step, i, arr) => (
                <React.Fragment key={i}>
                  <div className="flex-1 p-4 rounded-xl border border-slate-700/30 text-center bg-slate-800/20 hover:bg-slate-800/40 transition-colors">
                    <div className="w-8 h-8 mx-auto rounded-lg flex items-center justify-center mb-2 text-xs font-bold" style={{ backgroundColor: `${step.color}20`, color: step.color }}>
                      {i + 1}
                    </div>
                    <p className="text-xs font-bold text-slate-200">{step.label}</p>
                    <p className="text-[10px] font-mono text-slate-500 mt-1">{step.sub}</p>
                  </div>
                  {i < arr.length - 1 && (
                    <div className="flex items-center justify-center text-slate-600 md:rotate-0 rotate-90 py-2 md:py-0">
                      <ArrowRight className="w-4 h-4" />
                    </div>
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        </section>

        {/* ─── KEY CONCEPTS ─── */}
        <section>
          <SectionHeader icon={<Database className="w-5 h-5 text-cyan-400" />} title="Key Concepts" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <ConceptCard
              title="Orch OR (Objective Reduction)"
              color="#3b82f6"
              body="Penrose-Hameroff theory: quantum states in microtubules collapse by gravitational self-energy, producing conscious moments — here repurposed as routing primitives."
            />
            <ConceptCard
              title="BLAP (Bio-Layered Address Protocol)"
              color="#8b5cf6"
              body="64-bit addresses assigned to each node in the mycelial mesh, replacing MAC addresses with biologically-inspired identifiers for self-organizing topologies."
            />
            <ConceptCard
              title="QSP (Quantum Sync Protocol)"
              color="#ec4899"
              body="Three-phase handshake: RESONATE → PHASE-SYNC → ENTANGLE. Establishes entanglement pairs for zero-latency data transfer across the bio-quantum network."
            />
            <ConceptCard
              title="Entanglement Swapping"
              color="#10b981"
              body="Extends quantum channels: if A↔B and B↔C are entangled, a Bell measurement at B creates a direct A↔C link — enabling long-range non-local communication."
            />
            <ConceptCard
              title="Decoherence Storm"
              color="#ef4444"
              body="Environmental noise causes rapid quantum state collapse, severing mycelial links. The mesh self-heals by regrowing links at higher resonance cost."
            />
            <ConceptCard
              title="PPP (Penrose Privacy Protocol)"
              color="#f59e0b"
              body="HITL ethical filter: packets are scored by entropy delta (ΔS). Positive entropy → approved. Negative entropy (causality violation) → dropped."
            />
          </div>
        </section>

        {/* ─── 4-WEEK SPRINT ─── */}
        <section>
          <SectionHeader icon={<ShieldCheck className="w-5 h-5 text-amber-400" />} title="4-Week Development Sprint" />
          <div className="relative pl-6 border-l-2 border-slate-800 space-y-6">
            {SPRINT.map((s, i) => (
              <div key={s.week} className="relative">
                <div className="absolute -left-[31px] w-5 h-5 rounded-full bg-slate-900 border-2 border-blue-500 flex items-center justify-center">
                  <span className="text-[9px] font-bold text-blue-400">{s.week}</span>
                </div>
                <div className="bg-slate-900/40 border border-slate-800/50 rounded-xl p-5 ml-2 hover:bg-slate-900/60 transition-colors">
                  <h4 className="text-sm font-bold text-slate-200">Week {s.week}: {s.title}</h4>
                  <p className="text-xs text-slate-400 mt-1">{s.focus}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ─── KEYWORDS ─── */}
        <section className="text-center">
          <div className="flex flex-wrap justify-center gap-2">
            {["BRNA", "Orch-OR", "Microtubules", "QSP", "Mycelial-Mesh", "DNA-Storage", "Entanglement-Swapping", "BLAP", "Bio-Quantum", "Wetware", "HITL", "Resonance-Fidelity", "PPP"].map(kw => (
              <span key={kw} className="text-[10px] font-mono px-3 py-1.5 bg-slate-800/50 border border-slate-700/40 rounded-full text-slate-400 hover:text-blue-400 hover:border-blue-500/30 transition-colors cursor-default">
                {kw}
              </span>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}

/* ──────── Helper Components ──────── */
function SectionHeader({ icon, title }: { icon: React.ReactNode; title: string }) {
  return (
    <div className="flex items-center gap-3 mb-6">
      {icon}
      <h2 className="text-xl font-bold text-white">{title}</h2>
    </div>
  );
}

function ConceptCard({ title, color, body }: { title: string; color: string; body: string }) {
  return (
    <div className="p-5 rounded-2xl bg-slate-900/50 border border-slate-800/50 hover:border-slate-700/50 transition-colors group">
      <div className="flex items-center gap-2 mb-3">
        <span className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />
        <h4 className="text-xs font-bold text-white uppercase tracking-wider">{title}</h4>
      </div>
      <p className="text-xs text-slate-400 leading-relaxed">{body}</p>
    </div>
  );
}
