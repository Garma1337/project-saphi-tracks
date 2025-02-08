use crate::app::{App, ServiceContainer};
use crate::repository::filter::user_filter::UserFilter;
use crate::repository::user_repository::UserRepository;
use rocket::serde::json::{json, serde_json, Json};

#[get("/?<id>&<username>&<email>&<active>")]
pub fn index(
    id: Option<i32>,
    username: Option<&str>,
    email: Option<&str>,
    active: Option<bool>
) -> Json<serde_json::Value> {
    let mut repository = UserRepository::new(App::db());

    let username = username.map(|s| s.to_string());
    let email = email.map(|s| s.to_string());

    repository
        .find(UserFilter { id, username, email, active })
        .map(|users| Json(json!(users)))
        .unwrap()
}
