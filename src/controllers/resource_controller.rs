use crate::app::{App, ServiceContainer};
use crate::http::responses::paginated_result::PaginatedResult;
use crate::repository::filter::resource_filter::ResourceFilter;
use crate::repository::resource_repository::ResourceRepository;
use crate::util::pagination::Pagination;
use rocket::fs::NamedFile;
use rocket::serde::json::{json, serde_json, Json};

#[get("/?<id>&<author_id>&<custom_track_id>&<search_text>&<resource_type>&<verified>&<page>")]
pub async fn index(
    id: Option<i32>,
    author_id: Option<i32>,
    custom_track_id: Option<i32>,
    search_text: Option<&str>,
    resource_type: Option<&str>,
    verified: Option<bool>,
    page: Option<i32>
) -> Json<serde_json::Value> {
    let db = App::db().await;
    let mut repository = ResourceRepository::new(db);

    let search_text = search_text.map(|s| s.to_string());
    let resource_type = resource_type.map(|s| s.to_string());

    let filter = ResourceFilter { id, author_id, custom_track_id, search_text, resource_type, verified };

    let resource_count = repository.count(&filter).await;

    let mut pagination = Pagination::new(1, 20, resource_count);
    if let Some(page) = page {
        pagination.current_page = page;
    }

    let resources = repository.find(
        &filter,
        "id",
        pagination.get_items_per_page(),
        pagination.get_offset()
    ).await;

    Json(json!(PaginatedResult {
        pagination,
        items: resources
    }))
}

#[get("/download?<id>")]
pub async fn download(id: i32) {
    let db = App::db().await;
    let mut repository = ResourceRepository::new(db);

    let filter = ResourceFilter {
        id: Some(id),
        author_id: None,
        custom_track_id: None,
        search_text: None,
        resource_type: None,
        verified: Some(true),
    };

    let mut result = repository.find(&filter, "id", 1, 0).await;

    let resource = result.pop().unwrap();
    NamedFile::open(format!("/resources/{}", resource.file_name)).await.ok();
}
