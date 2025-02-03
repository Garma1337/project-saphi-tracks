use crate::repository::filter::user_filter::UserFilter;
use crate::repository::user_repository::UserRepository;
use crate::services::db_connection_factory::DbConnectionFactory;
use diesel::internal::operators_macro::FieldAliasMapper;
use rocket::serde::json::{json, serde_json, Json};

#[get("/?<id>&<username>&<active>")]
pub fn index(
    id: Option<i32>,
    username: Option<&str>,
    active: Option<bool>
) -> Json<serde_json::Value> {
    let db_connection = DbConnectionFactory::factory();
    let mut repository = UserRepository::new(db_connection);

    let username = username.map(|s| s.to_string());

    repository
        .find(UserFilter { id, username, active })
        .map(|users| Json(json!(users)))
        .unwrap()
}
