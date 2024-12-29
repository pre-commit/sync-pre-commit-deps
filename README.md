sync-pre-commit-deps
====================

Sync pre-commit hook dependencies based on other installed hooks

## install (standalone)

```bash
pip install sync-pre-commit-deps
```

## install as a pre-commit hook (recommended)

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/mxr/sync-pre-commit-deps
    rev: v0.0.2
    hooks:
    -   id: sync-pre-commit-deps
```

## cli

```console
$ sync-pre-commit-deps path/to/.pre-commit-config.yaml
```

## what it does

Ensures tools which declare `flake8`, `black`, or `mypy` as additional dependencies will have those versions synced with the `flake8`, `black`, or `mypy` versions in the rest of the config. For example, `flake8` under `yesqa` is updated from `5.0.0` to `6.0.0`.

```diff
 repos:
 -   repo: https://github.com/PyCQA/flake8
     rev: 6.0.0
     hooks:
     -   id: flake8
 -   repo: https://github.com/asottile/yesqa
     rev: v1.5.0
     hooks:
     -   id: yesqa
         additional_dependencies:
-        -   flake8==5.0.0
+        -   flake8==6.0.0
```
