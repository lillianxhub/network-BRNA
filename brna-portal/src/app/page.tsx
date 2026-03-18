"use client";

import React, { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Activity, 
  Cpu, 
  Database, 
  Dna, 
  Globe, 
  Info, 
  Layers, 
  Lock, 
  ShieldCheck, 
  Zap,
  Play,
  Square,
  AlertTriangle,
  CheckCircle,
  Clock,
  ListRestart
} from "lucide-react";
import TopologyCanvas from "@/components/TopologyCanvas";
import { fetchTestScenarios, fetchStatus as apiFetchStatus, fetchTestStatus as apiFetchTestStatus, startSimulation as apiStartSimulation, runTestScenario as apiRunTestScenario, IS_DEMO } from "@/lib/api";

// --- DATA ---
const INITIAL_NODES = [
  { id: "NR-A", x: 200, y: 120, zone: "core" as const, type: "router", status: "Offline" },
  { id: "NR-B", x: 450, y: 120, zone: "core" as const, type: "router", status: "Offline" },
  { id: "NR-C", x: 700, y: 120, zone: "core" as const, type: "router", status: "Offline" },
  { id: "NR-D", x: 450, y: 220, zone: "core" as const, type: "router", status: "Offline" },
  { id: "SW-BIO", x: 250, y: 350, zone: "bio" as const, type: "switch", status: "Offline" },
  { id: "DNA-Store", x: 250, y: 480, zone: "bio" as const, type: "pc", status: "Offline" },
  { id: "NR-E", x: 120, y: 430, zone: "bio" as const, type: "pc", status: "Offline" },
  { id: "NR-F", x: 380, y: 430, zone: "bio" as const, type: "pc", status: "Offline" },
  { id: "SW-HITL", x: 650, y: 350, zone: "hitl" as const, type: "switch", status: "Offline" },
  { id: "HITL-GW", x: 520, y: 430, zone: "hitl" as const, type: "pc", status: "Offline" },
  { id: "Monitor-1", x: 600, y: 430, zone: "hitl" as const, type: "pc", status: "Offline" },
  { id: "Monitor-2", x: 680, y: 430, zone: "hitl" as const, type: "pc", status: "Offline" },
  { id: "QNode-A", x: 200, y: 700, zone: "entangle" as const, type: "qnode", status: "Offline" },
  { id: "QNode-B", x: 350, y: 700, zone: "entangle" as const, type: "qnode", status: "Offline" },
  { id: "QNode-C", x: 550, y: 700, zone: "entangle" as const, type: "qnode", status: "Offline" },
  { id: "QNode-D", x: 700, y: 700, zone: "entangle" as const, type: "qnode", status: "Offline" },
];

const LINKS = [
  { from: "NR-A", to: "NR-B", type: "serial", label: "Serial" },
  { from: "NR-B", to: "NR-C", type: "serial", label: "Serial" },
  { from: "NR-A", to: "NR-D", type: "eth", label: "Fa0/1" },
  { from: "NR-B", to: "NR-D", type: "eth", label: "Fa1/0" },
  { from: "NR-C", to: "NR-D", type: "eth", label: "Fa1/0" },
  { from: "NR-D", to: "SW-BIO", type: "eth", label: "Fa1/0" },
  { from: "NR-D", to: "SW-HITL", type: "eth", label: "Fa1/1" },
  { from: "SW-BIO", to: "NR-E", type: "eth", label: "Gi0/1" },
  { from: "SW-BIO", to: "DNA-Store", type: "eth", label: "Gi0/2" },
  { from: "SW-BIO", to: "NR-F", type: "eth", label: "Gi0/3" },
  { from: "SW-HITL", to: "HITL-GW", type: "eth", label: "Gi0/1" },
  { from: "SW-HITL", to: "Monitor-1", type: "eth", label: "Gi0/2" },
  { from: "SW-HITL", to: "Monitor-2", type: "eth", label: "Gi0/3" },
  { from: "QNode-A", to: "QNode-B", type: "quantum", label: "QSP pair 1" },
  { from: "QNode-C", to: "QNode-D", type: "quantum", label: "QSP pair 2" },
  { from: "QNode-B", to: "QNode-C", type: "swap", label: "Swap" },
];

interface Node {
  id: string;
  x: number;
  y: number;
  zone: 'core' | 'bio' | 'hitl' | 'entangle';
  type: string;
  status: string;
  coherence?: number;
  atp?: number;
}

