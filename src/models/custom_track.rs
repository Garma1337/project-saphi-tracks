use diesel::prelude::*;
use serde::Serialize;
use std::time::SystemTime;

#[derive(Queryable, Selectable, Serialize, Insertable, AsChangeset)]
#[diesel(belongs_to(User), table_name = crate::schema::custom_tracks)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct CustomTrack {
    pub id: i32,
    pub author_id: i32,
    pub name: String,
    pub description: String,
    pub date_created: SystemTime,
    pub staff_pick: bool,
    pub verified: bool
}
