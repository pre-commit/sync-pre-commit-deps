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
    rev: v0.0.1
    hooks:
    -   id: sync-pre-commit-deps
```

## cli

```console
$ sync-pre-commit-deps path/to/.pre-commit-config.yaml
```

## what it does

Ensures tools which declare `flake8` and `black` as additional dependencies will have those versions synced with the `flake8` and `black` versions in the rest of the config.

```diff
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
