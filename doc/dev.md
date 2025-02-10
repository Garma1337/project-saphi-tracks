# Contributing

## Introduction

I made this website using [Rust](https://doc.rust-lang.org/) for the backend. I have no idea why, I just wanted to
play around with the language. The frontend was created using the good old [React](https://react.dev/learn), although I used [Vite](https://vite.dev/guide/)
to set up the frontend.

As for the backend, I used a web framework called [Rocket](https://rocket.rs/guide) and an ORM library called [Sea ORM](https://www.sea-ql.org/SeaORM/docs/index/).
As for the database, I decided to use [PostgreSQL](https://www.postgresql.org/docs/).

If you want to develop a new feature, just fork the project and open a PR. Considering the website is relatively
small and straightforward I don't think there's too much that needs to be done though.

## Folder Structure

* `doc/`: Contains the documentation for the project
* `migrations/`: Contains the database migrations to use with `Sea ORM`
* `resources/`: Contains resources (files uploaded to the website) 
* `src/`: Contains the source code for the website backend (basically the REST API)
  * `auth/`: Contains permission management and authentication
  * `controllers/`: Contains the controllers for the REST API
  * `models/`: Contains the models for the database
  * `repository/`: Contains the repositories for the models
    * `filter/`: Contains filters for repository find methods
  * `services/`: Contains various services
    * `file_system_adapter/`: Contains file system adapters used for storing resources
    * `resources/`: Contains resources-related services
  * `tests/`: Contains the unit tests for the backend
* `web/`: Contains the source code for the website frontend

## Testing

If you develop a new feature, make sure to write unit tests for it. I am not going
to merge PRs that don't have proper test coverage. You don't need to unit test *everything* ...
just be sensible about it and make sure your feature works.

## ORM

When regenerating identities, use the following command:

```bash
$ sea-orm-cli generate entity -u "[db_string]" -o src/models/ --with-serde both
```

It's important to use `--with-serde both` to generate the `Serialize` and `Deserialize` implementations for the entities.