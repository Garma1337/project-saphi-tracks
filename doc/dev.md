# Contributing

## Introduction

I made this website using [Rust](https://doc.rust-lang.org/) for the backend. I have no idea why, I just wanted to
play around with the language. The frontend was created using the good old [React](https://react.dev/learn), although I used [Vite](https://vite.dev/guide/)
to set up the frontend.

As for the backend, I used a web framework called [Rocket](https://rocket.rs/guide) and an ORM library called [Diesel](https://diesel.rs/guides).
As for the database, I decided to use [PostgreSQL](https://www.postgresql.org/docs/).

If you want to develop a new feature, just fork the project and open a PR. Considering the website is relatively
small and straightforward I don't think there's too much that needs to be done though.

## Folder Structure

* `doc/`: Contains the documentation for the project
* `migrations/`: Contains the database migrations to use with `Diesel`
* `src/`: Contains the source code for the website backend (basically the REST API)
  * `controllers/`: Contains the controllers for the REST API
  * `models/`: Contains the models for the database
  * `repository/`: Contains the repositories for the models
  * `services/`: Contains various services
  * `tests/`: Contains the unit tests for the backend
  * `schema.rs`: Contains the database schema
* `web/`: Contains the source code for the website frontend

## Testing

If you develop a new feature, make sure to write unit tests for it. I am not going
to merge PRs that don't have proper test coverage. You don't need to unit test *everything* ...
just be sensible about it and make sure your feature works.
