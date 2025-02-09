#[macro_use] extern crate rocket;

use crate::controllers::{
    custom_track_controller,
    index_controller,
    resource_controller,
    session_controller,
    setting_controller,
    tag_controller,
    user_controller
};

pub mod app;
pub mod auth;
pub mod controllers;
pub mod http;
pub mod models;
pub mod repository;
pub mod schema;
pub mod services;
pub mod tests;
pub mod util;

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index_controller::index])
        .mount("/api/v1/sessions", routes![session_controller::login, session_controller::register])
        .mount("/api/v1/custom_tracks", routes![custom_track_controller::index])
        .mount("/api/v1/permissions", routes![])
        .mount("/api/v1/resources", routes![resource_controller::index, resource_controller::download])
        .mount("/api/v1/settings", routes![setting_controller::index])
        .mount("/api/v1/tags", routes![tag_controller::index])
        .mount("/api/v1/users", routes![user_controller::index])
}
