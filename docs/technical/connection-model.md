# Connection model and boundaries

[简体中文](connection-model.zh-CN.md) the general VPN model. It is not a specification of Pangolin VPN’s internal implementation.

## General model

In a typical VPN connection, a client sends routed traffic through an encrypted tunnel to a VPN server. The server forwards that traffic toward its destination. Which traffic enters the tunnel depends on the application and operating system configuration.

## Protection boundaries

Tunnel encryption protects the client-to-server segment. End-to-end application encryption such as HTTPS remains relevant beyond the VPN server. A VPN alone does not establish complete anonymity.

## Implementation details pending verification

- Tunnel protocols and cryptographic configuration.
- DNS handling, IPv6 behavior and routing policy.
- Behavior during disconnection and network changes.
- Platform specific permissions and limitations.

No claims about these behaviors should be inferred from the generic model above. Data collection and retention must be described by verified official policies.
