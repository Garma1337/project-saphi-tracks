use crate::app::{App, ServiceContainer};
use crate::http::requests::session::{LoginRequest, RegisterRequest};
use crate::repository::filter::user_filter::UserFilter;
use crate::repository::user_repository::UserRepository;
use rocket::serde::json::{json, serde_json, Json};

#[post("/register", format = "application/json", data = "<register>")]
pub fn register(register: Json<RegisterRequest>) -> Json<serde_json::Value> {
    let mut repository = UserRepository::new(App::db());

    let username = register.username.to_string();
    let password = register.password.to_string();

    Json(json![{}])
}

#[post("/login", format = "application/json", data = "<login>")]
pub fn login(login: Json<LoginRequest>) -> Json<serde_json::Value> {
    let mut repository = UserRepository::new(App::db());

    let username = login.username.to_string();
    let password = login.password.to_string();

    let user_filter = UserFilter {
        id: None,
        email: None,
        username: Some(username),
        verified: Some(true),
    };

    repository
        .find(user_filter)
        .map(|users| Json(json!(users)))
        .unwrap()
}

#[post("/logout")]
pub fn logout() -> Json<serde_json::Value> {
    Json(json![{}])
}
