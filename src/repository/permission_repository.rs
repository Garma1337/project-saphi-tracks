use crate::models::permissions::{Entity as Permission, Model};
use crate::repository::filter::permission_filter::PermissionFilter;
use sea_orm::{DatabaseConnection, EntityTrait};

pub struct PermissionRepository {
    pub db: DatabaseConnection,
}

impl PermissionRepository {
    pub fn new(db: DatabaseConnection) -> PermissionRepository {
        PermissionRepository { db }
    }

    pub async fn find(
        &mut self,
        filter: &PermissionFilter,
        order_by: &str,
        limit: i32,
        offset: i32,
    ) -> Vec<Model> {
        let mut cursor = Permission::find().filter(filter).cursor_by("id");

        cursor.after(offset);
        cursor.before(offset + limit);

        cursor.all(&self.db).await.unwrap_or_else(|_| vec![])
    }

    pub async fn count(&mut self, filter: &PermissionFilter) -> i32 {
        Permission::find().filter(filter).count().await.unwrap_or_else(|_| 0)
    }
}
