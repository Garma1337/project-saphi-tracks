use crate::http::requests::session::{LoginRequest, RegisterRequest};
use rocket::serde::json::{json, serde_json, Json};

#[post("/register", format = "application/json", data = "<register>")]
pub async fn register(register: Json<RegisterRequest>) -> Json<serde_json::Value> {
    Json(json![{}])
}

#[post("/login", format = "application/json", data = "<login>")]
pub async fn login(login: Json<LoginRequest>) -> Json<serde_json::Value> {
    Json(json![{}])
}

#[post("/logout")]
pub fn logout() -> Json<serde_json::Value> {
    Json(json![{}])
}
