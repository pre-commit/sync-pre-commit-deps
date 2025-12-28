from __future__ import annotations

import pytest

from sync_pre_commit_deps import main


@pytest.mark.parametrize(
    ('s',),
    (
        pytest.param(
            'repos:\n'
            '-   repo: https://github.com/psf/black\n'
            '    rev: 23.3.0\n'
            '    hooks:\n'
            '    -   id: black\n'
            '-   repo: https://github.com/adamchainz/blacken-docs\n'
            '    rev: 1.15.0\n'
            '    hooks:\n'
            '    -   id: blacken-docs\n'
            '        additional_dependencies:\n'
            '        -   black==23.3.0\n',
            id='already correct version',
        ),
        pytest.param(
            'repos:\n'
            '-   repo: https://github.com/adamchainz/blacken-docs\n'
            '    rev: 1.15.0\n'
            '    hooks:\n'
            '    -   id: blacken-docs\n'
            '        additional_dependencies:\n'
            '        -   black==23.3.0\n',
            id='no hook to get the version from',
        ),
        pytest.param(
            'repos:\n'
            '-   repo: https://github.com/PyCQA/flake8\n'
            '    rev: 6.0.0\n'
            '    hooks:\n'
            '    -   id: flake8\n'
            '        additional_dependencies:\n'
            '        -   flake-bugbear==3.1.0\n',
            id='dep not supported',
        ),
        pytest.param(
            'repos:\n'
            '-   repo: local\n'
            '    hooks:\n'
            '    -   id: mypy\n'
            '-   repo: https://github.com/nbQA-dev/nbQA\n'
            '    rev: 1.9.1\n'
            '    hooks:\n'
            '    -   id: nbqa-mypy\n'
            '        additional_dependencies:\n'
            '        -   mypy==0.123\n',
            id='local hook shadows supported lib',
        ),
        pytest.param(
            'repos:\n'
            '-   repo: https://github.com/psf/black\n'
            '    rev: 23.3.0\n'
            '    hooks:\n'
            '    -   name: \N{SNOWMAN} black\n'
            '        id: black\n',
            id='unicode no-op',
        ),
    ),
)
def test_main_noop(tmpdir, s):
    cfg = tmpdir.join('.pre-commit-config.yaml')
    cfg.write_binary(s.encode())

    assert not main((str(cfg),))

    with open(cfg, encoding='utf-8') as f:
        assert f.read() == s


