use crate::http::responses::paginated_result::PaginatedResult;
use crate::repository::filter::user_filter::UserFilter;
use crate::repository::user_repository::UserRepository;
use crate::services::di::database_connection_factory::DatabaseConnectionFactory;
use crate::util::pagination::Pagination;
use rocket::serde::json::{json, serde_json, Json};

#[get("/?<id>&<username>&<email>&<verified>&<page>")]
pub async fn index(
    id: Option<i32>,
    username: Option<&str>,
    email: Option<&str>,
    verified: Option<bool>,
    page: Option<i32>
) -> Json<serde_json::Value> {
    let db = DatabaseConnectionFactory::get_connection().await;
    let mut repository = UserRepository::new(db);

    let username = username.map(|s| s.to_string());
    let email = email.map(|s| s.to_string());

    let filter = UserFilter { id, username, email, verified };
    let user_count = repository.count(&filter).await;

    let mut pagination = Pagination::new(1, 20, user_count);
    if let Some(page) = page {
        pagination.current_page = page;
    }

    let users = repository.find(
        &filter,
        "id",
        20,
        0
    ).await;

    Json(json!(PaginatedResult {
        pagination,
        items: users
    }))
}
