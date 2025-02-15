use crate::event::event::{Event, EventName};
use crate::http::requests::session::{LoginRequest, RegisterRequest};
use crate::services::di::event_manager_factory::EventManagerFactory;
use rocket::serde::json::{json, serde_json, Json};
use crate::event::event_manager::EventManager;

#[post("/register", format = "application/json", data = "<register>")]
pub async fn register(register: Json<RegisterRequest>) -> Json<serde_json::Value> {
    Json(json![{}])
}

#[post("/login", format = "application/json", data = "<login>")]
pub async fn login(login: Json<LoginRequest>) -> Json<serde_json::Value> {
    let event_manager: EventManager<E> = EventManagerFactory::get_event_manager();

    event_manager
        .fire_event(Event::new(
            EventName::UserLoggedIn,
            json!({
                "email": login.username.clone(),
                "password": login.password.clone()
            }),
        ))
        .await;

    Json(json![{}])
}

#[post("/logout")]
pub fn logout() -> Json<serde_json::Value> {
    Json(json![{}])
}
