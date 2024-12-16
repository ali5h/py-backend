# Minimal Python Build Backend

This is a minimal backend that only supports editable builds for a
python project. Building a project only in the editable mode can be
usefull in a monorepo environment.

This should work with an editable installation of the root project.

```console
$ uv run --reinstall -v hello.py
```
