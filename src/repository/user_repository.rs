use crate::models::users::{Entity as User, Model};
use crate::repository::filter::user_filter::UserFilter;
use sea_orm::{DatabaseConnection, EntityTrait};

pub struct UserRepository {
    pub db: DatabaseConnection,
}

impl UserRepository {
    pub fn new(db: DatabaseConnection) -> UserRepository {
        UserRepository { db }
    }

    pub async fn find_one(&mut self, id: i32) -> Option<Model> {
        User::find_by_id(id).one(&self.db).await.unwrap_or(None)
    }

    pub async fn find(
        &mut self,
        filter: &UserFilter,
        order_by: &str,
        limit: i32,
        offset: i32,
    ) -> Vec<Model> {
        let mut cursor = User::find().filter(filter).cursor_by("id");

        cursor.after(offset);
        cursor.before(offset + limit);

        cursor.all(&self.db).await.unwrap_or_else(|_| vec![])
    }

    pub async fn count(&mut self, filter: &UserFilter) -> i32 {
        User::find().filter(filter).count().await.unwrap_or_else(|_| 0)
    }
}
