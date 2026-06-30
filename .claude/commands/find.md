The user wants a fast keyword search of the book for: **$ARGUMENTS**

Run the search tool (prefer the workspace environment if it exists):

```bash
if [ -x .venv/bin/python ]; then PY=.venv/bin/python; else PY=python3; fi
$PY tools/search.py "$ARGUMENTS" --keyword --top 8
```

If it says there is no index yet, run `/setup` for the user first, then try again.

Present the results in plain language: for each hit, name the chapter (the source file maps to a
chapter, for example `02-north-identity.md` is the North / Identity chapter) and show the short
quote. Then offer to open the full passage or to search how the ideas connect with `/graph`.
