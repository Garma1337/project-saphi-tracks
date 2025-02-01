# Deployment

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
