#!/usr/bin/env python3
"""Validate local documentation links and HTML index coverage; no network calls."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src') and value:
                self.links.append(value)
            if key == 'id':
                self.ids.add(value)

def main():
    errors = []
    files = sorted([*ROOT.glob('*.md'), *ROOT.glob('docs/**/*.html'), *ROOT.glob('assets/**/*.md')])
    index = Links()
    index.feed((ROOT / 'docs/index.html').read_text())
    indexed = {urlsplit(link).path for link in index.links}
    for source in files:
        content = source.read_text()
        if source.suffix == '.html':
            parser = Links()
            parser.feed(content)
            links = parser.links
            if '<title>' not in content or 'name="viewport"' not in content:
                errors.append(f'{source.relative_to(ROOT)}: missing title or viewport')
            if source.name != 'index.html' and source.relative_to(ROOT / 'docs').as_posix() not in indexed:
                errors.append(f'{source.relative_to(ROOT)}: absent from docs index')
        else:
            links = re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', content)
        for link in links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            if parts.path.startswith('/'):
                errors.append(f'{source.relative_to(ROOT)}: absolute local link {link}')
                continue
            target = (source.parent / unquote(parts.path)).resolve() if parts.path else source
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f'{source.relative_to(ROOT)}: missing or out-of-repository target {link}')
            elif parts.fragment and target.suffix == '.html':
                anchors = Links()
                anchors.feed(target.read_text())
                if unquote(parts.fragment) not in anchors.ids:
                    errors.append(f'{source.relative_to(ROOT)}: missing anchor {link}')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Validated {len(files)} documentation files and local links. External URLs and product claims require manual verification.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
