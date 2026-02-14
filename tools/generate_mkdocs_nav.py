import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
DOCS_DIR = os.path.join(ROOT, 'docs')
MKDOCS_YML = os.path.join(ROOT, 'mkdocs.yml')

SKIP_DIRS = {'originals', '.git', '.venv', 'assets'}

def title_from_filename(name):
    if name.lower() == 'index.md':
        return 'Home'
    base = os.path.splitext(name)[0]
    base = base.replace('_', ' ').replace('-', ' ')
    return base.strip().title()

def nav_lines_for_dir(path, rel_prefix='', indent=2):
    lines = []
    items = []
    try:
        entries = sorted(os.listdir(path))
    except FileNotFoundError:
        return lines

    files = [e for e in entries if os.path.isfile(os.path.join(path, e)) and e.endswith('.md')]
    dirs = [e for e in entries if os.path.isdir(os.path.join(path, e))]

    # add files first
    for f in files:
        # skip README.md at root (we already have index)
        if f.lower() == 'readme.md':
            continue
        title = title_from_filename(f)
        rel = os.path.join(rel_prefix, f).replace('\\', '/')
        lines.append(' ' * indent + f"- {title}: {rel}\n")

    # then directories
    for d in dirs:
        if d in SKIP_DIRS:
            continue
        subpath = os.path.join(path, d)
        # check if dir contains any md files
        has_md = False
        for root, _, files2 in os.walk(subpath):
            for f2 in files2:
                if f2.endswith('.md'):
                    has_md = True
                    break
            if has_md:
                break
        if not has_md:
            continue
        display = d.replace('-', ' ').replace('_', ' ').title()
        lines.append(' ' * indent + f"- {display}:\n")
        # recurse
        child_rel = os.path.join(rel_prefix, d)
        child_lines = nav_lines_for_dir(subpath, child_rel, indent=indent+2)
        lines.extend(child_lines)

    return lines

def build_nav():
    lines = []
    # root index.md -> Home
    index_path = os.path.join(DOCS_DIR, 'index.md')
    if os.path.exists(index_path):
        lines.append('  - Home: index.md\n')

    # top level files and folders
    lines.extend(nav_lines_for_dir(DOCS_DIR, rel_prefix='', indent=2))
    return lines

def main():
    if not os.path.isdir(DOCS_DIR):
        print('docs directory not found', file=sys.stderr)
        sys.exit(1)

    with open(MKDOCS_YML, 'r', encoding='utf-8') as f:
        content = f.read()

    # find 'nav:' start
    parts = content.split('\n')
    nav_index = None
    for i, line in enumerate(parts):
        if line.strip() == 'nav:':
            nav_index = i
            break

    if nav_index is None:
        print('mkdocs.yml has no nav: key', file=sys.stderr)
        sys.exit(1)

    header = '\n'.join(parts[:nav_index]) + '\n'
    new_nav = 'nav:\n' + ''.join(build_nav())

    new_content = header + new_nav
    with open(MKDOCS_YML, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print('Regenerated nav in mkdocs.yml')

if __name__ == '__main__':
    main()
