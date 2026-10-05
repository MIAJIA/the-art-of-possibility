"""Build index.html from src/page.html and data/data.json.

Usage:  python scripts/build_page.py
"""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
page = (root / 'src' / 'page.html').read_text(encoding='utf-8')
data = (root / 'data' / 'data.json').read_text(encoding='utf-8')

marker = '/*__DATA__*/'
assert page.count(marker) == 1, 'src/page.html must contain the data marker exactly once'
(root / 'index.html').write_text(page.replace(marker, data), encoding='utf-8')
print('wrote', root / 'index.html')
