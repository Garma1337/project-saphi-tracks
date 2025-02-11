use crate::http::responses::paginated_result::PaginatedResult;
use crate::repository::custom_track_repository::CustomTrackRepository;
use crate::repository::filter::custom_track_filter::CustomTrackFilter;
use crate::services::di::database_connection_factory::DatabaseConnectionFactory;
use crate::util::pagination::Pagination;
use rocket::serde::json::{json, serde_json, Json};

#[get("/?<id>&<author_id>&<search_text>&<staff_pick>&<verified>&<page>")]
pub async fn index(
    id: Option<i32>,
    author_id: Option<i32>,
    search_text: Option<&str>,
    staff_pick: Option<bool>,
    verified: Option<bool>,
    page: Option<i32>
) -> Json<serde_json::Value> {
    let db = DatabaseConnectionFactory::get_connection().await;
    let mut repository = CustomTrackRepository::new(db);

    let search_text = search_text.map(|s| s.to_string());
    let filter = CustomTrackFilter { id, author_id, search_text, staff_pick, verified };

    let custom_track_count = repository.count(&filter).await;

    let mut pagination = Pagination::new(1, 20, custom_track_count);
    if let Some(page) = page {
        pagination.current_page = page;
    }

    let custom_tracks = repository.find(
        &filter,
        "id",
        pagination.get_items_per_page(),
        pagination.get_offset()
    ).await;

    Json(json!(PaginatedResult {
        pagination,
        items: custom_tracks
    }))
}
