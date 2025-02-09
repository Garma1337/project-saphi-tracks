-- Your SQL goes here
CREATE TABLE "tags_to_custom_tracks"
(
    "id"              INT4    NOT NULL PRIMARY KEY,
    "tag_id"          INT4    NOT NULL REFERENCES tags (id),
    "custom_track_id" INT4    NOT NULL REFERENCES custom_tracks (id)
);
