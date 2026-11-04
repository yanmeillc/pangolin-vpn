# Pangolin VPN 公开文档仓库

## 定位与范围
本仓库是 Pangolin VPN 的官方 GitHub 产品展示与公开文档入口，维护主体为 Yanmei AI LLC。目标是帮助访问者了解产品、找到官方安装入口、理解公开技术边界并提交反馈。

维护内容：产品说明、功能介绍、安装与使用指南、公开技术文档、常见问题、排障说明、公开图片与 GitHub 社区模板。
不存放：专有客户端/服务端源码、节点配置、基础设施清单、内部运维信息、用户数据、凭证或未经清理的诊断日志。推广活动文案和渠道素材统一归推广仓库，不在此维护。

## 内容真源与准确性
- 官网为 https://pangolin.yanmeiai.com/ 。运营主体为 Yanmei AI LLC，公开联系邮箱为 admin@yanmeiai.com。
- 现有 README 只提供产品概述，不作为平台已发布、协议已实现或安全承诺的证据。
- 平台支持、最低系统要求、版本、价格、下载地址、协议和功能状态必须根据已核实的官方产品信息更新。未核实项明确标为待核实；不编造安装命令或下载链接。
- 不承诺绝对匿名、零日志、绕过所有限制或固定速度；隐私与服务政策链接需验证后加入。
- 对外文档默认英文；维护规则可用中文。增加其他语言时保持目录对应与内容同步。

## 结构与文档约定
- README.md：GitHub 首屏与文档导航。
- docs/index.html：所有公开文档的入口与分类索引。
- docs/product/：产品与功能说明。
- docs/guides/：安装和使用指南。
- docs/technical/：公开连接模型与技术边界。
- docs/support/：FAQ、排障与反馈。
- docs/plans/：公开可见的仓库设计方案；不放内部商业计划。
- assets/：可公开图片与品牌素材，使用前确认版权与隐私。
- scripts/：本地文档校验工具；.github/：CI 与反馈模板。

新文档使用自包含 HTML、统一深色主题、内联 CSS/JS，不依赖 CDN。页面之间、图片和脚本使用相对路径；新增页面登记 docs/index.html。README、AGENTS、贡献规范和 GitHub 模板保留原生格式。内容优先于视觉特效，不引入网站框架或托管配置，除非任务明确需要。

## 开发与交付
先检查工作区与 worktree，再 git fetch origin，检查 main...origin/main。新任务从 origin/main 建立独立分支与 worktree，位置为项目根目录下 .codex/worktrees/<分支名>/。主工作区保留 main，保留无关改动。

提交前运行 python3 scripts/check_docs.py，检查页面链接、内容状态及 git diff --check。完成后提交、推送并创建 PR；用户确认后才能合并。未经明确授权不得部署、开启 Pages、打 tag 或发布版本。

## 本地阅读
直接打开 docs/index.html，或在 worktree 根目录运行 python3 -m http.server 8000，再访问 http://localhost:8000/docs/ 。重启时停止旧进程并重新执行该命令。
