"use client";

import React, { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface Node {
  id: string;
  x: number;
  y: number;
  zone: 'core' | 'bio' | 'hitl' | 'entangle';
  type: string;
  coherence?: number;
  status: string;
}

interface Link {
  from: string;
  to: string;
  type: string;
  label: string;
}

const zoneColors = {
  core: { border: '#3b82f6', fill: 'rgba(59, 130, 246, 0.05)', text: '#60a5fa' },
  bio: { border: '#8b5cf6', fill: 'rgba(139, 92, 246, 0.05)', text: '#a78bfa' },
  hitl: { border: '#f59e0b', fill: 'rgba(245, 158, 11, 0.05)', text: '#fbbf24' },
  entangle: { border: '#10b981', fill: 'rgba(16, 185, 129, 0.05)', text: '#34d399' }
};

export default function TopologyCanvas({ 
  nodes, 
  links, 
  onNodeSelect,
  activePath
}: { 
  nodes: Node[], 
  links: Link[], 
  onNodeSelect: (node: Node) => void,
  activePath?: [string, string] | null
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [hoveredNode, setHoveredNode] = useState<Node | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let offset = 0;
    
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      offset += 0.5;
      
      // Draw Zones
      drawZone(ctx, 50, 50, 850, 250, 'core');
      drawZone(ctx, 50, 300, 450, 600, 'bio');
      drawZone(ctx, 470, 300, 850, 600, 'hitl');
      drawZone(ctx, 50, 620, 850, 780, 'entangle');

      // Draw Links
      links.forEach(link => {
        const fromNode = nodes.find(n => n.id === link.from);
        const toNode = nodes.find(n => n.id === link.to);
        if (!fromNode || !toNode) return;

        const isActive = fromNode.status === 'Active' && toNode.status === 'Active';

        ctx.beginPath();
        ctx.moveTo(fromNode.x, fromNode.y);
        ctx.lineTo(toNode.x, toNode.y);
        
        let color = isActive ? 'rgba(51, 65, 85, 0.8)' : 'rgba(51, 65, 85, 0.2)';
        if (link.type === 'quantum') color = isActive ? '#10b981' : 'rgba(16, 185, 129, 0.2)';
        if (link.type === 'swap') color = isActive ? '#6366f1' : 'rgba(99, 102, 241, 0.2)';
        
        ctx.strokeStyle = color;
        ctx.lineWidth = link.type === 'quantum' ? 2 : 1;
        
        if (link.type === 'swap') {
            ctx.setLineDash([5, 5]);
        }
        
        ctx.stroke();
        ctx.setLineDash([]);

        // Animated particles for active links
        if (isActive) {
            const time = Date.now() / 1000;
            const progress = (time % 2) / 2;
            const px = fromNode.x + (toNode.x - fromNode.x) * progress;
            const py = fromNode.y + (toNode.y - fromNode.y) * progress;
            
            ctx.beginPath();
            ctx.arc(px, py, 2, 0, Math.PI * 2);
            ctx.fillStyle = link.type === 'quantum' ? '#34d399' : '#60a5fa';
            ctx.fill();
        }

        // Highlight active test path
        if (activePath && 
            ((fromNode.id === activePath[0] && toNode.id === activePath[1]) || 
             (fromNode.id === activePath[1] && toNode.id === activePath[0]))) {
             
             ctx.beginPath();
             ctx.moveTo(fromNode.x, fromNode.y);
             ctx.lineTo(toNode.x, toNode.y);
             ctx.strokeStyle = '#facc15'; // yellow-400
             ctx.lineWidth = 4;
             ctx.shadowBlur = 15;
             ctx.shadowColor = '#facc15';
             ctx.stroke();
             ctx.shadowBlur = 0;

             // Prominent test packet
             const time = Date.now() / 1500;
             const progress = time - Math.floor(time);
             // Direction depends on array order
             let px, py;
             if (fromNode.id === activePath[0]) {
                 px = fromNode.x + (toNode.x - fromNode.x) * progress;
                 py = fromNode.y + (toNode.y - fromNode.y) * progress;
             } else {
                 px = toNode.x + (fromNode.x - toNode.x) * progress;
                 py = toNode.y + (fromNode.y - toNode.y) * progress;
             }
             
             ctx.beginPath();
             ctx.arc(px, py, 6, 0, Math.PI * 2);
             ctx.fillStyle = '#facc15';
             ctx.shadowBlur = 20;
             ctx.shadowColor = '#facc15';
             ctx.fill();
             
             ctx.beginPath();
             ctx.arc(px, py, 3, 0, Math.PI * 2);
             ctx.fillStyle = '#ffffff';
             ctx.fill();
             ctx.shadowBlur = 0;
        }
      });

      // Draw Nodes
      nodes.forEach(node => {
        const isHovered = hoveredNode?.id === node.id;
        const isActive = node.status === 'Active';
        const isTestNode = activePath && (node.id === activePath[0] || node.id === activePath[1]);
        
        ctx.save();
        
        // Glow effect
        if (isActive || isTestNode) {
            ctx.shadowBlur = isHovered || isTestNode ? 25 : 15;
            ctx.shadowColor = isTestNode ? '#facc15' : zoneColors[node.zone].border;
        }
        
        ctx.fillStyle = isActive ? '#0f172a' : '#1e293b';
        ctx.strokeStyle = isTestNode ? '#facc15' : (isActive ? zoneColors[node.zone].border : 'rgba(255,255,255,0.1)');
        ctx.lineWidth = isHovered || isTestNode ? 3 : 2;
        
        ctx.beginPath();
        if (node.type === 'router') {
          // Diamond for routers
          ctx.moveTo(node.x, node.y - 12);
          ctx.lineTo(node.x + 12, node.y);
          ctx.lineTo(node.x, node.y + 12);
          ctx.lineTo(node.x - 12, node.y);
          ctx.closePath();
        } else if (node.type === 'qnode') {
          // Circle for quantum nodes
          ctx.arc(node.x, node.y, 12, 0, Math.PI * 2);
        } else if (node.type === 'switch') {
          // Square for switches
          ctx.rect(node.x - 10, node.y - 10, 20, 20);
        } else {
          // Rounded rect for others
          ctx.roundRect(node.x - 12, node.y - 9, 24, 18, 4);
        }
        
        ctx.fill();
        ctx.stroke();
        
        // Label
        ctx.shadowBlur = 0;
        ctx.fillStyle = isActive ? '#f8fafc' : '#64748b';
        ctx.font = `bold ${isHovered ? '12px' : '10px'} "Inter", sans-serif`;
        ctx.textAlign = 'center';
        ctx.fillText(node.id, node.x, node.y - (node.type === 'router' ? 18 : 20));
        
        if (isActive && node.coherence) {
            ctx.fillStyle = zoneColors[node.zone].border;
            ctx.font = '8px monospace';
            ctx.fillText(`${node.coherence}%`, node.x, node.y + 22);
        }

        ctx.restore();
      });

      animationFrameId = requestAnimationFrame(draw);
    };

    draw();
    return () => cancelAnimationFrame(animationFrameId);
  }, [nodes, links, hoveredNode]);

  const drawZone = (ctx: CanvasRenderingContext2D, x1: number, y1: number, x2: number, y2: number, zone: keyof typeof zoneColors) => {
    ctx.save();
    ctx.fillStyle = zoneColors[zone].fill;
    ctx.strokeStyle = `rgba(${zone === 'core' ? '59,130,246' : zone === 'bio' ? '139,92,246' : zone === 'hitl' ? '245,158,11' : '16,185,129'}, 0.2)`;
    ctx.lineWidth = 1;
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.roundRect(x1, y1, x2 - x1, y2 - y1, 16);
    ctx.fill();
    ctx.stroke();
    
    // Zone Label
    ctx.setLineDash([]);
    ctx.fillStyle = zoneColors[zone].border;
    ctx.font = 'bold 10px "Inter", sans-serif';
    ctx.globalAlpha = 0.5;
    ctx.fillText(zone.toUpperCase() + ' FABRIC', x1 + 10, y1 + 20);
    ctx.restore();
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    const found = nodes.find(n => Math.sqrt((n.x - x * scaleX)**2 + (n.y - y * scaleY)**2) < 20);
    setHoveredNode(found || null);
    canvas.style.cursor = found ? 'pointer' : 'default';
  };

  return (
    <div className="relative w-full h-full">
      <canvas 
        ref={canvasRef}
        width={900}
        height={800}
        onMouseMove={handleMouseMove}
        onClick={() => hoveredNode && onNodeSelect(hoveredNode)}
        className="w-full h-auto block"
      />
      <div className="absolute top-4 left-4 flex flex-wrap gap-4 p-2 bg-slate-900/40 backdrop-blur-sm rounded-lg border border-white/5">
        {Object.entries(zoneColors).map(([zone, colors]) => (
          <div key={zone} className="flex items-center gap-2 text-[10px] font-bold tracking-widest pointer-events-none">
            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: colors.border }}></span>
            <span className="uppercase" style={{ color: colors.text }}>{zone}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
