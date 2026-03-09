# Cisco Switch Security Configuration Guide

## Overview

This guide provides detailed configuration commands for implementing endpoint spoofing prevention on Cisco switches (IOS, IOS-XE, and NX-OS).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Global Configuration](#global-configuration)
3. [Access Port Configuration](#access-port-configuration)
4. [Trunk Port Configuration](#trunk-port-configuration)
5. [DHCP Server/Uplink Configuration](#dhcp-serveruplink-configuration)
6. [IPv6 Configuration (Optional)](#ipv6-configuration-optional)
7. [Complete Configuration Examples](#complete-configuration-examples)
8. [Verification Commands](#verification-commands)

---

## Prerequisites

### Required Information

Before configuring, gather:
- [ ] DHCP server IP address(es)
- [ ] DHCP server port location(s)
- [ ] List of VLANs in use
- [ ] Trunk port locations
- [ ] List of unused ports
- [ ] IPv6 status (enabled/disabled)

### Version Compatibility

These configurations are tested on:
- Cisco IOS 12.2(55)SE and later
- Cisco IOS-XE 16.x and later
- Cisco NX-OS 7.x and later

---

## Global Configuration

### Step 1: Enable DHCP Snooping

```cisco
! Enter global configuration mode
configure terminal

! Enable DHCP snooping globally
ip dhcp snooping

! Enable DHCP snooping on specific VLANs (example: VLANs 10, 20, 30)
ip dhcp snooping vlan 10,20,30

! Optional: Store bindings in persistent storage
! This preserves bindings across reboots
ip dhcp snooping database flash:dhcp-snooping.db
ip dhcp snooping database write-delay 60

! Verify Option-82 insertion (recommended: disable for switch as client)
no ip dhcp snooping information option

! Exit configuration mode
end

! Save configuration
write memory
```

### Step 2: Enable Dynamic ARP Inspection (DAI)

```cisco
configure terminal

! Enable DAI on VLANs where DHCP snooping is enabled
ip arp inspection vlan 10,20,30

! Configure validation checks (recommended: all three)
ip arp inspection validate src-mac dst-mac ip

! Log DAI drops (optional but recommended)
ip arp inspection log-buffer entries 1024
ip arp inspection log-buffer logs 1024 interval 60

end
write memory
```

### Step 3: Configure Dead VLAN for Unused Ports

```cisco
configure terminal

! Create a dedicated VLAN for unused ports
vlan 999
 name DEAD_VLAN
 shutdown
exit

end
write memory
```

---

## Access Port Configuration

Configure these settings on every access port (user-facing ports).

### Standard Access Port Template

```cisco
configure terminal

! Example: Configure interface GigabitEthernet1/0/1
interface GigabitEthernet1/0/1

 ! Set as access port
 switchport mode access
 switchport access vlan 10
 
 ! Enable PortFast for faster connectivity (access ports only)
 spanning-tree portfast
 
 ! Enable BPDU Guard to prevent rogue switches
 spanning-tree bpduguard enable
 
 ! Configure port security
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security aging time 2
 switchport port-security aging type inactivity
 
 ! Enable IP Source Guard
 ip verify source
 
 ! Configure DHCP snooping rate limit
 ip dhcp snooping limit rate 15
 
 ! Configure DAI rate limit
 ip arp inspection limit rate 15
 
 ! Enable storm control
 storm-control broadcast level 10.00
 storm-control multicast level 10.00
 storm-control action shutdown
 
 ! Add description for documentation
 description Access Port - Workstation
 
exit
end
write memory
```

### Voice VLAN Configuration (IP Phones)

```cisco
configure terminal

interface GigabitEthernet1/0/5

 switchport mode access
 switchport access vlan 10
 switchport voice vlan 20
 
 spanning-tree portfast
 spanning-tree bpduguard enable
 
 ! Allow 2 MAC addresses: PC + Phone
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation shutdown
 
 ip verify source
 ip dhcp snooping limit rate 30
 ip arp inspection limit rate 30
 
 storm-control broadcast level 10.00
 storm-control multicast level 10.00
 storm-control action shutdown
 
 description Access Port - IP Phone with PC
 
exit
end
write memory
```

---

## Trunk Port Configuration

Configure these settings on trunk ports connecting switches.

### Trunk Port Template

```cisco
configure terminal

! Example: Configure trunk to another switch
interface GigabitEthernet1/0/48

 ! Configure as static trunk (no DTP negotiation)
 switchport mode trunk
 switchport nonegotiate
 
 ! Allow only necessary VLANs (security best practice)
 switchport trunk allowed vlan 10,20,30
 
 ! Set native VLAN to unused VLAN (not VLAN 1)
 switchport trunk native vlan 999
 
 ! Enable Root Guard to prevent topology changes
 spanning-tree guard root
 
 ! Mark as trusted for DHCP snooping
 ip dhcp snooping trust
 
 ! Mark as trusted for DAI
 ip arp inspection trust
 
 ! No rate limit on DAI for trunk ports
 no ip arp inspection limit
 
 ! Higher storm control thresholds for trunks
 storm-control broadcast level 50.00
 storm-control multicast level 50.00
 
 ! Disable port security on trunks
 no switchport port-security
 
 description Trunk to Distribution Switch
 
exit
end
write memory
```

---

## DHCP Server/Uplink Configuration

Configure uplink ports to DHCP servers or routers.

### Uplink to DHCP Server

```cisco
configure terminal

interface GigabitEthernet1/0/46

 switchport mode access
 switchport access vlan 10
 
 ! Trust this port for DHCP snooping
 ip dhcp snooping trust
 
 ! Trust this port for DAI
 ip arp inspection trust
 
 ! No rate limit on DHCP snooping for uplinks
 no ip dhcp snooping limit
 
 ! No rate limit on DAI for uplinks
 no ip arp inspection limit
 
 ! Disable port security on uplink
 no switchport port-security
 
 ! Disable BPDU Guard on uplink
 no spanning-tree bpduguard enable
 
 description Uplink to DHCP Server
 
exit
end
write memory
```

---

## IPv6 Configuration (Optional)

If you're running IPv6, add these configurations.

### Global IPv6 Configuration

```cisco
configure terminal

! Enable IPv6 RA Guard globally
ipv6 nd raguard policy ACCESS_PORT_POLICY
 device-role host
exit

! Create policy for uplink/router ports
ipv6 nd raguard policy ROUTER_PORT_POLICY
 device-role router
 trusted-port
exit

end
write memory
```

### Apply RA Guard to Access Ports

```cisco
configure terminal

! Apply to access port range
interface range GigabitEthernet1/0/1-24

 ! Apply RA Guard policy
 ipv6 nd raguard attach-policy ACCESS_PORT_POLICY
 
 ! Block DHCPv6 server messages
 ipv6 dhcp guard attach-policy ACCESS_PORT_POLICY
 
exit
end
write memory
```

---

## Complete Configuration Examples

### Small Office Switch (24 ports)

```cisco
! ===== GLOBAL CONFIGURATION =====
configure terminal

! DHCP Snooping
ip dhcp snooping
ip dhcp snooping vlan 10
no ip dhcp snooping information option
ip dhcp snooping database flash:dhcp-snooping.db

! Dynamic ARP Inspection
ip arp inspection vlan 10
ip arp inspection validate src-mac dst-mac ip

! Dead VLAN
vlan 999
 name DEAD_VLAN
 shutdown
exit

! ===== ACCESS PORTS (1-20) =====
interface range GigabitEthernet1/0/1-20
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 
 ip verify source
 ip dhcp snooping limit rate 15
 ip arp inspection limit rate 15
 
 storm-control broadcast level 10.00
 storm-control multicast level 10.00
 storm-control action shutdown
 
 description Access Port - Workstation
exit

! ===== UNUSED PORTS (21-22) =====
interface range GigabitEthernet1/0/21-22
 shutdown
 switchport access vlan 999
 description UNUSED PORT
exit

! ===== UPLINK TO ROUTER/DHCP SERVER (23) =====
interface GigabitEthernet1/0/23
 switchport mode access
 switchport access vlan 10
 
 ip dhcp snooping trust
 ip arp inspection trust
 no ip dhcp snooping limit
 no ip arp inspection limit
 
 description Uplink to Router (DHCP Server)
exit

! ===== TRUNK TO ANOTHER SWITCH (24) =====
interface GigabitEthernet1/0/24
 switchport mode trunk
 switchport nonegotiate
 switchport trunk allowed vlan 10
 switchport trunk native vlan 999
 
 spanning-tree guard root
 ip dhcp snooping trust
 ip arp inspection trust
 
 description Trunk to Distribution Switch
exit

end
write memory
```

---

## Verification Commands

### Verify DHCP Snooping

```cisco
! Show DHCP snooping status
show ip dhcp snooping

! Show DHCP snooping binding table
show ip dhcp snooping binding

! Show DHCP snooping statistics
show ip dhcp snooping statistics
```

### Verify Dynamic ARP Inspection

```cisco
! Show DAI status
show ip arp inspection

! Show DAI statistics
show ip arp inspection statistics

! Show trusted interfaces
show ip arp inspection interfaces
```

### Verify IP Source Guard

```cisco
! Show IP Source Guard configuration
show ip verify source

! Show IP Source Guard on specific interface
show ip verify source interface GigabitEthernet1/0/1
```

### Verify Port Security

```cisco
! Show port security status
show port-security

! Show port security on specific interface
show port-security interface GigabitEthernet1/0/1
```

---

## Common Issues and Solutions

### Issue: DHCP clients not getting addresses

**Solutions**:
```cisco
! Check if uplink is marked as trusted
show ip dhcp snooping | include Trusted

! Solution: Mark uplink as trusted
configure terminal
interface GigabitEthernet1/0/45
 ip dhcp snooping trust
exit
end
```

### Issue: Port in err-disabled state

**Solutions**:
```cisco
! Check why interface is err-disabled
show interfaces status err-disabled

! Solution: Manually re-enable
configure terminal
interface GigabitEthernet1/0/1
 shutdown
 no shutdown
exit
end
```

---

## Best Practices

1. **Test Before Production**: Always test configurations in a lab or staging environment
2. **Implement Gradually**: Roll out in phases, starting with least critical areas
3. **Document Everything**: Keep detailed records of configurations and changes
4. **Monitor Closely**: Watch logs and alerts during initial deployment
5. **Plan Rollback**: Have a rollback plan ready before making changes

---

## License

This configuration guide is provided under the Apache License 2.0.
