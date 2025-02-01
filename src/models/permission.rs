use diesel::prelude::*;
use serde::Serialize;

#[derive(Queryable, Selectable, Serialize, Insertable, AsChangeset)]
#[diesel(table_name = crate::schema::permissions)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct Permission {
    pub id: i32,
    pub user_id: i32,
    pub can_edit_custom_tracks: bool,
    pub can_delete_custom_tracks: bool,
    pub can_edit_resources: bool,
    pub can_delete_resources: bool,
    pub can_edit_users: bool,
}
