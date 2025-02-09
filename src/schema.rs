// @generated automatically by Diesel CLI.

diesel::table! {
    custom_tracks (id) {
        id -> Int4,
        author_id -> Int4,
        name -> Varchar,
        description -> Varchar,
        date_created -> Timestamp,
        staff_pick -> Bool,
        verified -> Bool,
    }
}

diesel::table! {
    permissions (id) {
        id -> Int4,
        user_id -> Int4,
        can_edit_custom_tracks -> Bool,
        can_delete_custom_tracks -> Bool,
        can_edit_resources -> Bool,
        can_delete_resources -> Bool,
        can_edit_users -> Bool,
    }
}

diesel::table! {
    resources (id) {
        id -> Int4,
        author_id -> Int4,
        custom_track_id -> Int4,
        file_name -> Varchar,
        file_size -> Int4,
        resource_type -> Varchar,
        checksum -> Varchar,
        version -> Varchar,
        date_created -> Timestamp,
        verified -> Bool,
    }
}

diesel::table! {
    settings (id) {
        id -> Int4,
        category -> Varchar,
        key -> Varchar,
        value -> Varchar,
    }
}

diesel::table! {
    tags (id) {
        id -> Int4,
        name -> Varchar,
    }
}

diesel::table! {
    tags_to_custom_tracks (id) {
        id -> Int4,
        tag_id -> Int4,
        custom_track_id -> Int4,
    }
}

diesel::table! {
    users (id) {
        id -> Int4,
        username -> Varchar,
        email -> Varchar,
        password_hash -> Varchar,
        created_at -> Timestamp,
        verified -> Bool,
    }
}

diesel::joinable!(custom_tracks -> users (author_id));
diesel::joinable!(permissions -> users (user_id));
diesel::joinable!(resources -> custom_tracks (custom_track_id));
diesel::joinable!(resources -> users (author_id));
diesel::joinable!(tags_to_custom_tracks -> custom_tracks (custom_track_id));
diesel::joinable!(tags_to_custom_tracks -> tags (tag_id));

diesel::allow_tables_to_appear_in_same_query!(
    custom_tracks,
    permissions,
    resources,
    settings,
    tags,
    tags_to_custom_tracks,
    users,
);
