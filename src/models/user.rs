use diesel::prelude::*;
use std::time::SystemTime;
use serde::Serialize;

#[derive(Queryable, Selectable, Serialize, Insertable, AsChangeset)]
#[diesel(table_name = crate::schema::users)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct User {
    pub id: i32,
    pub username: String,
    pub email: String,
    pub password_hash: String,
    pub created_at: SystemTime,
    pub active: bool,
}
