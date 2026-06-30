The user wants the latest version of the book (Brody keeps the shared copy up to date).

Do this for them and report in plain language:

```bash
git pull
if [ -x .venv/bin/python ]; then PY=.venv/bin/python; else PY=python3; fi
$PY tools/build_index.py
```

Then tell them what changed: run `git log --oneline -8` and summarize any new updates in plain
English (for example "Brody added a new version of the North chapter"). If nothing changed, just
say they are already up to date. If the search index rebuilt, mention search now reflects the
latest text.
