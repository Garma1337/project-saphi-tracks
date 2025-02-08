use crate::app::{App, ServiceContainer};
use crate::repository::custom_track_repository::CustomTrackRepository;
use crate::repository::filter::custom_track_filter::CustomTrackFilter;
use rocket::serde::json::{json, serde_json, Json};

#[get("/?<id>&<author_id>&<search_text>&<staff_pick>&<active>")]
pub fn index(
    id: Option<i32>,
    author_id: Option<i32>,
    search_text: Option<&str>,
    staff_pick: Option<bool>,
    active: Option<bool>
) -> Json<serde_json::Value> {
    let mut repository = CustomTrackRepository::new(App::db());
    let search_text = search_text.map(|s| s.to_string());

    repository
        .find(CustomTrackFilter { id, author_id, search_text, staff_pick, active })
        .map(|tracks| Json(json!(tracks)))
        .unwrap()
}
