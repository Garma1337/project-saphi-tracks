use crate::app::{App, ServiceContainer};
use crate::http::responses::paginated_result::PaginatedResult;
use crate::repository::filter::tag_filter::TagFilter;
use crate::repository::tag_repository::TagRepository;
use crate::util::pagination::Pagination;
use rocket::serde::json::{json, serde_json, Json};

#[get("/?<id>&<name>&<page>")]
pub async fn index(id: Option<i32>, name: Option<String>, page: Option<i32>) -> Json<serde_json::Value> {
    let db = App::db().await;
    let mut repository = TagRepository::new(db);

    let filter = TagFilter { id, name };
    let tag_count = repository.count(&filter).await;

    let mut pagination = Pagination::new(1, 20, tag_count);
    if let Some(page) = page {
        pagination.current_page = page;
    }

    let tags = repository.find(
        &filter,
        "id",
        pagination.get_items_per_page(),
        pagination.get_offset()
    ).await;

    Json(json!(PaginatedResult {
        pagination,
        items: tags
    }))
}
