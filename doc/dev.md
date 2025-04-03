# Contributing

## Introduction

First of all, thank you for considering contributing to this project. It's always great to see people interested in CTR!

This website was built on `Python` and `TypeScript`. The REST API backend uses `Flask` as a framework
and `SQLAlchemy` as an ORM library to interact with the `PostgreSQL` database. The frontend is built with `React`,
or more specifically, `Vite`. Besides that, I am using `Docker` to containerize the application.

If any of these technologies sound familar to you and there's something you think the site is lacking, have a go
at implementing it yourself.

Here is an overview of contents in this document:

* [Development Environment Setup](#development-environment-setup)
* [Faking Data](#faking-data)
* [Test Coverage](#test-coverage)
* [Model DTOs](#model-dtos)

## Development Environment Setup

It is probably better if you create a new virtual environment. You can obviously also just install all requirements in your
global python environment, but I recommend using a virtual environment.

```bash
$ python -m venv .venv
$ source .venv/bin/activate
```

If you use windows ~~you have my condolences~~ you need to search for the correct command to activate the virtual environment.

After you activated the virtual environment, you can install the requirements:

```bash
$ pip install -r requirements.txt
```

Running the REST API backend is then as simple as:

```bash
$ flask --app api run
```

## Faking Data

You might not always have a database dump from the live database ready to test your local application
instance with some data. This is where the `FakerService` comes in. A handy utility which can generate
a lot of fake data. This is especially useful if you want to test if your functions scale well as the dataset
grows.

The `FakerService` can be interfaced via CLI using the `flask faker` command. The command has a few subcommands:

```
(.venv) garma@garma-pc /srv/http/ctr_custom_tracks$ flask --app api faker                                                                                                                                                 ✹ ✚main 
Usage: flask faker [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate_all
  generate_custom_tracks
  generate_resources
  generate_tags
  generate_users
```

There is not much else to say besides this help text. If you need to generate fake data for new entities you added,
you can just extend the `FakerService` and extend the CLI command to make the new generator accessible.

## Test Coverage

If you develop a new feature, make sure to write unit tests for it. I am not going
to merge PRs that don't have proper test coverage. You don't need to unit test *everything* ...
just be sensible about it and make sure your feature at least works.

Alternatively, you can also write integration tests. But I might still reject your PR if you wrote an integration test
for something that should and can be unit tested.

The project comes with the `coverage` package, which is used to measure the test coverage of the project. You can check
your test coverage with:

```bash
$ python -m coverage run -m unittest discover -v --pattern "*test.py" 
```

The current test coverage is around 95%.

## Model DTOs

If you want to connect an external service to the API you can export DTOs for all models via the REST API.
Currently, there is one implementation for `TypeScript` and one for `Python`.

The endpoint is reachable via `GET /api/v1/dtos?generator_type={language}`, where `language` is either `python` or `typescript`.

In case you want to add another language, feel free to do so. The steps necessary to add a new DTO generator are quite simple:

* Create a new generator class that implements the `DTOGenerator` interface, for example `JavaDTOGenerator`
* Register the new generator in the `DTOGeneratorServiceFactory`

Example:

```python
dto_generator_service.register_generator('java', JavaDTOGenerator())
```

And that's it. The generator is now automatically available via the REST API if you pass `generator_type=java` as a query parameter.
