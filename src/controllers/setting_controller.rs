use crate::repository::setting_repository::SettingRepository;
use crate::services::db_connection_factory::DbConnectionFactory;
use rocket::serde::json::{serde_json, Json};
use crate::repository::filter::setting_filter::SettingFilter;

#[get("/?<id>&<key>")]
pub fn index(id: Option<i32>, key: Option<String>) -> Json<serde_json::Value> {
    let db_connection = DbConnectionFactory::factory();
    let mut repository = SettingRepository::new(db_connection);

    repository
        .find(SettingFilter { id, key })
        .map(|settings| Json(serde_json::json!(settings)))
        .unwrap()
}
