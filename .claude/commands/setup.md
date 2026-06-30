Set up this workspace for the user. They are likely not technical, so do this FOR them and
explain it in plain language.

Run the setup script and show the user the progress:

```bash
bash setup.sh
```

This creates a self-contained environment, installs the knowledge-graph search, and builds the
search index over the book. It is safe to run more than once.

When it finishes, tell the user in one or two friendly sentences that everything is ready, and
remind them they can now use `/find`, `/graph`, `/board`, or just ask you anything about the book.
If any step reported a hiccup, reassure them that you can still read and search the whole book
directly, so nothing is blocked.
