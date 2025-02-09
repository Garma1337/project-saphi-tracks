use crate::app::{App, ServiceContainer};
use crate::repository::filter::tag_filter::TagFilter;
use crate::repository::tag_repository::TagRepository;
use rocket::serde::json::{json, serde_json, Json};

#[get("/?<id>&<name>")]
pub fn index(id: Option<i32>, name: Option<String>) -> Json<serde_json::Value> {
    let mut tag_repository = TagRepository::new(App::db());

    tag_repository
        .find(TagFilter { id, name })
        .map(|tags| Json(json!(tags)))
        .unwrap()
}
