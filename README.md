# Pangolin VPN

**Secure connections. Simple experience. Your internet, your choice.**

Pangolin VPN is a cross-platform VPN service designed to make encrypted connections, server selection and connection management easy to use.

This is the official public product information and documentation repository maintained by **Yanmei AI LLC**. The proprietary VPN client and server source code are not included.

[Official website](https://pangolin.yanmeiai.com/) · [Documentation index](docs/index.md)

## Product overview

- Encrypted VPN connections to help protect traffic in transit.
- Selection from available VPN server locations.
- Simple connect and disconnect controls.
- Connection status and available usage information.

Feature availability can vary by platform and release. Check current official information before installing. A verified platform, version and download matrix has not yet been added here.

## Documentation

| Topic | Entry |
| --- | --- |
| Product and features | [Overview](docs/product/overview.md) |
| Installation and first connection | [Guide](docs/guides/install.md) |
| Public technical documentation | [Connection model](docs/technical/connection-model.md) |
| FAQ and troubleshooting | [Support guide](docs/support/troubleshooting.md) |
| Repository design and next steps | [Foundation](docs/plans/repository-scope.md) |

GitHub renders the Markdown documentation directly. Consult the official website for hosted product information.

## Repository layout

```text
AGENTS.md                 Maintainer and agent rules
README.md                 Public GitHub entry point
docs/index.md           Documentation index
docs/product/             Product and feature descriptions
docs/guides/              Installation and usage
docs/technical/           Public technical reference
docs/support/             FAQ and troubleshooting
docs/plans/               Public repository design
assets/                   Public documentation assets
scripts/                  Documentation validation
.github/                  Feedback templates and CI
```

## Read and validate locally

From the repository root:

```sh
python3 scripts/check_docs.py
python3 -m http.server 8000
```

Open http://localhost:8000/docs/ . To restart the preview, stop the server with Ctrl+C and run the server command again. No hosting or deployment is configured by this repository.

## Feedback and contribution

Use GitHub issues for sanitized bug reports, feature requests or documentation corrections. Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes. Never post personal information, credentials or raw diagnostic logs.

For private support and security reports, email [admin@yanmeiai.com](mailto:admin@yanmeiai.com). See [SECURITY.md](SECURITY.md).

## Privacy and ownership

Encrypted tunnels help protect traffic in transit; they do not by themselves guarantee complete anonymity. Consult current official service policies for data handling information.

Pangolin VPN is proprietary software. This repository does not grant a license to the application, trademarks or documentation. No open-source license is granted by this initialization.
