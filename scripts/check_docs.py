#!/usr/bin/env python3
"""Validate local Markdown links and documentation index coverage."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')

def main():
    errors = []
    files = sorted([*ROOT.glob('*.md'), *ROOT.glob('docs/**/*.md'), *ROOT.glob('assets/**/*.md')])
    index = ROOT / 'docs/index.md'
    indexed = {urlsplit(link).path for link in LINK.findall(index.read_text())}
    for source in files:
        content = source.read_text()
        for link in LINK.findall(content):
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            if parts.path.startswith('/'):
                errors.append(f'{source.relative_to(ROOT)}: absolute local link {link}')
                continue
            target = (source.parent / unquote(parts.path)).resolve() if parts.path else source
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f'{source.relative_to(ROOT)}: missing or out-of-repository target {link}')
            elif source.parent == ROOT / 'docs' and source != index and target.suffix == '.md':
                rel = target.relative_to(ROOT / 'docs').as_posix()
                if rel not in indexed:
                    errors.append(f'{source.relative_to(ROOT)}: absent from docs/index.md')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Validated {len(files)} Markdown files and local links. External URLs and product claims require manual verification.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
