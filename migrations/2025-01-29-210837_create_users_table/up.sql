-- Your SQL goes here
CREATE TABLE "users"
(
    "id"            INT4      NOT NULL PRIMARY KEY,
    "username"      VARCHAR   NOT NULL,
    "email"         VARCHAR   NOT NULL,
    "password_hash" VARCHAR   NOT NULL,
    "created_at"    TIMESTAMP NOT NULL,
    "verified"      BOOL      NOT NULL
);
