# Network Security Configuration Templates

This directory contains vendor-specific configuration templates for implementing network security hardening measures to prevent endpoint spoofing.

## Available Configurations

### Cisco
- **[Cisco Switch Security Configuration](cisco-switch-security-config.md)** - Complete configuration guide for Cisco IOS, IOS-XE, and NX-OS switches

### UniFi
- **[UniFi Security Configuration](unifi-security-config.md)** - Complete configuration guide for UniFi Network Controller

## Other Vendors (Coming Soon)
- **Aruba** - ArubaOS-Switch and ArubaOS-CX configurations
- **Juniper** - Junos OS configurations for EX Series switches
- **HPE** - HPE Aruba (ProCurve) configurations

## Overview

Each configuration guide provides:
- Step-by-step configuration commands
- Complete working examples
- Verification commands
- Troubleshooting tips
- Best practices

## Security Features Covered

All guides implement the following security controls:
- **DHCP Snooping** - Prevents rogue DHCP servers
- **Dynamic ARP Inspection (DAI)** - Prevents ARP spoofing
- **IP Source Guard** - Blocks IP/MAC spoofing per port
- **Port Security** - Limits MAC addresses per port
- **BPDU Guard** - Prevents rogue switch insertion
- **Root Guard** - Protects spanning tree topology
- **Storm Control** - Limits broadcast/multicast floods
- **IPv6 RA Guard** - Prevents IPv6 router advertisement attacks (when applicable)

## How to Use

1. Choose the configuration guide for your switch vendor
2. Review the prerequisites section
3. Gather required information (DHCP server location, VLANs, etc.)
4. Test configurations in a non-production environment
5. Implement gradually, monitoring closely
6. Use verification commands to confirm proper operation

## Getting Vendor-Specific Help

The main security hardening guide includes a section where you can request customized configurations:

**Tell us:**
1. Switch vendor/model (Cisco/Aruba/UniFi/Juniper/etc.)
2. Do you run IPv6?
3. DHCP server location (on-prem router, Windows DHCP, firewall, cloud)
4. How users connect (wired, Wi-Fi, both)

We can provide precise configuration steps/commands for your specific platform.

## Contributing

To contribute additional vendor configurations:
1. Follow the template structure used in existing guides
2. Include verification commands and troubleshooting sections
3. Provide complete working examples
4. Test configurations on actual hardware/software versions
5. Submit a pull request with your additions

## Related Documentation

- [Network Security Hardening Guide](../NETWORK_SECURITY_HARDENING.md) - Comprehensive overview of all security measures
- [AWS Network MCP Server](../../src/aws-network-mcp-server/README.md) - Network troubleshooting and analysis tools

## License

All configuration templates are provided under the Apache License 2.0.
