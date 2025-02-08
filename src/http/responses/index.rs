use rocket::serde::{Deserialize, Serialize};
use std::time::SystemTime;

#[derive(Deserialize, Serialize)]
pub struct StatusResponse {
    pub status: String,
    pub current_time: SystemTime
}
