use crate::app::{App, ServiceContainer};
use crate::repository::filter::setting_filter::SettingFilter;
use crate::repository::setting_repository::SettingRepository;
use rocket::serde::json::{serde_json, Json};

#[get("/?<id>&<category>&<key>")]
pub fn index(id: Option<i32>, category: Option<String>, key: Option<String>) -> Json<serde_json::Value> {
    let mut repository = SettingRepository::new(App::db());

    repository
        .find(SettingFilter { id, category, key })
        .map(|settings| Json(serde_json::json!(settings)))
        .unwrap()
}
