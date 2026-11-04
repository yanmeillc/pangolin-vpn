[简体中文](CONTRIBUTING.zh-CN.md)

# Contributing

This repository accepts improvements to public Pangolin VPN product information and documentation.

1. Explain the correction or proposed addition in an issue or pull request.
2. Use verified official sources for platform support, downloads, protocols and feature claims. Include the source and applicable version in the PR.
3. Write public documentation in English. Use self-contained HTML with inline styles, relative local links and no external CDN dependencies. Register new pages in docs/index.html.
4. Remove credentials, personal data, private endpoints and account information from all content and images.
5. Run `python3 scripts/check_docs.py` and `git diff --check` before submitting.

Do not submit proprietary application code, infrastructure configuration or marketing campaign materials here. Maintainers review changes through pull requests; merging and publishing require owner approval.
