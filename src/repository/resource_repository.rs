use crate::models::resources::{Entity as Resource, Model};
use crate::repository::filter::resource_filter::ResourceFilter;
use sea_orm::prelude::Expr;
use sea_orm::{DatabaseConnection, EntityTrait, PaginatorTrait, QueryFilter, QueryOrder};

pub struct ResourceRepository {
    pub db: DatabaseConnection,
}

impl ResourceRepository {
    pub fn new(db: DatabaseConnection) -> ResourceRepository {
        ResourceRepository { db }
    }

    pub async fn find(
        &mut self,
        filter: &ResourceFilter,
        order_by: &str,
        limit: i32,
        offset: i32,
    ) -> Vec<Model> {
        let mut cursor = Resource::find()
            .filter(filter)
            .order_by_asc(Expr::cust(order_by))
            .cursor_by("id")
        ;

        cursor.after(offset);
        cursor.before(offset + limit);

        cursor.all(&self.db).await.unwrap_or_else(|_| vec![])
    }

    pub async fn count(&mut self, filter: &ResourceFilter) -> i32 {
        Resource::find().filter(filter).count(&self.db).await.unwrap_or_else(|_| 0) as i32
    }
}
