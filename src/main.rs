#[macro_use] extern crate rocket;

use crate::controllers::{custom_track_controller, index_controller, resource_controller, user_controller};

pub mod controllers;
pub mod helpers;
pub mod models;
pub mod repository;
pub mod schema;
pub mod services;
pub mod tests;

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index_controller::index])
        .mount("/api/v1/custom_tracks", routes![custom_track_controller::index])
        .mount("/api/v1/permissions", routes![])
        .mount("/api/v1/resources", routes![resource_controller::index, resource_controller::download])
        .mount("/api/v1/settings", routes![])
        .mount("/api/v1/users", routes![user_controller::index])
}
