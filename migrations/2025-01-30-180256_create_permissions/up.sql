-- Your SQL goes here
CREATE TABLE "permissions"
(
    "id"                       INT4 NOT NULL PRIMARY KEY,
    "user_id"                  INT4 NOT NULL REFERENCES users(id),
    "can_edit_custom_tracks"   BOOL NOT NULL,
    "can_delete_custom_tracks" BOOL NOT NULL,
    "can_edit_resources"       BOOL NOT NULL,
    "can_delete_resources"     BOOL NOT NULL,
    "can_edit_users"           BOOL NOT NULL
);