-- Your SQL goes here
CREATE TABLE "resources"
(
    "id"              INT4      NOT NULL PRIMARY KEY,
    "custom_track_id" INT4      NOT NULL,
    "file_name"       VARCHAR   NOT NULL,
    "file_size"       INT4      NOT NULL,
    "checksum"        VARCHAR   NOT NULL,
    "version"         VARCHAR   NOT NULL,
    "date_created"    TIMESTAMP NOT NULL
);