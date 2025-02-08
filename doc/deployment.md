# Deployment

## Container

To deploy the application, just run the `docker-compose.yml` in the root folder:

```bash
$ docker-compose up -f docker-compose.yml -p ctr-custom-tracks
```

The compose file will create 3 containers:

* The web application, running on port **80**
* The database, running on port **5432**
* The adminer container, running on port **8080**

I recommend installing some reverse proxy in front of the website and adminer to handle SSL, 
request throttling and other things.

## Rotating JWT Secrets

The application uses [JWT](https://jwt.io/)s to authenticate users. The JWTs are signed with a secret key, which is
stored inside the .env file.

To prevent users from reusing older, valid JWTs it is recommended you set up a cronjob to rotate
the secret key regularly. The application will then automatically use the new secret key to sign new JWTs.

Here is an example cronjob to rotate the secret key every 30 days:

```bash
$ chmod +x /app/update_jwt_secret.sh
$ 0 0 */30 * * /app/update_jwt_secret.sh
```
