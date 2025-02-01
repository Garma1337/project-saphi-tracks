#[macro_use] extern crate rocket;

use crate::controllers::{custom_track_controller, index_controller};

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
        .mount("/api/v1/customtracks", routes![custom_track_controller::index, custom_track_controller::show])
        .mount("/api/v1/resources", routes![])
        .mount("/api/v1/users", routes![])
}
