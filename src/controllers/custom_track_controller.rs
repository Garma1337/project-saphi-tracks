use crate::repository::custom_track_repository::CustomTrackRepository;
use crate::repository::filter::custom_track_filter::CustomTrackFilter;
use crate::services::db_connection_factory::DbConnectionFactory;
use rocket::serde::json::{json, serde_json, Json};

#[get("/?<id>&<author_id>&<search_text>&<staff_pick>&<active>")]
pub fn index(
    id: Option<i32>,
    author_id: Option<i32>,
    search_text: Option<&str>,
    staff_pick: Option<bool>,
    active: Option<bool>
) -> Json<serde_json::Value> {
    let db_connection = DbConnectionFactory::factory();
    let mut repository = CustomTrackRepository::new(db_connection);

    let search_text = search_text.map(|s| s.to_string());

    repository
        .find(CustomTrackFilter { id, author_id, search_text, staff_pick, active })
        .map(|tracks| Json(json!(tracks)))
        .unwrap()
}
