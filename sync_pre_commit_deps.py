from __future__ import annotations

import argparse
from collections.abc import Sequence

import ruamel.yaml

SUPPORTED = frozenset(('black', 'flake8'))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='.pre-commit-config.yaml')

    args = parser.parse_args(argv)
    filename: str = args.filename

    # match pre-commit config as documented
    # TODO - support round-tripping
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=4, sequence=4)

    with open(filename) as f:
        loaded = yaml.load(f)

    # TODO - validate schema?
    versions = {}
    for repo in loaded['repos']:
        for hook in repo['hooks']:
            if (hid := hook['id']) in SUPPORTED:
                versions[hid] = repo['rev']

    updated = []
    for repo in loaded['repos']:
        for hook in repo['hooks']:
            for i, dep in enumerate(hook.get('additional_dependencies', ())):
                name, _, cur_version = dep.partition('==')
                target_version = versions.get(name, cur_version)
                if target_version != cur_version:
                    name_and_version = f'{name}=={target_version}'
                    hook['additional_dependencies'][i] = name_and_version
                    updated.append((hook['id'], name))

    if updated:
        print(f'Writing updates to {filename}:')
        for hid, name in updated:
            print(f'\tSetting {hid!r} dependency {name!r} to {versions[name]}')

        with open(filename, 'w+') as f:
            yaml.dump(loaded, f)
        return 1

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
