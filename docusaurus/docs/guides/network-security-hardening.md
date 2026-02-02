# Network Security Hardening Guide

A comprehensive guide for preventing endpoint spoofing across all network layers.

## Overview

This documentation provides best practices and configuration templates for implementing network security hardening measures to prevent endpoint spoofing attacks, including host/IP/MAC/DNS spoofing and switch-level abuse.

## Documentation Structure

### Main Guide
- **[Network Security Hardening Guide](https://github.com/awslabs/mcp/blob/main/docs/NETWORK_SECURITY_HARDENING.md)** - Complete overview of security measures across all layers

### Vendor-Specific Configuration Guides

#### Available Now
- **[Cisco Switch Security Configuration](https://github.com/awslabs/mcp/blob/main/docs/network-security-configs/cisco-switch-security-config.md)** - Detailed Cisco IOS/IOS-XE configuration examples
- **[UniFi Security Configuration](https://github.com/awslabs/mcp/blob/main/docs/network-security-configs/unifi-security-config.md)** - UniFi Network Controller security setup

#### Coming Soon
- Aruba ArubaOS-Switch and ArubaOS-CX
- Juniper Junos OS (EX Series)
- HPE Aruba (ProCurve)

## Security Layers Covered

### Layer 2 (Switch-Level)
- DHCP Snooping - Prevents rogue DHCP servers
- Dynamic ARP Inspection (DAI) - Prevents ARP spoofing
- IP Source Guard - Blocks IP/MAC spoofing per port
- Port Security - Limits MAC addresses per port
- BPDU Guard - Prevents rogue switch insertion
- Root Guard - Protects spanning tree topology
- Storm Control - Limits broadcast/multicast floods

### Layer 3 (Routing/Gateway)
- Rogue DHCP protection
- Gateway ARP protection
- IPv6 Router Advertisement Guard

### Layer 7 (DNS/Service Identity)
- DNS security (forced resolution, DoT/DoH policy, DNSSEC)
- TLS & service identity (mTLS, certificate pinning, HSTS)

### Endpoint Hardening
- 802.1X authentication with NAC
- EDR and host firewall configuration
- Legacy protocol disablement
- Credential protection

### Monitoring & Containment
- Security event alerting
- Automated response mechanisms
- Incident response procedures

## Quick Reference Checklist

### "PrecludeSWITCH" Baseline

**Access Ports:**
- ✓ 802.1X authentication
- ✓ Port Security
- ✓ BPDU Guard
- ✓ Storm Control

**Global Configuration:**
- ✓ DHCP Snooping
- ✓ Dynamic ARP Inspection (DAI)
- ✓ IP Source Guard

**Uplinks/Trunks:**
- ✓ Trusted for DHCP snooping and DAI
- ✓ Restricted VLAN access
- ✓ Locked trunking mode (no DTP)
- ✓ Root Guard enabled

## Getting Custom Configuration

Need specific configuration for your environment? Provide:

1. **Switch vendor/model** (Cisco/Aruba/UniFi/Juniper/etc.)
2. **IPv6 status** (yes/no)
3. **DHCP server location** (on-prem router, Windows DHCP, firewall, cloud)
4. **Connection types** (wired, Wi-Fi, both)

We can provide precise configuration steps for your platform.

## Integration with AWS Network MCP Server

This security documentation complements the [AWS Network MCP Server](./aws-network-mcp-server.md), which provides tools for:
- Network troubleshooting
- Flow log analysis
- Security group analysis
- Network path tracing

Together, these resources help you secure and troubleshoot your network infrastructure.

## Additional Resources

- [AWS Well-Architected Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Controls](https://www.cisecurity.org/controls)
- [AWS Network MCP Server Documentation](./aws-network-mcp-server.md)

## Contributing

Contributions are welcome! To add vendor-specific configurations:
1. Follow the template structure in existing guides
2. Include verification commands and troubleshooting sections
3. Provide complete working examples
4. Test on actual hardware/software versions
5. Submit a pull request

## License

This documentation is provided under the Apache License 2.0.
