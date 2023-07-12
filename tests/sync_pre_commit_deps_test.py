from __future__ import annotations

from sync_pre_commit_deps import main


def test_main_noop(tmpdir):
    s = (
        "repos:\n"
        "-   repo: https://github.com/psf/black\n"
        "    rev: 23.3.0\n"
        "    hooks:\n"
        "    -   id: black\n"
        "-   repo: https://github.com/adamchainz/blacken-docs\n"
        "    rev: 1.15.0\n"
        "    hooks:\n"
        "    -   id: blacken-docs\n"
        "        additional_dependencies:\n"
        "        -   black==23.3.0\n"
    )
    cfg = tmpdir.join(".pre-commit-config.yaml")
    cfg.write(s)

    assert not main((str(cfg),))

    assert cfg.read() == s


def test_main_writes_both(tmpdir):
    cfg = tmpdir.join(".pre-commit-config.yaml")
    cfg.write(
        "repos:\n"
        # should not be touched
        "-   repo: https://github.com/asottile/pyupgrade\n"
        "    rev: v3.8.0\n"
        "    hooks:\n"
        "    -   id: pyupgrade\n"
        # gives the `black` version
        "-   repo: https://github.com/psf/black\n"
        "    rev: 23.3.0\n"
        "    hooks:\n"
        "    -   id: black\n"
        # gives the `flake8` version
        "-   repo: https://github.com/PyCQA/flake8\n"
        "    rev: 6.0.0\n"
        "    hooks:\n"
        "    -   id: flake8\n"
        # all 3 below should be rewritten
        "-   repo: https://github.com/asottile/yesqa\n"
        "    rev: v1.5.0\n"
        "    hooks:\n"
        "    -   id: yesqa\n"
        "        additional_dependencies:\n"
        "        -   flake8==5.0.0\n"
        "-   repo: https://github.com/adamchainz/blacken-docs\n"
        "    rev: 1.15.0\n"
        "    hooks:\n"
        "    -   id: blacken-docs\n"
        "        additional_dependencies:\n"
        "        -   black==22.12.0\n"
        "-   repo: https://github.com/example/example\n"
        "    rev: v1.0.0\n"
        "    hooks:\n"
        "    -   id: example\n"
        "        additional_dependencies:\n"
        "        -   black==22.12.0\n"
        "        -   flake8==5.0.0\n"
    )

    assert main((str(cfg),))

    assert cfg.read() == (
        "repos:\n"
        "-   repo: https://github.com/asottile/pyupgrade\n"
        "    rev: v3.8.0\n"
        "    hooks:\n"
        "    -   id: pyupgrade\n"
        "-   repo: https://github.com/psf/black\n"
        "    rev: 23.3.0\n"
        "    hooks:\n"
        "    -   id: black\n"
        "-   repo: https://github.com/PyCQA/flake8\n"
        "    rev: 6.0.0\n"
        "    hooks:\n"
        "    -   id: flake8\n"
        "-   repo: https://github.com/asottile/yesqa\n"
        "    rev: v1.5.0\n"
        "    hooks:\n"
        "    -   id: yesqa\n"
        "        additional_dependencies:\n"
        "        -   flake8==6.0.0\n"
        "-   repo: https://github.com/adamchainz/blacken-docs\n"
        "    rev: 1.15.0\n"
        "    hooks:\n"
        "    -   id: blacken-docs\n"
        "        additional_dependencies:\n"
        "        -   black==23.3.0\n"
        "-   repo: https://github.com/example/example\n"
        "    rev: v1.0.0\n"
        "    hooks:\n"
        "    -   id: example\n"
        "        additional_dependencies:\n"
        "        -   black==23.3.0\n"
        "        -   flake8==6.0.0\n"
    )


def test_main_no_dep_on_one_and_writes_other(tmpdir):
    cfg = tmpdir.join(".pre-commit-config.yaml")
    cfg.write(
        "repos:\n"
        "-   repo: https://github.com/psf/black\n"
        "    rev: 23.3.0\n"
        "    hooks:\n"
        "    -   id: black\n"
        "-   repo: https://github.com/asottile/yesqa\n"
        "    rev: v1.5.0\n"
        "    hooks:\n"
        "    -   id: yesqa\n"
        "        additional_dependencies:\n"
        # should not be rewritten because target version can't be found
        "        -   flake8==5.0.0\n"
        "-   repo: https://github.com/adamchainz/blacken-docs\n"
        "    rev: 1.15.0\n"
        "    hooks:\n"
        "    -   id: blacken-docs\n"
        "        additional_dependencies:\n"
        # should be rewritten
        "        -   black==22.12.0\n"
    )

    assert main((str(cfg),))

    assert cfg.read() == (
        "repos:\n"
        "-   repo: https://github.com/psf/black\n"
        "    rev: 23.3.0\n"
        "    hooks:\n"
        "    -   id: black\n"
        "-   repo: https://github.com/asottile/yesqa\n"
        "    rev: v1.5.0\n"
        "    hooks:\n"
        "    -   id: yesqa\n"
        "        additional_dependencies:\n"
        "        -   flake8==5.0.0\n"
        "-   repo: https://github.com/adamchainz/blacken-docs\n"
        "    rev: 1.15.0\n"
        "    hooks:\n"
        "    -   id: blacken-docs\n"
        "        additional_dependencies:\n"
        "        -   black==23.3.0\n"
    )
