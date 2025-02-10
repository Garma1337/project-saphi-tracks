use crate::models::resources::{Entity as Resource, Model};
use crate::repository::filter::resource_filter::ResourceFilter;
use sea_orm::{DatabaseConnection, EntityTrait};

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
        let mut cursor = Resource::find().filter(filter).cursor_by("id");

        cursor.after(offset);
        cursor.before(offset + limit);

        cursor.all(&self.db).await.unwrap_or_else(|_| vec![])
    }

    pub async fn count(&mut self, filter: &ResourceFilter) -> i32 {
        Resource::find().filter(filter).count().await.unwrap_or_else(|_| 0)
    }
}
