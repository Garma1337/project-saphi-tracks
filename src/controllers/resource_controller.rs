use crate::app::{App, ServiceContainer};
use crate::repository::filter::resource_filter::ResourceFilter;
use crate::repository::resource_repository::ResourceRepository;
use rocket::fs::NamedFile;
use rocket::serde::json::{json, serde_json, Json};

#[get("/?<id>&<custom_track_id>&<search_text>&<resource_type>")]
pub fn index(
    id: Option<i32>,
    custom_track_id: Option<i32>,
    search_text: Option<&str>,
    resource_type: Option<&str>
) -> Json<serde_json::Value> {
    let mut repository = ResourceRepository::new(App::db());

    let search_text = search_text.map(|s| s.to_string());
    let resource_type = resource_type.map(|s| s.to_string());

    repository
        .find(ResourceFilter { id, custom_track_id, search_text, resource_type })
        .map(|resources| Json(json!(resources)))
        .unwrap()
}

#[get("/download?<id>")]
pub async fn download(id: i32) {
    let mut repository = ResourceRepository::new(App::db());

    let filter = ResourceFilter {
        id: Some(id),
        custom_track_id: None,
        search_text: None,
        resource_type: None,
    };

    let mut result = repository.find(filter).unwrap();

    let resource = result.pop().unwrap();
    NamedFile::open(format!("/resources/{}", resource.file_name)).await.ok();
}
