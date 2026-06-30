The user wants to explore how the book's ideas connect, using the knowledge graph.

If they gave a question (**$ARGUMENTS**), answer it with the graph:

```bash
if [ -x .venv/bin/graphify ]; then GF=.venv/bin/graphify; else GF=graphify; fi
$GF query "$ARGUMENTS"
```

Then translate the raw graph output into plain language for the user: which concepts connect to
which, which chapter each lives in, and what the connection reveals about the book. Cite the
chapters by name.

If they gave NO question, open the visual map in their browser instead:

```bash
open graphify-out/graph.html
```

and tell them they can click around the map of every concept in the book. If `graphify` is not
installed yet, run `/setup` first.
