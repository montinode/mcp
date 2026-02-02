# Network Security Hardening Guide: Preclude Endpoint Spoofing

## Overview

This guide provides comprehensive best practices for preventing endpoint spoofing attacks across all network layers. Endpoint spoofing includes host/IP/MAC/DNS spoofing and switch-level abuse. These security measures help protect your network infrastructure from unauthorized access and man-in-the-middle attacks.

## Table of Contents

1. [Layer 2 Security (Switch-Level)](#1-layer-2-security-switch-level)
2. [Layer 3 Security (Routing/Gateway)](#2-layer-3-security-routinggateway)
3. [Layer 7 Security (DNS/Service Identity)](#3-layer-7-security-dnsservice-identity)
4. [Endpoint Hardening](#4-endpoint-hardening)
5. [Monitoring & Rapid Containment](#5-monitoring--rapid-containment)
6. [Quick Reference Checklist](#quick-reference-checklist)
7. [Vendor-Specific Configurations](#vendor-specific-configurations)

---

## 1. Layer 2 Security (Switch-Level)

Lock down identity at the data link layer to prevent spoofing at the switch level.

### DHCP Snooping

**Purpose**: Trust only uplinks to your DHCP server, preventing rogue DHCP servers from distributing malicious network configurations.

**Configuration Steps**:
- Enable DHCP snooping globally on the switch
- Configure trusted ports (uplinks to legitimate DHCP server)
- All access ports should remain untrusted by default
- Rate limit DHCP packets on untrusted ports

**Benefits**:
- Prevents rogue DHCP servers
- Creates binding database for DAI
- Blocks DHCP starvation attacks

### Dynamic ARP Inspection (DAI)

**Purpose**: Validates ARP packets against DHCP snooping binding table to prevent ARP spoofing.

**Configuration Steps**:
- Enable DAI on VLANs (requires DHCP snooping)
- Configure trusted ports (uplinks, inter-switch links)
- Set validation checks (src-mac, dst-mac, ip)
- Configure rate limiting to prevent DoS

**Benefits**:
- Prevents ARP spoofing/poisoning
- Stops man-in-the-middle attacks
- Validates IP-to-MAC bindings

### IP Source Guard

**Purpose**: Blocks IP/MAC spoofing on a per-port basis using DHCP snooping bindings.

**Configuration Steps**:
- Enable IP Source Guard on access ports
- Use DHCP snooping binding database
- Configure static bindings for non-DHCP devices
- Enable both IP and MAC address filtering

**Benefits**:
- Prevents IP address spoofing
- Blocks MAC address spoofing
- Per-port security enforcement

### Port Security

**Purpose**: Limits MAC addresses per access port and implements sticky MAC learning.

**Configuration Steps**:
- Set maximum MAC addresses per port (typically 1-3)
- Enable sticky MAC learning for stable devices
- Configure violation actions (shutdown, restrict, protect)
- Set aging timers appropriately

**Benefits**:
- Prevents MAC flooding attacks
- Limits unauthorized device connections
- Creates stable MAC-to-port mappings

### Unused Ports Security

**Purpose**: Disable unused ports and isolate them from production networks.

**Configuration Steps**:
- Administratively disable all unused ports
- Assign unused ports to a dedicated "dead" VLAN
- Remove unused ports from trunk allowed VLANs
- Implement auto-disable for long-inactive ports

**Benefits**:
- Reduces attack surface
- Prevents unauthorized physical access
- Simplifies security monitoring

### BPDU Guard & Root Guard

**Purpose**: Prevents rogue switches/bridges from being inserted into the network topology.

**Configuration Steps**:
- Enable BPDU Guard on all access ports (edge ports)
- Enable Root Guard on uplink ports
- Configure PortFast on access ports (with BPDU Guard)
- Disable on trunk ports between switches

**Benefits**:
- Prevents spanning tree manipulation
- Stops rogue switch insertion
- Protects network topology

### Storm Control

**Purpose**: Limits broadcast/multicast/unknown unicast floods to prevent network storms.

**Configuration Steps**:
- Enable storm control on access ports
- Set thresholds for broadcast, multicast, and unicast
- Configure appropriate action (shutdown, trap)
- Monitor and tune thresholds based on network behavior

**Benefits**:
- Prevents broadcast storms
- Limits multicast flooding
- Protects against DoS attacks

---

## 2. Layer 3 Security (Routing/Gateway)

Stop rogue routing and gateway spoofing at the network layer.

### Rogue DHCP Protection

**Purpose**: Block unauthorized DHCP servers from distributing network configurations.

**Implementation**:
- DHCP snooping (covered in Layer 2)
- DHCP guard where available
- Port security to limit devices
- Monitor for multiple DHCP servers

**Benefits**:
- Prevents gateway redirection
- Stops DNS hijacking via DHCP
- Maintains legitimate network configuration

### Gateway ARP Protection

**Purpose**: Prevent ARP spoofing of the default gateway.

**Implementation**:
- Dynamic ARP Inspection (DAI)
- Static ARP entries for critical infrastructure (optional)
- Regular ARP table monitoring
- Alert on ARP conflicts

**Benefits**:
- Protects default gateway identity
- Prevents gateway man-in-the-middle attacks
- Maintains routing integrity

### IPv6 Router Advertisement Guard

**Purpose**: Prevent rogue IPv6 router advertisements.

**Configuration Steps** (if using IPv6):
- Enable RA Guard on access ports
- Configure policy to block RAs on untrusted ports
- Allow RAs only on uplinks to legitimate routers
- Block DHCPv6 server messages on access ports

**Benefits**:
- Prevents IPv6 default route hijacking
- Stops rogue IPv6 DHCP servers
- Maintains IPv6 routing integrity

---

## 3. Layer 7 Security (DNS/Service Identity)

Prevent name and service spoofing at the application layer.

### DNS Security

**Forced DNS Resolution**:
- Use firewall rules to block outbound DNS (ports 53/853/443) except to approved resolvers
- Redirect DNS queries to internal resolvers
- Monitor for DNS tunneling attempts

**DNS over TLS/HTTPS Policy**:
- Deploy managed DoT/DoH endpoints for controlled encrypted DNS
- OR explicitly disable unmanaged DoH in browsers/OS
- Use DNS filtering services with encrypted transport

**DNSSEC Validation**:
- Enable DNSSEC validation on resolvers
- Monitor DNSSEC validation failures
- Use DNSSEC-aware recursive resolvers

**Benefits**:
- Prevents DNS hijacking
- Stops phishing via DNS manipulation
- Ensures DNS integrity and authenticity

### TLS & Service Identity

**Mutual TLS (mTLS)**:
- Implement mTLS for internal service-to-service communication
- Require both client and server certificates
- Use short-lived certificates with automatic rotation

**Certificate Pinning**:
- Implement certificate pinning in applications and agents
- Pin to intermediate CA or leaf certificates
- Maintain backup pins for rotation

**HSTS & Modern TLS**:
- Enforce HTTP Strict Transport Security
- Disable TLS 1.0 and 1.1
- Use strong cipher suites only
- Enable OCSP stapling

**Benefits**:
- Prevents TLS man-in-the-middle attacks
- Ensures service identity
- Protects encrypted communications

---

## 4. Endpoint Hardening

Harden endpoints so spoofing attempts don't succeed.

### Network Access Control

**802.1X Authentication**:
- Deploy 802.1X for wired and wireless networks
- Implement NAC posture checks (device health, compliance)
- Use certificate-based authentication when possible
- Fall back to MAC authentication bypass (MAB) with approval

**Benefits**:
- Strongest control against "plug in anything"
- Per-device authentication and authorization
- Granular access control

### Endpoint Protection

**EDR + Host Firewall**:
- Deploy endpoint detection and response (EDR) solutions
- Enable host-based firewalls on all endpoints
- Block lateral movement ports (SMB/RDP/WinRM) by default
- Allow only necessary communications

**Disable Legacy Protocols**:
- Disable LLMNR (Link-Local Multicast Name Resolution)
- Disable NetBIOS Name Service (NBT-NS)
- Disable mDNS where not needed
- These are common local spoofing vectors

**Credential Protection**:
- Patch regularly and remove local admin privileges
- Enable Windows Credential Guard
- Enable LSA Protection (LSASS)
- Use privileged access workstations (PAWs) for admins

**Benefits**:
- Prevents exploitation of compromised endpoints
- Limits attacker lateral movement
- Protects credentials from theft

---

## 5. Monitoring & Rapid Containment

Detect and respond to spoofing attempts quickly.

### Security Monitoring

**Key Alerts**:
- New MAC address on port
- MAC address flapping between ports
- New DHCP server detected
- ARP anomalies and conflicts
- Duplicate IP address detection
- Multiple authentication failures
- Unexpected VLAN changes

**Logging Infrastructure**:
- NetFlow/sFlow to SIEM
- Switch syslog to centralized logging
- Network Access Control (NAC) logs
- Endpoint security telemetry

### Automated Response

**Containment Actions**:
- Quarantine VLAN for suspicious devices
- Automated port shutdown on high-confidence events
- Dynamic ACLs to restrict access
- Alert security operations center (SOC)

**Incident Response**:
- Documented response procedures
- Escalation paths for security events
- Forensic capabilities (packet capture)
- Regular tabletop exercises

**Benefits**:
- Rapid threat detection
- Automated containment
- Reduced dwell time
- Improved security posture

---

## Quick Reference Checklist

### "PrecludeSWITCH" Baseline for Most Environments

#### Access Ports
- [ ] **802.1X** - Network access control with authentication
- [ ] **Port Security** - Limit MAC addresses per port
- [ ] **BPDU Guard** - Prevent rogue switch insertion
- [ ] **Storm Control** - Limit broadcast/multicast floods

#### Global Configuration
- [ ] **DHCP Snooping** - Trust only uplinks to DHCP server
- [ ] **DAI (Dynamic ARP Inspection)** - Validate ARP packets
- [ ] **IP Source Guard** - Block IP/MAC spoofing per port

#### Uplinks/Trunks
- [ ] Mark as **trusted** for DHCP snooping and DAI
- [ ] Restrict allowed VLANs (principle of least privilege)
- [ ] Lock trunking mode (no DTP negotiation)
- [ ] Enable Root Guard to protect spanning tree

#### Additional Measures
- [ ] Disable unused ports and assign to dead VLAN
- [ ] Implement RA Guard for IPv6 (if applicable)
- [ ] Configure management access restrictions
- [ ] Enable secure protocols (SSH, SNMPv3)

---

## Vendor-Specific Configurations

This section provides configuration examples for common network equipment vendors. Choose your platform for specific commands:

### I can make this exact for your environment

**Tell me:**
1. **Switch vendor/model** (Cisco/Aruba/UniFi/Juniper/etc.)
2. **Do you run IPv6?**
3. **DHCP server location** (on-prem router, Windows DHCP, firewall, cloud)
4. **How users connect** (wired, Wi-Fi, both)

### Cisco IOS/IOS-XE Configuration

**Coming in next update** - Will include specific configuration examples for:
- Catalyst switches (IOS and IOS-XE)
- Nexus switches (NX-OS)
- Small business switches

### Aruba Configuration

**Coming in next update** - Will include specific configuration examples for:
- ArubaOS-Switch
- ArubaOS-CX
- Aruba Central managed switches

### UniFi Configuration

**Coming in next update** - Will include specific configuration examples for:
- UniFi Network Controller
- UniFi switches
- CLI and GUI configuration steps

### Juniper Configuration

**Coming in next update** - Will include specific configuration examples for:
- Junos OS (EX Series)
- QFX Series
- SRX Series firewall integration

### HPE Networking

**Coming in next update** - Will include specific configuration examples for:
- HPE Aruba (formerly ProCurve)
- FlexFabric switches

### Other Vendors

For other vendors not listed above:
- Look for equivalent features in your vendor's documentation
- Map the security control to vendor-specific terminology
- Test in a non-production environment first

---

## Implementation Best Practices

### Planning Phase
1. **Inventory** - Document all network devices, connections, and configurations
2. **Assessment** - Identify gaps in current security posture
3. **Prioritization** - Focus on high-risk areas first
4. **Testing Plan** - Prepare test environment and rollback procedures

### Deployment Phase
1. **Pilot** - Start with a small segment or single switch
2. **Monitor** - Watch for false positives and connectivity issues
3. **Adjust** - Fine-tune thresholds and policies
4. **Scale** - Gradually roll out to entire network

### Maintenance Phase
1. **Regular Audits** - Verify configurations haven't drifted
2. **Update Documentation** - Keep network diagrams and configs current
3. **Review Logs** - Analyze security events and anomalies
4. **Test Responses** - Conduct regular security drills

---

## Troubleshooting Common Issues

### DHCP Clients Not Getting Addresses
- Verify uplink ports are configured as trusted
- Check DHCP rate limits aren't too restrictive
- Ensure DHCP relay/helper addresses are correct
- Verify DHCP server is reachable from clients

### Legitimate Devices Blocked by DAI
- Check DHCP snooping binding table
- Verify static ARP entries for non-DHCP devices
- Review DAI rate limits
- Check trusted port configurations

### Devices Locked Out by Port Security
- Review MAC address limits per port
- Check for devices with multiple MAC addresses (VMs, phones with passthrough)
- Verify sticky MAC configurations
- Consider using dynamic learning instead of sticky

### 802.1X Authentication Failures
- Verify RADIUS server connectivity
- Check certificate validity
- Review supplicant configurations
- Test with MAB as fallback

---

## Additional Resources

### Industry Standards
- [NIST Special Publication 800-97](https://csrc.nist.gov/publications/detail/sp/800-97/final) - Establishing Wireless Robust Security Networks
- [CIS Controls](https://www.cisecurity.org/controls) - Critical Security Controls
- [PCI DSS](https://www.pcisecuritystandards.org/) - Payment Card Industry Data Security Standard

### Vendor Documentation
- Cisco Press - Network Security books
- Aruba Networks - Security Best Practices Guides
- Juniper Networks - Day One security guides

### Community Resources
- Network security forums and communities
- Vendor support forums
- Security mailing lists (e.g., SANS, US-CERT)

---

## Security Considerations

### Defense in Depth
These controls work best when implemented in layers. No single control is perfect, but combined they create a robust security posture.

### Impact Assessment
Some controls (especially 802.1X and strict port security) can impact operations if not properly planned. Always:
- Test thoroughly in non-production
- Have rollback procedures ready
- Communicate changes to stakeholders
- Plan for exceptions and special cases

### Compliance Requirements
Many of these controls align with regulatory requirements:
- **PCI DSS** - Requires network segmentation and access controls
- **HIPAA** - Mandates access controls and encryption
- **SOC 2** - Requires security monitoring and incident response
- **ISO 27001** - Comprehensive information security management

---

## Contributing

This guide is maintained as part of the AWS MCP Servers project. To contribute:
1. Submit issues for clarifications or corrections
2. Propose additional vendor configurations
3. Share real-world implementation experiences
4. Suggest improvements to the guide

---

## License

This documentation is provided under the Apache License 2.0. See the LICENSE file in the repository root for details.

---

## Disclaimer

This guide provides general security recommendations. Always:
- Consult with network security professionals
- Test in non-production environments first
- Consider your specific environment and requirements
- Keep security controls updated as threats evolve
- Review vendor-specific documentation for your equipment

Network security is an ongoing process requiring regular review and updates to maintain effectiveness against evolving threats.
