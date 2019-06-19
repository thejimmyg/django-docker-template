# mysite

Heroku will expect an app called `mysite-staging` to be created, along with a free PostgreSQL instance. You will need a Stripe account with a test Secret key. The Heroku instance needs the following variables set up:

* `SECRET_KEY` -  a long (32 characters+) random string used for deriving secrets for the session cookies and other things
* `ALLOWED_HOSTS` - a comma-separated list of allowed hosts
* `ADMINS` - a comma-separated list of emails to receive error reports
* `DJANGO_SETTINGS_MODULE` - `mysite.settings.production`

## Development

1. Install the latest version of Docker
2. Clone the repo to a directory called `mysite` (if you choose a different name, Docker Compose will name the containers in a different way to the names used in the documentation).
3. Copy `docker-compose.yml.example` to `docker-compose.yml` and update it with the settings you want to use for development, including `STRIPE_API_SECRET_KEY`
4. Run `docker-compose up`

Your will be hosted then at http://localhost:8001 (the port may be different if you configured a different `PORT` variable.

You can also make a copy of `web/run.sh` and update docker-compose.yml to use it in `cmd`:

```
cp web/run.sh web/run.sh.local
```

## Deployment

### Release to Heroku

Make sure static files are up to date:

```
docker exec -it mysite_web_1 /usr/local/bin/python3 manage.py collectstatic --noinput --link
```

Set the deployment target to the Heroku app name:

```
export DEPLOYMENT_TARGET=mysite-staging
```

Create a new version number each time. You can find the old number like this:

```
docker images | grep $DEPLOYMENT_TARGET
```

Then export the new version:

```
export BACKEND_VERSION=0.1.1
```

Then commit any changes you want to deploy.

Finally run these one at a time, otherwise they might not all get run:


```
heroku login
heroku container:login
git stash
cd web
docker build -t $DEPLOYMENT_TARGET:$BACKEND_VERSION .
docker tag $DEPLOYMENT_TARGET:$BACKEND_VERSION registry.heroku.com/$DEPLOYMENT_TARGET/web
docker push registry.heroku.com/$DEPLOYMENT_TARGET/web
heroku container:release --app $DEPLOYMENT_TARGET web
heroku run --type=worker -a $DEPLOYMENT_TARGET /usr/local/bin/python3 manage.py migrate
git stash pop
```

Other useful commands:

```
heroku config --app $DEPLOYMENT_TARGET
heroku logs --tail --app $DEPLOYMENT_TARGET
```
