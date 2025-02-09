use diesel::prelude::*;
use serde::Serialize;

#[derive(Queryable, Selectable, Serialize, Insertable, AsChangeset)]
#[diesel(table_name = crate::schema::tags)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct Tag {
    pub id: i32,
    pub name: String,
}

#[derive(Queryable, Selectable, Serialize, Insertable, AsChangeset)]
#[diesel(belongs_to(Tag))]
#[diesel(belongs_to(CustomTrack))]
#[diesel(table_name = crate::schema::tags_to_custom_tracks)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct CustomTrackTag {
    pub id: i32,
    pub tag_id: i32,
    pub custom_track_id: i32,
}
