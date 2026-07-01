The user wants to save a snapshot of their work (a git commit). They are likely not technical, so
do it for them and explain it simply.

What "saving a snapshot" means, in plain words (say this if they seem unsure): it is like hitting
save with a label on it. It records the book exactly as it is right now, so you can always look
back or undo to this point later. It stays on your own computer.

Steps:

```bash
git add -A
git commit -m "MESSAGE"
```

Pick a short, plain-English MESSAGE describing what changed (for example "Reworked the North
chapter opening" or "Fixed typos in South"). If you are not sure what changed, run
`git diff --cached --stat` first and base the message on that.

After committing, the search index refreshes automatically. Tell the user it is saved, in one
friendly sentence.

About sharing with Brody: a snapshot saves on THIS computer only. If they want Brody to have these
changes, the simplest way for now is to send Brody the changed file(s), since sharing back to the
shared copy needs a GitHub account they do not have yet. Only mention this if they ask how Brody
sees their edits. Do not push unless they explicitly ask and have access.
