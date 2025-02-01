use crate::repository::custom_track_repository::CustomTrackRepository;
use ctr_custom_tracks::establish_connection;
use rocket::serde::json::{json, serde_json, Json};

#[get("/")]
pub fn index() -> Json<serde_json::Value> {
    let pg_connection = establish_connection();
    let mut repository = CustomTrackRepository::new(pg_connection);

    repository.find().map(|tracks| Json(json!(tracks))).unwrap()
}

#[get("/show/<id>")]
pub fn show(id: String) -> Json<serde_json::Value> {
    let pg_connection = establish_connection();
    let mut repository = CustomTrackRepository::new(pg_connection);

    repository.find_one(id.parse::<i32>().unwrap()).map(|track| Json(json!(track))).unwrap()
}
