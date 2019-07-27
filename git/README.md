# Git

Generate an RSA key named `id_rsa` into the `ssh` directory with:

```
cd ssh
ssh-keygen -t rsa
```

Share `id_rsa.pub` with GitHub or BitBucket.

Then you can run this, using the SSH key generated and the author and committer information in the `docker-compose.yml` file:

```
alias git='docker-compose run --rm git'
git push origin master
```

By default, the `docker-compose.yml` file mounts the entire git tree into the `/repo` directory and uses that as the working directory. This means that `git` insite the container behaves as if it were running locally on your repo.
