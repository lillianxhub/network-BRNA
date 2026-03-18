# Packet Tracer Build Guide — Step by Step

## Step 1: Open Packet Tracer and create new project
- File → New
- Save as `brna_topology.pkt`

---

## Step 2: Place devices on canvas

Drag from the device panel at the bottom:

### Routers (use 2811 or 1941)
Place in a diamond layout at the top of the canvas:
```
        [NR-B]
       /       \
   [NR-A]   [NR-C]
       \       /
        [NR-D]
```
Label each router: click the name under it and type NR-A, NR-B, NR-C, NR-D.

### Switches (use 2960)
Place below the router mesh:
- `SW-BIO` — below and left of NR-D
- `SW-HITL` — below and right of NR-D

### PCs
**Bio zone** (below SW-BIO, 3 PCs):
- `NR-E`, `DNA-Store`, `NR-F`

**HITL zone** (below SW-HITL, 3 PCs):
- `HITL-GW`, `Monitor-1`, `Monitor-2`

**Entanglement zone** (bottom row, 4 PCs):
- `QNode-A`, `QNode-B`, `QNode-C`, `QNode-D`

---

## Step 3: Draw links

Use the **Connections** tool (lightning bolt icon).  
Select **Copper Straight-Through** for PC↔Switch.  
Select **Copper Cross-Over** or **Serial** for Router↔Router.

| From | To | Cable type |
|------|----|------------|
| NR-A fa0/0 | NR-B fa0/0 | Copper cross-over |
| NR-B fa0/1 | NR-C fa0/0 | Copper cross-over |
| NR-A fa0/1 | NR-D fa0/0 | Copper cross-over |
| NR-B fa0/2 | NR-D fa0/1 | Copper cross-over |
| NR-C fa0/1 | NR-D fa0/2 | Copper cross-over |
| NR-A fa0/2 | SW-BIO port 1 | Copper straight-through |
| NR-D fa0/3 | SW-BIO port 2 | Copper straight-through |
| NR-C fa0/2 | SW-HITL port 1 | Copper straight-through |
| NR-D fa0/4 | SW-HITL port 2 | Copper straight-through |
| SW-BIO | NR-E | Copper straight-through |
| SW-BIO | DNA-Store | Copper straight-through |
| SW-BIO | NR-F | Copper straight-through |
| SW-HITL | HITL-GW | Copper straight-through |
| SW-HITL | Monitor-1 | Copper straight-through |
| SW-HITL | Monitor-2 | Copper straight-through |
| QNode-A | QNode-B | Copper cross-over (label: Entanglement pair 1) |
| QNode-C | QNode-D | Copper cross-over (label: Entanglement pair 2) |

---

## Step 4: Assign IP addresses

### Routers — click router → CLI tab → paste:

**NR-A:**
```
enable
conf t
hostname NR-A
interface fa0/0
 ip address 10.0.1.1 255.255.255.0
 no shutdown
interface fa0/1
 ip address 10.0.2.254 255.255.255.0
 no shutdown
ip route 10.0.3.0 255.255.255.0 10.0.1.4
ip route 10.0.4.0 255.255.255.0 10.0.1.4
end
```

**NR-B:**
```
enable
conf t
hostname NR-B
interface fa0/0
 ip address 10.0.1.2 255.255.255.0
 no shutdown
end
```

**NR-C:**
```
enable
conf t
hostname NR-C
interface fa0/0
 ip address 10.0.1.3 255.255.255.0
 no shutdown
interface fa0/1
 ip address 10.0.3.254 255.255.255.0
 no shutdown
ip route 10.0.2.0 255.255.255.0 10.0.1.4
ip route 10.0.4.0 255.255.255.0 10.0.1.4
end
```

**NR-D (hub):**
```
enable
conf t
hostname NR-D
interface fa0/0
 ip address 10.0.1.4 255.255.255.0
 no shutdown
ip route 10.0.2.0 255.255.255.0 10.0.2.254
ip route 10.0.3.0 255.255.255.0 10.0.3.254
ip route 10.0.4.0 255.255.255.0 10.0.1.1
end
```

### PCs — click PC → Desktop tab → IP Configuration:

| PC | IP | Subnet | Gateway |
|----|-----|--------|---------|
| NR-E | 10.0.2.1 | 255.255.255.0 | 10.0.2.254 |
| DNA-Store | 10.0.2.2 | 255.255.255.0 | 10.0.2.254 |
| NR-F | 10.0.2.3 | 255.255.255.0 | 10.0.2.254 |
| HITL-GW | 10.0.3.1 | 255.255.255.0 | 10.0.3.254 |
| Monitor-1 | 10.0.3.2 | 255.255.255.0 | 10.0.3.254 |
| Monitor-2 | 10.0.3.3 | 255.255.255.0 | 10.0.3.254 |
| QNode-A | 10.0.4.1 | 255.255.255.0 | 10.0.1.1 |
| QNode-B | 10.0.4.2 | 255.255.255.0 | 10.0.1.1 |
| QNode-C | 10.0.4.3 | 255.255.255.0 | 10.0.1.1 |
| QNode-D | 10.0.4.4 | 255.255.255.0 | 10.0.1.1 |

---

## Step 5: Verify connectivity

Open NR-A CLI and ping each zone:
```
ping 10.0.1.2    ← NR-B (should work)
ping 10.0.2.2    ← DNA-Store (should work)
ping 10.0.3.1    ← HITL-GW (should work)
```

Open NR-E Desktop → Command Prompt:
```
ping 10.0.3.1    ← HITL-GW across zones
ping 10.0.1.4    ← NR-D hub
```

**All pings succeed = topology is correct.**

---

## Step 6: Add visual labels (optional but looks good)

- Right-click each zone boundary → Draw rectangle
- Color the core mesh zone light green
- Color the bio zone light blue  
- Color the HITL zone light purple
- Color the entanglement zone light amber
- Add text labels: "Neural Repeater Core", "Bio Storage Zone", etc.

---

## Step 7: Save and screenshot

- File → Save
- Take a screenshot of the full canvas for your GitHub repo
- Save screenshot as `topology/brna_topology_screenshot.png`
