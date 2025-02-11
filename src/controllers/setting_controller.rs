use crate::http::responses::paginated_result::PaginatedResult;
use crate::repository::filter::setting_filter::SettingFilter;
use crate::repository::setting_repository::SettingRepository;
use crate::services::di::database_connection_factory::DatabaseConnectionFactory;
use crate::util::pagination::Pagination;
use rocket::serde::json::{json, serde_json, Json};

#[get("/?<id>&<category>&<key>&<page>")]
pub async fn index(
    id: Option<i32>,
    category: Option<String>,
    key: Option<String>,
    page: Option<i32>
) -> Json<serde_json::Value> {
    let db = DatabaseConnectionFactory::get_connection().await;
    let mut repository = SettingRepository::new(db);

    let filter = SettingFilter { id, category, key };
    let setting_count = repository.count(&filter).await;

    let mut pagination = Pagination::new(1, 20, setting_count);
    if let Some(page) = page {
        pagination.current_page = page;
    }

    let settings = repository.find(
        &filter,
        "id",
        pagination.get_items_per_page(),
        pagination.get_offset()
    ).await;

    Json(json!(PaginatedResult {
        pagination,
        items: settings
    }))
}
