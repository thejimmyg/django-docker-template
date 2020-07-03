# Django Docker Template

To use this template:

1. Clone or download to your project name (the instructions assume the folder name you clone to is the same as the name of your Django project):

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
```

4. Follow the instructions in the new `README.md`


## Potential Improvements

* The current set up causes an infinite redirect if you register as a normal user and then try to access Wagtail or the Django admin. It should probably give an error message instead.
* Nginx could perform the redirect to www. rather than Django? (The redirect is now configured with the `PREPEND_WWW` environment vairbale).
