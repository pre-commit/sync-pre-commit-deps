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
-   repo: https://github.com/pre-commit/sync-pre-commit-deps
    rev: v0.0.3
    hooks:
    -   id: sync-pre-commit-deps
```

## cli

```console
$ sync-pre-commit-deps path/to/.pre-commit-config.yaml
```

## what it does

Hooks like `black`, `yesqa`, and `eslint` reference additional dependencies which are also `pre-commit` hooks. This tool syncs the version in `additional_dependencies` with the version in `rev`.

For example, `flake8` under `yesqa` is updated from `5.0.0` to `6.0.0` because the `flake8` hook uses `6.0.0`:

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

Another example, the `eslint` version in `additional_dependencies` is updated to match the version in `rev`:

```diff
 -   repo: https://github.com/pre-commit/mirrors-eslint
     rev: v4.15.0
     hooks:
     -   id: eslint
         additional_dependencies:
-        -   eslint@4.14.0
+        -   eslint@4.15.0
         -   eslint-config-google@0.7.1
         -   eslint-loader@1.6.1
         -   eslint-plugin-react@6.10.3
         -   babel-eslint@6.1.2
```

## what it doesn't do

- Does not add new additional dependencies. Only updates versions for dependencies that are already specified.
- Does not sync versions from `package.json`, `requirements.txt`, `pyproject.toml`, etc.
