# Pangolin VPN

**安全连接，简单体验。自由选择你的互联网。**

Pangolin VPN 是一项跨平台 VPN 服务，致力于让加密连接、服务器选择和连接管理更简单。

本仓库由 **Yanmei AI LLC** 维护，用于发布 Pangolin VPN 官方产品信息和公开文档。仓库不包含专有 VPN 客户端或服务器端源代码。

[官方网站](https://pangolin.yanmeiai.com/) · [中文文档索引](docs/index.zh-CN.md) · [English](README.md)

## 产品概览

- 通过加密 VPN 连接帮助保护传输中的流量。
- 从可用的 VPN 服务器位置中进行选择。
- 简单的连接和断开控制。
- 查看连接状态及可用的用量信息。

功能可用性可能因平台和版本而异。安装前请查看当前官方信息。本仓库尚未提供经过核实的平台、版本和下载列表。

## 文档

| 内容 | 文档 |
| --- | --- |
| 产品与功能 | [产品介绍](docs/product/overview.zh-CN.md) |
| 安装与首次连接 | [安装指南](docs/guides/install.zh-CN.md) |
| 公开技术说明 | [连接模型](docs/technical/connection-model.zh-CN.md) |
| 常见问题与故障排查 | [支持指南](docs/support/troubleshooting.zh-CN.md) |
| 仓库建设计划 | [文档计划](docs/plans/repository-scope.zh-CN.md) |

GitHub 会直接渲染 Markdown 文档。托管的产品信息请查看官方网站。

## 本地阅读与检查

在仓库根目录运行：

```sh
python3 scripts/check_docs.py
python3 -m http.server 8000
```

然后访问 http://localhost:8000/docs/ 。如需重启预览，按 Ctrl+C 停止服务，再次运行启动命令。本仓库未配置网站托管或部署。

## 反馈与贡献

可以通过 GitHub Issue 提交已清理的 Bug 报告、功能建议或文档修正。提交前请阅读 [贡献指南](CONTRIBUTING.md)。请勿发布个人信息、凭证或未经清理的诊断日志。

私密支持和安全问题请联系 [admin@yanmeiai.com](mailto:admin@yanmeiai.com)，详见 [安全报告说明](SECURITY.md)。

## 隐私与权属

加密隧道有助于保护传输中的流量，但本身不保证完全匿名。数据处理方式请查看当前有效的官方服务政策。

Pangolin VPN 为专有软件。本仓库不授予对应用、商标或文档的许可；本次初始化不提供开源许可。
