#!/usr/bin/env python3
"""
Generate a `nav:` section for mkdocs.yml from the `docs/` folder structure.

This script rewrites the `nav:` block in `mkdocs.yml` to include all
Markdown files under `docs/`, grouping them by folders. It keeps other
configuration in `mkdocs.yml` intact.

Run:
  python scripts/generate_nav.py

"""
import os
import re
import sys


def clean_title(name: str) -> str:
    # Remove leading numeric prefixes like '00-' and file extensions
    name = re.sub(r'^\d+[-_]*', '', name)
    name = re.sub(r'[-_]+', ' ', name)
    name = os.path.splitext(name)[0]
    return name.strip().replace('\n', ' ').strip().title()


def collect_docs(docs_dir: str):
    entries = []
    # collect root markdown files
    for item in sorted(os.listdir(docs_dir)):
        path = os.path.join(docs_dir, item)
        if os.path.isfile(path) and item.lower().endswith('.md'):
            entries.append((item, os.path.relpath(path, docs_dir).replace('\\', '/')))
    # collect directories
    for item in sorted(os.listdir(docs_dir)):
        path = os.path.join(docs_dir, item)
        if os.path.isdir(path):
            subitems = []
            for root, dirs, files in os.walk(path):
                # sort files for stable output
                files = sorted(f for f in files if f.lower().endswith('.md'))
                # compute relative root from docs_dir
                rel_root = os.path.relpath(root, docs_dir).replace('\\', '/')
                for f in files:
                    relpath = os.path.join(rel_root, f).replace('\\', '/')
                    title = clean_title(f)
                    subitems.append((title, relpath))
            if subitems:
                entries.append((item, subitems))
    return entries


def render_nav(entries):
    lines = []
    lines.append('nav:')
    # prefer index.md as Home if present in root entries
    root_files = [e for e in entries if isinstance(e[1], str)]
    for name, rel in root_files:
        title = 'Home' if name.lower() == 'index.md' else clean_title(name)
        lines.append(f"  - {title}: {rel}")

    # folders / grouped entries
    for name, value in entries:
        if isinstance(value, list):
            title = clean_title(name)
            lines.append(f"  - {title}:")
            for sub_title, sub_rel in value:
                safe_title = sub_title.replace(':', ' -')
                lines.append(f"      - {safe_title}: {sub_rel}")
    return '\n'.join(lines) + '\n'


def main():
    repo_root = os.path.abspath(os.path.dirname(__file__) + os.path.sep + '..')
    docs_dir = os.path.join(repo_root, 'docs')
    mk_file = os.path.join(repo_root, 'mkdocs.yml')

    if not os.path.isdir(docs_dir):
        print('docs/ folder not found', file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(mk_file):
        print('mkdocs.yml not found', file=sys.stderr)
        sys.exit(1)

    entries = collect_docs(docs_dir)
    nav_block = render_nav(entries)

    # Read existing mkdocs.yml and replace nav block
    with open(mk_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start = None
    for i, l in enumerate(lines):
        if l.lstrip().startswith('nav:') and (l.startswith('nav:') or l.startswith('nav:')):
            start = i
            break

    if start is None:
        # append nav at end
        new_content = ''.join(lines) + '\n' + nav_block
    else:
        # find where the nav block ends: next top-level key (no indentation, ends with ':')
        end = None
        for j in range(start + 1, len(lines)):
            if re.match(r'^\S.*:$', lines[j]):
                end = j
                break
        if end is None:
            new_content = ''.join(lines[:start]) + nav_block
        else:
            new_content = ''.join(lines[:start]) + nav_block + ''.join(lines[end:])

    with open(mk_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print('Updated mkdocs.yml nav section')


if __name__ == '__main__':
    main()
