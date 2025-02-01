use diesel::prelude::*;
use std::time::SystemTime;
use serde::Serialize;

#[derive(Queryable, Selectable, Serialize, Insertable, AsChangeset)]
#[diesel(table_name = crate::schema::custom_tracks)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct CustomTrack {
    pub id: i32,
    pub author_id: i32,
    pub name: String,
    pub description: String,
    pub date_created: SystemTime,
    pub preview: String,
    pub staff_pick: bool,
    pub active: bool
}
