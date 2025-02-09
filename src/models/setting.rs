use diesel::{AsChangeset, Insertable, Queryable, Selectable};
use serde::Serialize;

#[derive(Queryable, Selectable, Serialize, Insertable, AsChangeset)]
#[diesel(table_name = crate::schema::settings)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct Setting {
    pub id: i32,
    pub category: String,
    pub key: String,
    pub value: String,
}
