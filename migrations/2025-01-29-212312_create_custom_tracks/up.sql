-- Your SQL goes here
CREATE TABLE "custom_tracks"
(
    "id"           INT4      NOT NULL PRIMARY KEY,
    "author_id"    INT4      NOT NULL,
    "name"         VARCHAR   NOT NULL,
    "description"  VARCHAR   NOT NULL,
    "date_created" TIMESTAMP NOT NULL,
    "preview"      VARCHAR   NOT NULL,
    "staff_pick"   BOOL      NOT NULL,
    "active"       BOOL      NOT NULL
);
