# BRNA Topology Diagram — Packet Tracer Layout

## Canvas Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  CORE MESH (10.0.1.0/24)                                        │
│                                                                 │
│  [NR-A]────────[NR-B]────────[NR-C]                            │
│    │  \          │          /  │                                │
│    │   \─────[NR-D]─────/   │                                  │
│    │        (hub)            │                                  │
└────┼─────────────────────────┼────────────────────────────────-─┘
     │                         │
┌────▼──────────────┐   ┌──────▼──────────────┐
│  BIO ZONE         │   │  HITL ZONE          │
│  (10.0.2.0/24)   │   │  (10.0.3.0/24)      │
│                   │   │                     │
│  [SW-BIO]         │   │  [SW-HITL]          │
│  /    |    \      │   │  /    |    \        │
│NR-E DNA-Store NR-F│   │HITL-GW Mon-1 Mon-2  │
└───────────────────┘   └─────────────────────┘

┌─────────────────────────────────────────────┐
│  ENTANGLEMENT ZONE (10.0.4.0/24)            │
│                                             │
│  [QNode-A] ~~~~ [QNode-B]                  │
│  [QNode-C] ~~~~ [QNode-D]                  │
│                                             │
│  ~~~~ = quantum/dashed link in PT           │
└─────────────────────────────────────────────┘
```

## Link Types in Packet Tracer

| Link type | PT cable | Represents |
|-----------|----------|------------|
| Solid line | Copper straight-through | Mycelial fiber (L2) |
| Router-router | Serial DCE/DTE or copper cross | Core mesh backbone |
| Dashed (label it) | Copper + note | Entanglement pair (L3) |
| To switch | Copper straight-through | BLAP fabric connection |
