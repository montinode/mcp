# UniFi Network Security Configuration Guide

## Overview

This guide provides configuration steps for implementing endpoint spoofing prevention on Ubiquiti UniFi switches using the UniFi Network Controller (UI and CLI where applicable).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Controller Global Settings](#controller-global-settings)
3. [Switch Profile Configuration](#switch-profile-configuration)
4. [Port Profile Configuration](#port-profile-configuration)
5. [Verification](#verification)
6. [Limitations](#limitations)

---

## Prerequisites

### Required Information

Before configuring, gather:
- [ ] UniFi Controller version (7.x or later recommended)
- [ ] UniFi switch models and firmware versions
- [ ] DHCP server IP address and location
- [ ] List of VLANs in use
- [ ] IPv6 status (enabled/disabled)

### Supported Devices

These configurations work on:
- UniFi Switch (USW) models
- UniFi Switch Pro models
- UniFi Switch Enterprise models
- UniFi Aggregation Switch models

**Note**: UniFi switches run a custom Linux-based OS with limited CLI access. Most configuration is done through the UniFi Network Controller UI.

---

## Controller Global Settings

### Access UniFi Network Controller

1. Log in to UniFi Network Controller
2. Navigate to **Settings** → **Networks**
3. Configure your VLANs if not already done

### Configure Network Settings

```
Settings → Networks → [Your Network]

General:
- VLAN ID: 10 (example)
- DHCP Mode: DHCP Server (or DHCP Relay if using external server)
- DHCP Range: Configure appropriate range

Advanced:
- Enable DHCP Guarding: ON (if available)
- Enable IGMP Snooping: ON
```

---

## Switch Profile Configuration

### Create Security-Focused Switch Profile

1. Navigate to **Settings** → **Profiles** → **Switch Ports**
2. Click **Create New Port Profile**

### Access Port Profile (Standard Workstation)

```
Profile Name: Secure-Access-Port

General Settings:
- Native VLAN: 10
- Switch Port Profile: All

Advanced Settings:
- Port Isolation: Enable (if needed for guest networks)
- Storm Control: Enable
  - Broadcast: 10% or 1000 pps
  - Multicast: 10% or 1000 pps
  - Unknown Unicast: 10% or 1000 pps
- PoE: Auto (if device needs power)

802.1X Control:
- 802.1X Control: Force Authorized (or use 802.1X if configured)
```

### Voice Port Profile (IP Phones)

```
Profile Name: Secure-Voice-Port

General Settings:
- Native VLAN: 10 (data)
- Tagged VLANs: 20 (voice)

Advanced Settings:
- Port Isolation: Disabled
- Storm Control: Enable
  - Broadcast: 20% or 2000 pps
  - Multicast: 20% or 2000 pps
- PoE: Auto (for IP phones)

802.1X Control:
- 802.1X Control: Force Authorized (or use 802.1X)
```

### Trunk Port Profile (Switch Uplinks)

```
Profile Name: Secure-Trunk-Port

General Settings:
- Native VLAN: 999 (unused)
- Tagged VLANs: 10,20,30 (only required VLANs)
- Switch Port Profile: All

Advanced Settings:
- Storm Control: Enable
  - Broadcast: 50%
  - Multicast: 50%
- PoE: Disabled (typically for uplinks)
```

---

## Port Profile Configuration

### Apply Port Profiles to Physical Ports

1. Navigate to **UniFi Devices**
2. Click on your switch
3. Go to **Ports** tab
4. For each port:

#### Access Port (Ports 1-20)
```
Port: 1-20
Profile Override: Secure-Access-Port
```

#### Voice Port (Ports 21-40)
```
Port: 21-40
Profile Override: Secure-Voice-Port
```

#### Uplink Port (Port 48)
```
Port: 48
Profile Override: Secure-Trunk-Port
```

#### Unused Ports
```
Port: 41-47
Profile Override: Disabled
Or create a "Dead-VLAN" profile with VLAN 999 and port disabled
```

---

## UniFi CLI Configuration (Advanced)

For advanced users with SSH access to UniFi switches:

### Enable SSH Access

1. Settings → System → Advanced
2. Enable "SSH Authentication"
3. Set a secure password

### Connect via SSH

```bash
ssh ubnt@<switch-ip>
# Default password: ubnt (change immediately!)
```

### DHCP Snooping (Limited Support)

**Note**: DHCP Snooping is not fully supported on all UniFi switches through CLI. Use Controller settings where possible.

```bash
# Enter configuration mode
enable
configure

# Show current configuration
show running-config

# Basic port configuration
interface 0/1
 description Access Port - Workstation
 switchport mode access
 switchport access vlan 10
 storm-control broadcast level 10
 storm-control multicast level 10
 exit
```

---

## 802.1X Configuration

UniFi supports 802.1X for network access control.

### Prerequisites

- RADIUS server configured (Windows NPS, FreeRADIUS, etc.)
- User certificates or credentials configured

### Configure RADIUS Profile

1. Navigate to **Settings** → **Profiles** → **RADIUS**
2. Click **Create New RADIUS Profile**

```
Profile Name: NAC-RADIUS

RADIUS Server:
- IP Address: <your-radius-server-ip>
- Port: 1812
- Shared Secret: <your-shared-secret>

Accounting:
- Accounting Port: 1813
- Enable Accounting: ON
```

### Enable 802.1X on Network

1. Navigate to **Settings** → **Networks** → [Your Network]
2. Advanced Settings:

```
RADIUS:
- RADIUS Profile: NAC-RADIUS

802.1X Control:
- Enable: ON
```

### Apply 802.1X to Ports

1. Go to **UniFi Devices** → [Your Switch] → **Ports**
2. For each access port:

```
Port Settings:
- 802.1X Control: MAC-Based (or Single Host)
- RADIUS Profile: NAC-RADIUS
```

---

## Verification

### Via UniFi Controller UI

1. **UniFi Devices** → [Switch] → **Insights**
   - View port statistics
   - Check for storm control events
   - Monitor PoE consumption

2. **UniFi Devices** → [Switch] → **Ports**
   - Verify port profiles are applied
   - Check port status (enabled/disabled)
   - Review connected client information

3. **Insights** → **Client Devices**
   - View all connected clients
   - Check IP address assignments
   - Verify VLAN assignments

### Via CLI (if SSH enabled)

```bash
# Show interface status
show interfaces status

# Show VLAN configuration
show vlan

# Show MAC address table
show mac address-table

# Show storm control
show storm-control
```

---

## Limitations

### UniFi Switch Limitations

UniFi switches have some limitations compared to enterprise switches:

1. **No DHCP Snooping**: Limited or no DHCP snooping capability on most models
2. **No DAI**: Dynamic ARP Inspection not available
3. **No IP Source Guard**: Not available on UniFi switches
4. **Limited Port Security**: Basic MAC limiting only
5. **No BPDU Guard**: Not available through UI (may be available via CLI on some models)

### Workarounds

To compensate for these limitations:

1. **Use 802.1X**: Provides strong per-port authentication
2. **Use VLANs**: Segment network traffic
3. **Enable Storm Control**: Prevents network storms
4. **Firewall Rules**: Use USG/UDM firewall for additional protection
5. **Monitor Traffic**: Use UniFi's built-in traffic analytics
6. **Physical Security**: Secure physical access to switches

---

## Enhanced Security with UniFi Gateway

If using UniFi Security Gateway (USG) or UniFi Dream Machine (UDM):

### Enable IDS/IPS

1. Navigate to **Settings** → **Security** → **Threat Management**
2. Enable:
   - **IDS/IPS**: ON
   - **Categories**: Select appropriate categories (all recommended)

### Enable Advanced Firewall Rules

1. Navigate to **Settings** → **Security** → **Firewall**
2. Create LAN rules:

```
Rule Name: Block-Lateral-SMB
Action: Drop
Protocol: TCP/UDP
Destination: LAN
Port: 445, 135-139
Description: Block lateral SMB movement
```

```
Rule Name: Block-Lateral-RDP
Action: Drop
Protocol: TCP
Destination: LAN
Port: 3389
Description: Block lateral RDP movement
```

### Enable DPI (Deep Packet Inspection)

1. Navigate to **Settings** → **Internet** → **DPI**
2. Enable DPI for traffic visibility

---

## Best Practices for UniFi Environments

1. **Keep Firmware Updated**: Regularly update controller and switch firmware
2. **Use 802.1X**: Provides the strongest access control for UniFi
3. **Segment with VLANs**: Create separate VLANs for different security zones
4. **Enable Storm Control**: On all access ports
5. **Disable Unused Ports**: Explicitly disable ports not in use
6. **Use Strong Passwords**: For controller, devices, and SSO
7. **Enable Two-Factor Authentication**: On UniFi Cloud accounts
8. **Regular Monitoring**: Review logs and traffic analytics regularly

---

## Troubleshooting

### Clients Not Getting DHCP Addresses

1. Check DHCP server configuration in Controller
2. Verify VLAN assignments on ports
3. Check if DHCP Guarding is blocking requests
4. Review firewall rules if using USG/UDM

### Port Shows as Disabled

1. Check if storm control triggered port shutdown
2. Review port profile settings
3. Verify PoE budget if using powered devices
4. Check for cable issues

### 802.1X Authentication Failures

1. Verify RADIUS server connectivity
2. Check shared secret matches
3. Review RADIUS server logs
4. Test with bypass mode first

---

## Complete Configuration Example

### Small Office (24-port switch)

```
Device: UniFi Switch 24 PoE

Global Settings:
- Enable Storm Control globally

Port Profiles:
1. Secure-Access-Port (Ports 1-16)
   - VLAN: 10
   - Storm Control: 10%
   - 802.1X: Enabled (if configured)

2. Secure-Voice-Port (Ports 17-22)
   - Native VLAN: 10
   - Tagged VLAN: 20
   - Storm Control: 20%

3. Secure-Trunk-Port (Port 23)
   - Native VLAN: 999
   - Tagged VLANs: 10,20
   - Storm Control: 50%

4. Uplink (Port 24)
   - Trunk to router/firewall
   - All VLANs allowed

Unused Ports: None (all in use)

Additional Security:
- Enable 802.1X on all access ports
- IDS/IPS enabled on USG/UDM
- VLANs properly segmented
- Firewall rules configured
```

---

## Additional Resources

- [UniFi Support Center](https://help.ui.com/)
- [UniFi Community Forums](https://community.ui.com/)
- [UniFi Enterprise System](https://unifi-network.ui.com/)

---

## Notes

- UniFi equipment is best suited for small to medium businesses
- For large enterprises requiring advanced security features, consider enterprise-grade switches
- Always test configurations in a staging environment first
- Keep backups of controller configuration

---

## License

This configuration guide is provided under the Apache License 2.0.
