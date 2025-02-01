use diesel::prelude::*;
use std::time::SystemTime;
use serde::Serialize;

#[derive(Queryable, Selectable, Serialize, Insertable, AsChangeset)]
#[diesel(table_name = crate::schema::resources)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct Resource {
    pub id: i32,
    pub custom_track_id: i32,
    pub file_name: String,
    pub file_size: i32,
    pub checksum: String,
    pub version: String,
    pub date_created: SystemTime,
}
