#!/usr/bin/env python3
"""Regenerate the CORE members block in profile/README.md
from the list of public org members stored in /tmp/members.txt."""

import re
import pathlib
import sys

MAX_PER_ROW = 6
AVATAR_SIZE = 96

members_file = pathlib.Path('/tmp/members.txt')
members = [m.strip() for m in members_file.read_text().splitlines() if m.strip()]

if not members:
    sys.exit('No members — not touching README.')

# Dynamic row width: if few members, fit all into one row (no empty padding cells)
per_row = min(MAX_PER_ROW, len(members))

def cell(user: str) -> str:
    # avatar is clickable; username is plain bold text so GitHub doesn't style it as blue link
    return (
        f'<td align="center" valign="top" width="130">'
        f'<a href="https://github.com/{user}">'
        f'<img src="https://github.com/{user}.png?size=200" width="{AVATAR_SIZE}" height="{AVATAR_SIZE}" '
        f'style="border-radius:50%" alt="{user}" />'
        f'</a>'
        f'<br/><sub><b>{user}</b></sub>'
        f'</td>'
    )

rows_html = []
for i in range(0, len(members), per_row):
    batch = members[i:i + per_row]
    cells = [cell(u) for u in batch]
    # For the last row, if it's shorter than per_row, DO NOT pad — let it be narrower.
    # The outer <table align="center"> will center it visually.
    rows_html.append('<tr>' + ''.join(cells) + '</tr>')

# If the very last row is partial (happens only when members > MAX_PER_ROW),
# pull it out into its own centered table so it looks balanced, not left-aligned
# under a wider row.
if len(members) > MAX_PER_ROW and len(members) % MAX_PER_ROW != 0:
    main_rows = rows_html[:-1]
    last_row = rows_html[-1]
    block = (
        f'<table align="center">{"".join(main_rows)}</table>'
        f'<table align="center">{last_row}</table>'
    )
else:
    block = f'<table align="center">{"".join(rows_html)}</table>'

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
