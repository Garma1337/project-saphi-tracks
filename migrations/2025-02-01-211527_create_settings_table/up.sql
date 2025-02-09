-- Your SQL goes here
CREATE TABLE "settings"
(
    "id"       INT4    NOT NULL PRIMARY KEY,
    "category" VARCHAR NOT NULL,
    "key"      VARCHAR NOT NULL,
    "value"    VARCHAR NOT NULL
);
