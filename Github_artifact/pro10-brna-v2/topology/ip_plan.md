# BRNA Topology — IP Addressing Plan

## Subnets

| Subnet | Zone | Purpose |
|--------|------|---------|
| 10.0.1.0/24 | Core mesh | Router-to-router (NR-A to NR-D) |
| 10.0.2.0/24 | Bio storage | SW-BIO zone (NR-E, NR-F, DNA-Store) |
| 10.0.3.0/24 | HITL control | SW-HITL zone (HITL-GW, Monitors) |
| 10.0.4.0/24 | Entanglement | QNode pairs |

## Node IP Table

| Node | Device | IP | Gateway | Role |
|------|--------|----|---------|------|
| NR-A | Router | 10.0.1.1/24 | — | Neural repeater |
| NR-B | Router | 10.0.1.2/24 | — | Neural repeater |
| NR-C | Router | 10.0.1.3/24 | — | Neural repeater |
| NR-D | Router | 10.0.1.4/24 | — | Hub / central resonance |
| NR-E | PC | 10.0.2.1/24 | 10.0.1.4 | Neural repeater |
| DNA-Store | PC | 10.0.2.2/24 | 10.0.1.4 | DNA data lake |
| NR-F | PC | 10.0.2.3/24 | 10.0.1.4 | Neural repeater |
| HITL-GW | PC | 10.0.3.1/24 | 10.0.1.4 | Human override |
| Monitor-1 | PC | 10.0.3.2/24 | 10.0.3.1 | Fidelity observer |
| Monitor-2 | PC | 10.0.3.3/24 | 10.0.3.1 | Ethics audit |
| QNode-A | PC | 10.0.4.1/24 | — | Entanglement pair 1a |
| QNode-B | PC | 10.0.4.2/24 | — | Entanglement pair 1b |
| QNode-C | PC | 10.0.4.3/24 | — | Entanglement pair 2a |
| QNode-D | PC | 10.0.4.4/24 | — | Entanglement pair 2b |

## Packet Tracer Router Config (paste into CLI)

### NR-A
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

### NR-B
```
enable
conf t
hostname NR-B
interface fa0/0
 ip address 10.0.1.2 255.255.255.0
 no shutdown
end
```

### NR-C
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

### NR-D (hub)
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