def test_main_writes_all(tmpdir):
    cfg = tmpdir.join('.pre-commit-config.yaml')
    cfg.write(
        'repos:\n'
        # should not be touched
        '-   repo: https://github.com/asottile/pyupgrade\n'
        '    rev: v3.8.0\n'
        '    hooks:\n'
        '    -   id: pyupgrade\n'
        # gives the `black` version
        '-   repo: https://github.com/psf/black\n'
        '    rev: 23.3.0\n'
        '    hooks:\n'
        '    -   id: black\n'
        # gives the `flake8` version
        '-   repo: https://github.com/PyCQA/flake8\n'
        '    rev: 6.0.0\n'
        '    hooks:\n'
        '    -   id: flake8\n'
        # gives the `mypy` version
        '-   repo: https://github.com/pre-commit/mirrors-mypy\n'
        '    rev: v1.13.0\n'
        '    hooks:\n'
        '    -   id: mypy\n'
        # all repos below should have their additional_dependencies rewritten
        '-   repo: https://github.com/asottile/yesqa\n'
        '    rev: v1.5.0\n'
        '    hooks:\n'
        '    -   id: yesqa\n'
        '        additional_dependencies:\n'
        '        -   flake8==5.0.0\n'
        '-   repo: https://github.com/adamchainz/blacken-docs\n'
        '    rev: 1.15.0\n'
        '    hooks:\n'
        '    -   id: blacken-docs\n'
        '        additional_dependencies:\n'
        '        -   black==22.12.0\n'
        '-   repo: https://github.com/nbQA-dev/nbQA\n'
        '    rev: 1.9.1\n'
        '    hooks:\n'
        '    -   id: nbqa-mypy\n'
        '        additional_dependencies:\n'
        '        -   mypy==0.910\n'
        '-   repo: https://github.com/example/example\n'
        '    rev: v1.0.0\n'
        '    hooks:\n'
        '    -   id: example\n'
        '        additional_dependencies:\n'
        '        -   black==22.12.0\n'
        '        -   flake8==5.0.0\n'
        '        -   mypy==0.123\n',
    )

    assert main((str(cfg),))

    assert cfg.read() == (
        'repos:\n'
        '-   repo: https://github.com/asottile/pyupgrade\n'
        '    rev: v3.8.0\n'
        '    hooks:\n'
        '    -   id: pyupgrade\n'
        '-   repo: https://github.com/psf/black\n'
        '    rev: 23.3.0\n'
        '    hooks:\n'
        '    -   id: black\n'
        '-   repo: https://github.com/PyCQA/flake8\n'
        '    rev: 6.0.0\n'
        '    hooks:\n'
        '    -   id: flake8\n'
        '-   repo: https://github.com/pre-commit/mirrors-mypy\n'
        '    rev: v1.13.0\n'
        '    hooks:\n'
        '    -   id: mypy\n'
        '-   repo: https://github.com/asottile/yesqa\n'
        '    rev: v1.5.0\n'
        '    hooks:\n'
        '    -   id: yesqa\n'
        '        additional_dependencies:\n'
        '        -   flake8==6.0.0\n'
        '-   repo: https://github.com/adamchainz/blacken-docs\n'
        '    rev: 1.15.0\n'
        '    hooks:\n'
        '    -   id: blacken-docs\n'
        '        additional_dependencies:\n'
        '        -   black==23.3.0\n'
        '-   repo: https://github.com/nbQA-dev/nbQA\n'
        '    rev: 1.9.1\n'
        '    hooks:\n'
        '    -   id: nbqa-mypy\n'
        '        additional_dependencies:\n'
        '        -   mypy==1.13.0\n'
        '-   repo: https://github.com/example/example\n'
        '    rev: v1.0.0\n'
        '    hooks:\n'
        '    -   id: example\n'
        '        additional_dependencies:\n'
        '        -   black==23.3.0\n'
        '        -   flake8==6.0.0\n'
        '        -   mypy==1.13.0\n'
    )


def test_main_no_dep_on_one_and_writes_other(tmpdir):
    cfg = tmpdir.join('.pre-commit-config.yaml')
    cfg.write(
        'repos:\n'
        '-   repo: https://github.com/psf/black\n'
        '    rev: 23.3.0\n'
        '    hooks:\n'
        '    -   id: black\n'
        '-   repo: https://github.com/asottile/yesqa\n'
        '    rev: v1.5.0\n'
        '    hooks:\n'
        '    -   id: yesqa\n'
        '        additional_dependencies:\n'
        # should not be rewritten because target versions can't be found
        '        -   flake8==5.0.0\n'
        '        -   mypy==0.910\n'
        '-   repo: https://github.com/adamchainz/blacken-docs\n'
        '    rev: 1.15.0\n'
        '    hooks:\n'
        '    -   id: blacken-docs\n'
        '        additional_dependencies:\n'
        # should be rewritten
        '        -   black==22.12.0\n'
        '-   repo: https://github.com/nbQA-dev/nbQA\n'
        '    rev: 1.9.1\n'
        '    hooks:\n'
        '    -   id: nbqa-mypy\n'
        '        additional_dependencies:\n'
        # should not be rewritten because target version can't be found
        '        -   mypy==0.123',
    )

    assert main((str(cfg),))

    assert cfg.read() == (
        'repos:\n'
        '-   repo: https://github.com/psf/black\n'
        '    rev: 23.3.0\n'
        '    hooks:\n'
        '    -   id: black\n'
        '-   repo: https://github.com/asottile/yesqa\n'
        '    rev: v1.5.0\n'
        '    hooks:\n'
        '    -   id: yesqa\n'
        '        additional_dependencies:\n'
        '        -   flake8==5.0.0\n'
        '        -   mypy==0.910\n'
        '-   repo: https://github.com/adamchainz/blacken-docs\n'
        '    rev: 1.15.0\n'
        '    hooks:\n'
        '    -   id: blacken-docs\n'
        '        additional_dependencies:\n'
        '        -   black==23.3.0\n'
        '-   repo: https://github.com/nbQA-dev/nbQA\n'
        '    rev: 1.9.1\n'
        '    hooks:\n'
        '    -   id: nbqa-mypy\n'
        '        additional_dependencies:\n'
        '        -   mypy==0.123\n'
    )
