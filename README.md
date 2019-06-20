# Django Docker Template

To use this template:

1. Replace all instances of `mysite` with the actual name of your project, e.g. `myactualsite`:

```
find . -type f -name "*" -print0 | xargs -0 sed -i '' -e 's/mysite/myactualsite/g'
```

2. Delete this file and replace with the real `README.md`:

```
mv README.md.real README.md
```
