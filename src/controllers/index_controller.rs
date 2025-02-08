use crate::http::responses::index::StatusResponse;
use rocket::serde::json::{json, serde_json, Json};
use std::time::SystemTime;

#[get("/")]
pub fn index() -> Json<serde_json::Value> {
    let status_response = StatusResponse {
        status: "ok".to_string(),
        current_time: SystemTime::now()
    };

    Json(json![status_response])
}