const zoneColors = {
  core: { border: '#3b82f6', fill: 'rgba(59, 130, 246, 0.1)', text: '#60a5fa' },
  bio: { border: '#8b5cf6', fill: 'rgba(139, 92, 246, 0.1)', text: '#a78bfa' },
  hitl: { border: '#f59e0b', fill: 'rgba(245, 158, 11, 0.1)', text: '#fbbf24' },
  entangle: { border: '#10b981', fill: 'rgba(16, 185, 129, 0.1)', text: '#34d399' }
};

// const API_BASE = "http://localhost:8000";

// --- APP ---
export default function BRNAPortal() {
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [nodes, setNodes] = useState<Node[]>(INITIAL_NODES);
  const [simRunning, setSimRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentWeek, setCurrentWeek] = useState(0);
  const [weekData, setWeekData] = useState<any>({});
  const [logs, setLogs] = useState<{msg: string, type: string, week?: number}[]>([]);
  
  const [sidebarMode, setSidebarMode] = useState<"info" | "tests">("info");
  const [testScenarios, setTestScenarios] = useState<any>({});
  const [testStatus, setTestStatus] = useState<any>({ status: 'idle' });

  useEffect(() => {
    fetchTestScenarios()
      .then(setTestScenarios)
      .catch(console.error);
  }, []);

  const fetchStatus = useCallback(async () => {
    try {
      const data = await apiFetchStatus();
      
      setSimRunning(data.running);
      setProgress(data.progress);
      setCurrentWeek(data.current_week);
      setWeekData(data.week_data);
      
      // Update logs if new
      if (data.events && data.events.length > logs.length) {
        setLogs(data.events);
      }

      // Update node data
      if (data.nodes) {
        setNodes(prev => prev.map(n => {
          const remoteNode = data.nodes[n.id];
          if (remoteNode) {
            return {
              ...n,
              status: remoteNode.status === 'ONLINE' ? 'Active' : 'Offline',
              coherence: Math.round(remoteNode.fidelity * 100),
              atp: remoteNode.atp
            };
          }
          return n;
        }));
      }
      
      // Test status
      const testData = await apiFetchTestStatus();
      setTestStatus(testData);

    } catch (e) {
      // Silently fail if API is not up yet
    }
  }, [logs.length]);

  useEffect(() => {
    const interval = setInterval(fetchStatus, 1000);
    return () => clearInterval(interval);
  }, [fetchStatus]);

  const startSimulation = async () => {
    try {
      await apiStartSimulation();
      setLogs([{ msg: "Sim Engine Start Initiated...", type: "system" }]);
    } catch (e) {
      console.error("Failed to start simulation", e);
    }
  };

  const runTestScenario = async (id: string) => {
    if (testStatus.running) return;
    try {
      await apiRunTestScenario(id);
      setSidebarMode("tests");
      setSelectedNode(null);
    } catch (e) {
      console.error(e);
    }
  };

  const avgCoherence = nodes.filter(n => n.coherence).reduce((acc, n) => acc + (n.coherence || 0), 0) / (nodes.filter(n => n.coherence).length || 1);

  return (
    <main className="container mx-auto p-6 max-w-7xl min-h-screen flex flex-col gap-6 bg-[#050a14] text-slate-200">
      {/* HEADER */}
      <header className="flex justify-between items-center glass-card p-6 border-b-4 border-blue-500/50 rounded-xl bg-slate-900/50 backdrop-blur-md relative overflow-hidden">
        {IS_DEMO && (
          <div className="absolute top-0 right-0 bg-amber-500/20 text-amber-500 text-[10px] font-bold uppercase tracking-widest px-4 py-1 rounded-bl-lg border-b border-l border-amber-500/50 z-10">
            DEMO MODE (Static)
          </div>
        )}
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-linear-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Globe className="text-white w-6 h-6 animate-pulse" />
          </div>
          <div>
            <motion.h1 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="text-4xl font-bold bg-linear-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent"
            >
              BRNA Command Portal
            </motion.h1>
            <p className="text-slate-400 text-xs mt-1 uppercase tracking-widest font-semibold flex items-center gap-2">
              <Layers className="w-3 h-3 text-blue-400" />
              Bio-Resonance Network Architecture v3.1-SPRINT
            </p>
          </div>
        </div>
        
        <div className="flex gap-6 items-center">
          <div className="flex flex-col items-end">
            <span className="text-[10px] text-slate-500 font-bold uppercase tracking-tighter">Simulation Progress</span>
            <div className="flex items-center gap-3">
              <span className="text-blue-400 font-mono text-xl font-bold">{progress}%</span>
              <div className="w-32 h-2 bg-slate-800 rounded-full overflow-hidden border border-slate-700">
                <motion.div 
                  className="h-full bg-linear-to-r from-blue-500 to-cyan-400"
                  animate={{ width: `${progress}%` }}
                />
              </div>
            </div>
          </div>
          <button 
            onClick={startSimulation}
            disabled={simRunning}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-bold transition-all ${
              simRunning 
                ? "bg-slate-800 text-slate-500 border border-slate-700 cursor-not-allowed" 
                : "bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-600/20 active:scale-95"
            }`}
          >
            {simRunning ? <Clock className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
            {simRunning ? "SIMULATION RUNNING" : "INITIALIZE FULL SYNC"}
          </button>
        </div>
      </header>

      {/* PROGRESS TRACKER */}
      <div className="grid grid-cols-4 gap-4">
        {[1, 2, 3, 4].map(w => (
          <div key={w} className={`glass-card p-4 border-l-4 transition-all rounded-xl bg-slate-900/40 ${
            currentWeek === w ? 'border-blue-500 bg-blue-500/5' : 
            (weekData[w]?.status === 'complete' ? 'border-green-500 opacity-60' : 'border-slate-800 opacity-40')
          }`}>
            <div className="flex justify-between items-center mb-1">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Week {w}</span>
              {weekData[w]?.status === 'complete' && <CheckCircle className="w-3 h-3 text-green-500" />}
              {currentWeek === w && <Activity className="w-3 h-3 text-blue-500 animate-pulse" />}
            </div>
            <h4 className="text-xs font-bold text-slate-300">
              {w === 1 && "Bio-Physical Sync"}
              {w === 2 && "QSP Handshake"}
              {w === 3 && "Mycelial Topology"}
              {w === 4 && "HITL Gateway"}
            </h4>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1">
        {/* TOPOLOGY VIEW */}
        <section className="lg:col-span-8 flex flex-col gap-4">
          <div className="glass-card p-4 relative min-h-[500px] flex-1 rounded-2xl bg-slate-900/30 border border-white/5">
            <TopologyCanvas 
              nodes={nodes as any} 
              links={LINKS as any} 
              onNodeSelect={(node) => {
                setSelectedNode(node as any);
                setSidebarMode("info");
              }} 
              activePath={testStatus?.running && testStatus.active_hop >= 0 && testStatus.data_flow ? 
                 [testStatus.data_flow[testStatus.active_hop], testStatus.data_flow[testStatus.active_hop + 1]] : null}
            />
            
            {/* OVERLAY TELEMETRY */}
            <div className="absolute bottom-6 right-6 flex flex-col gap-2 pointer-events-none">
               <div className="glass-card p-3 border-l-2 border-emerald-500 bg-slate-900/80 backdrop-blur-md rounded-lg">
                  <p className="text-[10px] text-emerald-500 font-bold uppercase tracking-widest">Avg Coherence</p>
                  <p className="text-xl font-mono font-bold text-white">{avgCoherence.toFixed(1)}%</p>
               </div>
               <div className="glass-card p-3 border-l-2 border-purple-500 bg-slate-900/80 backdrop-blur-md rounded-lg">
                  <p className="text-[10px] text-purple-500 font-bold uppercase tracking-widest">Active Links</p>
                  <p className="text-xl font-mono font-bold text-white">{LINKS.length}</p>
               </div>
            </div>
          </div>
          
          {/* LOG PANEL */}
          <div className="glass-card p-4 h-40 flex flex-col gap-2 font-mono text-xs overflow-hidden border-t-2 border-blue-500/30 rounded-xl bg-slate-900/60">
            <div className="flex justify-between items-center mb-1 px-1 border-b border-slate-800 pb-2">
              <span className="text-slate-500 font-bold uppercase tracking-widest flex items-center gap-2">
                <Database className="w-3 h-3" />
                Sub-Quantum Telemetry Log
              </span>
              <span className="text-blue-500/50 flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
                LIVE_STREAM
              </span>
            </div>
            <div className="flex-1 overflow-y-auto space-y-1 pr-2 custom-scrollbar">
              {logs.length === 0 && <span className="text-slate-600 italic">Waiting for simulation data...</span>}
              {[...logs].reverse().map((log, i) => (
                <motion.div 
                  initial={{ opacity: 0, x: -10 }} 
                  animate={{ opacity: 1, x: 0 }} 
                  key={i} 
                  className="flex gap-2"
                >
                  <span className="text-slate-600 shrink-0 w-16">[{log.week ? `W${log.week}` : 'SYS'}]</span>
                  <span className={
                    log.type === 'alert' ? 'text-red-400 font-bold' : 
                    log.type === 'heal' ? 'text-emerald-400' : 
                    log.type === 'sync' ? 'text-purple-400' :
                    'text-blue-300'
                  }>
                    {log.msg}
                  </span>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* SIDEBAR / INFO */}
        <aside className="lg:col-span-4 flex flex-col gap-6">
          <div className="flex gap-2">
            <button 
              onClick={() => { setSidebarMode("info"); setSelectedNode(null); }} 
              className={`flex-1 py-3 flex items-center justify-center gap-2 text-xs font-bold uppercase tracking-widest rounded-xl transition-all border ${sidebarMode === 'info' && !selectedNode ? 'bg-blue-600/20 shadow-[0_0_15px_rgba(37,99,235,0.2)] text-blue-400 border-blue-500/50' : 'bg-slate-900/40 text-slate-500 hover:bg-slate-800 border-transparent hover:border-slate-700'}`}
            >
              <Info className="w-4 h-4" /> Sprint Info
            </button>
            <button 
              onClick={() => { setSidebarMode("tests"); setSelectedNode(null); }} 
              className={`flex-1 py-3 flex items-center justify-center gap-2 text-xs font-bold uppercase tracking-widest rounded-xl transition-all border ${sidebarMode === 'tests' && !selectedNode ? 'bg-purple-600/20 shadow-[0_0_15px_rgba(147,51,234,0.2)] text-purple-400 border-purple-500/50' : 'bg-slate-900/40 text-slate-500 hover:bg-slate-800 border-transparent hover:border-slate-700'}`}
            >
              <ListRestart className="w-4 h-4" /> Test Runner
            </button>
          </div>

          <AnimatePresence mode="wait">
            {selectedNode ? (
              <motion.div 
                key={selectedNode.id}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="glass-card p-6 border-t-4 rounded-2xl bg-slate-900/40 flex-1"
                style={{ borderTopColor: zoneColors[selectedNode.zone].border }}
              >
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-bold uppercase">{selectedNode.type}</span>
                      <span className={`w-2 h-2 rounded-full ${selectedNode.status === 'Active' ? 'bg-green-500 animate-pulse' : 'bg-slate-600'}`}></span>
                    </div>
                    <h3 className="text-3xl font-bold tracking-tight text-white">{selectedNode.id}</h3>
                    <p className="text-slate-400 text-xs uppercase font-bold tracking-widest" style={{ color: zoneColors[selectedNode.zone].text }}>{selectedNode.zone} Zone</p>
                  </div>
                  <button onClick={() => setSelectedNode(null)} className="p-2 hover:bg-slate-800 rounded-full transition-colors text-slate-500">✕</button>
                </div>

                <div className="space-y-4">
                  <div className="p-4 bg-slate-900/50 rounded-xl border border-slate-800">
                    <div className="flex justify-between items-center mb-4">
                      <span className="text-xs font-bold text-slate-500 uppercase">Quantum Fidelity</span>
                      <span className="text-blue-400 font-mono font-bold text-lg">{selectedNode.coherence || 0}%</span>
                    </div>
                    <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                       <motion.div 
                        className="h-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]"
                        animate={{ width: `${selectedNode.coherence || 0}%` }}
                       />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 bg-slate-900/50 rounded-xl border border-slate-800">
                      <p className="text-[10px] text-slate-500 uppercase font-bold mb-1">ATP Level</p>
                      <div className="flex items-baseline gap-1">
                        <span className="text-xl font-bold text-purple-400">{selectedNode.atp?.toFixed(1) || "0.0"}</span>
                        <span className="text-[10px] text-slate-500">%</span>
                      </div>
                    </div>
                    <div className="p-4 bg-slate-900/50 rounded-xl border border-slate-800">
                      <p className="text-[10px] text-slate-500 uppercase font-bold mb-1">System Load</p>
                      <div className="flex items-baseline gap-1">
                        <span className="text-xl font-bold text-amber-400">1.2</span>
                        <span className="text-[10px] text-slate-500">ms</span>
                      </div>
                    </div>
                  </div>
                  
                  <button className="w-full bg-linear-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white py-4 rounded-xl font-bold text-sm shadow-xl shadow-blue-500/10 flex items-center justify-center gap-2 mt-4">
                    <Zap className="w-4 h-4" />
                    RE-SYNCHRONIZE NODE
                  </button>
                </div>
              </motion.div>
            ) : sidebarMode === 'tests' ? (
              <motion.div 
                key="test-runner"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="glass-card flex flex-col gap-4 p-4 border-t-4 border-purple-500 rounded-2xl bg-slate-900/40 flex-1 overflow-hidden"
              >
                 <div className="flex justify-between items-center mb-2 shrink-0">
                   <h3 className="text-xl font-bold text-white">10 Validation Subroutines</h3>
                   {testStatus.running && <span className="flex items-center gap-2 text-xs font-bold text-purple-400 px-2 py-1 bg-purple-500/10 rounded-full border border-purple-500/30"><Activity className="w-3 h-3 animate-pulse" /> RUNNING</span>}
                 </div>
                 
                 {testStatus.running ? (
                    // ACTIVE TEST VIEW
                    <div className="flex flex-col flex-1 overflow-hidden">
                       <div className="p-4 bg-black/40 rounded-xl border border-slate-700 mb-4 shrink-0">
                         <span className="text-xs text-slate-400 font-bold uppercase tracking-widest block mb-1">Active Scenario</span>
                         <span className="text-purple-400 font-bold text-sm">{testStatus.test_name}</span>
                         <div className="flex items-center gap-2 mt-3">
                            <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                               <div className="h-full bg-purple-500 transition-all duration-500" style={{ width: `${(testStatus.current_step / testStatus.total_steps) * 100}%` }}></div>
                            </div>
                            <span className="text-[10px] text-slate-400 font-mono font-bold">STEP {testStatus.current_step}/{testStatus.total_steps}</span>
                         </div>
                       </div>
                       
                       <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
                         {testStatus.step_results?.map((r: any, idx: number) => (
                           <motion.div 
                             initial={{ opacity: 0, y: 10 }}
                             animate={{ opacity: 1, y: 0 }}
                             key={idx} 
                             className="p-3 bg-slate-900/60 rounded-xl border border-slate-700 relative overflow-hidden"
                           >
                             <div className={`absolute top-0 left-0 w-1 h-full ${r.status === 'passed' ? 'bg-green-500' : r.status === 'failed' ? 'bg-red-500' : 'bg-amber-500'}`}></div>
                             <div className="flex justify-between items-start text-xs mb-2 pl-2">
                               <span className="font-bold text-slate-300">[{r.step}] {r.name}</span>
                               {r.status === 'passed' ? <CheckCircle className="w-4 h-4 text-green-500 shrink-0"/> :
                                r.status === 'failed' ? <AlertTriangle className="w-4 h-4 text-red-500 shrink-0"/> :
                                <Activity className="w-4 h-4 text-amber-500 shrink-0"/>}
                             </div>
                             <div className="pl-2 space-y-1">
                               <p className="text-[10px] text-slate-500 font-mono">$&gt; {r.command}</p>
                               <p className={`text-[10px] font-mono mt-1 ${r.status === 'passed' ? 'text-green-400/80' : r.status === 'failed' ? 'text-red-400/80' : 'text-amber-400/80'}`}>=&gt; {r.measured}</p>
                             </div>
                           </motion.div>
                         ))}
                         {testStatus.current_step < testStatus.total_steps && (
                           <div className="p-4 bg-slate-900/20 rounded-xl border border-slate-800 border-dashed text-center text-xs text-slate-500 flex items-center justify-center gap-2">
                             <Clock className="w-4 h-4 animate-spin" /> Executing Operation {testStatus.current_step + 1}...
                           </div>
                         )}
                       </div>
                    </div>
                 ) : (
                    // TEST LIST
                    <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
                      {testStatus.status !== 'idle' && testStatus.step_results?.length > 0 && (
                        <div className={`p-4 rounded-xl mb-4 border ${testStatus.status === 'passed' ? 'bg-green-500/10 border-green-500/30' : testStatus.status === 'failed' ? 'bg-red-500/10 border-red-500/30' : 'bg-amber-500/10 border-amber-500/30'}`}>
                           <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Last Results</p>
                           <p className="text-sm font-bold text-white flex justify-between items-center">
                              {testStatus.test_name}
                              <span className={`text-[10px] px-2 py-0.5 rounded-full border ${testStatus.status === 'passed' ? 'text-green-400 border-green-500/30 bg-green-500/10' : testStatus.status === 'failed' ? 'text-red-400 border-red-500/30 bg-red-500/10' : 'text-amber-400 border-amber-500/30 bg-amber-500/10'}`}>{testStatus.status.toUpperCase()}</span>
                           </p>
                        </div>
                      )}

                      {Object.entries(testScenarios).map(([id, scenario]: [string, any]) => (
                        <div key={id} className="p-4 bg-slate-900/50 rounded-xl hover:bg-slate-800 transition-colors border border-slate-800 group relative">
                          <div className="flex justify-between items-start mb-2">
                             <h4 className="text-sm font-bold text-slate-200 group-hover:text-white transition-colors">{id}. {scenario.name}</h4>
                             <button 
                               onClick={() => runTestScenario(id)}
                               disabled={testStatus.running}
                               className="p-1.5 bg-purple-600/80 hover:bg-purple-500 rounded-lg text-white transition-colors disabled:opacity-50 opacity-0 group-hover:opacity-100 shadow-md shadow-purple-500/20"
                               title="Run Test Case"
                             >
                                <Play className="w-3 h-3 ml-0.5" />
                             </button>
                          </div>
                          <p className="text-xs text-slate-500 leading-relaxed max-w-[90%]">{scenario.description}</p>
                          <div className="flex gap-2 mt-3">
                             <span className="text-[9px] px-2 py-0.5 bg-black/40 rounded text-slate-400 uppercase font-bold tracking-wider" style={{ color: zoneColors[scenario.zone as keyof typeof zoneColors]?.border }}>{scenario.zone} Fabric</span>
                             <span className="text-[9px] px-2 py-0.5 bg-black/40 rounded text-slate-400 uppercase font-bold tracking-wider">{scenario.steps.length} Steps</span>
                          </div>
                        </div>
                      ))}
                    </div>
                 )}
              </motion.div>
            ) : (
              <motion.div 
                key="sprint-info"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="flex flex-col gap-6 flex-1"
              >
                {/* WEEK RESULTS SUMMARY */}
                <div className="glass-card p-6 border-l-4 border-blue-500 rounded-xl bg-slate-900/40">
                  <h3 className="text-sm font-bold text-slate-400 uppercase mb-4 tracking-widest flex items-center gap-2">
                    <Activity className="w-4 h-4 text-blue-400" />
                    Sprint Metrics
                  </h3>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center text-xs">
                       <span className="text-slate-500 font-semibold border-b border-dotted border-slate-700 pb-1">Orch OR Coherence</span>
                       <span className="text-blue-400 font-mono font-bold">PASS (100ms)</span>
                    </div>
                    <div className="flex justify-between items-center text-xs">
                       <span className="text-slate-500 font-semibold border-b border-dotted border-slate-700 pb-1">QSP Sync Delta</span>
                       <span className="text-purple-400 font-mono font-bold">&lt; 0.1 rad</span>
                    </div>
                    <div className="flex justify-between items-center text-xs">
                       <span className="text-slate-500 font-semibold border-b border-dotted border-slate-700 pb-1">Mesh Resiliency</span>
                       <span className="text-emerald-400 font-mono font-bold">100% HEAL</span>
                    </div>
                  </div>
                </div>

                {/* HITL AUDIT */}
                <div className="glass-card p-6 border-l-4 border-amber-500 rounded-xl bg-slate-900/40 flex-1 flex flex-col min-h-[150px]">
                  <h3 className="text-sm font-bold text-slate-400 uppercase mb-4 tracking-widest flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-amber-400" />
                    HITL Audit Log
                  </h3>
                  <div className="flex-1 overflow-y-auto space-y-2 pr-2 custom-scrollbar text-white">
                    {weekData[4]?.hitl?.map((h: string, i: number) => (
                      <div key={i} className="text-[10px] font-mono p-2 bg-slate-900/50 rounded border border-slate-800">
                        {h}
                      </div>
                    )) || <p className="text-[10px] text-slate-600 italic">Waiting for Week 4 interface...</p>}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </aside>
      </div>
    </main>
  );
}
