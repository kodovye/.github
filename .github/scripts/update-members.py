#!/usr/bin/env python3
"""Regenerate the CORE members block in profile/README.md
from the list of public org members stored in /tmp/members.txt."""

import re
import pathlib
import sys

PER_ROW = 6

members_file = pathlib.Path('/tmp/members.txt')
members = [m.strip() for m in members_file.read_text().splitlines() if m.strip()]

if not members:
    sys.exit('No members — not touching README.')

rows = []
for i in range(0, len(members), PER_ROW):
    cells = []
    for user in members[i:i + PER_ROW]:
        cells.append(
            f'<td align="center" width="110">'
            f'<a href="https://github.com/{user}">'
            f'<img src="https://github.com/{user}.png" width="90" height="90" '
            f'style="border-radius:50%" alt="{user}" />'
            f'<br/><sub><b>{user}</b></sub></a></td>'
        )
    while len(cells) < PER_ROW:
        cells.append('<td width="110"></td>')
    rows.append('<tr>' + ''.join(cells) + '</tr>')

block = '<table align="center">' + ''.join(rows) + '</table>'
new_section = f'<!-- CORE:START -->\n{block}\n<!-- CORE:END -->'

readme = pathlib.Path('profile/README.md')
src = readme.read_text(encoding='utf-8')

pattern = re.compile(r'<!-- CORE:START -->.*?<!-- CORE:END -->', re.DOTALL)
if not pattern.search(src):
    sys.exit('CORE markers not found in README, aborting.')

updated = pattern.sub(lambda _: new_section, src)

if updated != src:
    readme.write_text(updated, encoding='utf-8')
    print('README updated.')
else:
    print('No changes.')
