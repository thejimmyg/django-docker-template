# Django Docker Template

To use this template:

1. Clone and download to your project name (the instructions assume the folder name you clone to is the same as the name of your Django project):

```
git clone https://github.com/thejimmyg/django-docker-template.git myactualsite
cd myactualsite
```

2. Replace all instances of `mysite` with the actual name of your project, e.g. `myactualsite`:

```
rm -rf .git
find . -type f -name "*" | grep -v ".git" | grep -v '.DS_Store' | xargs sed -i '' -e 's/mysite/myactualsite/g'
```

3. Delete this file and replace with the real `README.md`:

```
mv -f README.md.real README.md
git init
git add .
```

4. Follow the instructions in the new `README.md`
