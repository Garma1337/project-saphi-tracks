use diesel::prelude::*;
use serde::Serialize;
use std::time::SystemTime;

#[derive(Serialize)]
pub enum ResourceType {
    PreviewImage,
    Lev,
    Vrm,
    XDelta,
}

#[derive(Queryable, Selectable, Serialize, Insertable, AsChangeset)]
#[diesel(belongs_to(CustomTrack), table_name = crate::schema::resources)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct Resource {
    pub id: i32,
    pub author_id: i32,
    pub custom_track_id: i32,
    pub file_name: String,
    pub file_size: i32,
    pub resource_type: String,
    pub checksum: String,
    pub version: String,
    pub date_created: SystemTime,
    pub verified: bool,
}
