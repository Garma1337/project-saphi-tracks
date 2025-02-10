use crate::util::pagination::Pagination;
use rocket::serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
pub struct PaginatedResult<T> {
    pub pagination: Pagination,
    pub items: Vec<T>,
}
