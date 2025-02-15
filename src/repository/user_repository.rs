use crate::models::users::{Entity as User, Model};
use crate::repository::filter::user_filter::UserFilter;
use sea_orm::prelude::Expr;
use sea_orm::{DatabaseConnection, EntityTrait, PaginatorTrait, QueryFilter, QueryOrder};

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
        let mut cursor = User::find()
            .filter(filter)
            .order_by_asc(Expr::cust(order_by))
            .cursor_by("id")
        ;

        cursor.after(offset);
        cursor.before(offset + limit);

        cursor.all(&self.db).await.unwrap_or_else(|_| vec![])
    }

    pub async fn find_all(&mut self) -> Vec<Model> {
        User::find().all(&self.db).await.unwrap_or_else(|_| vec![])
    }

    pub async fn count(&mut self, filter: &UserFilter) -> i32 {
        User::find().filter(filter).count(&self.db).await.unwrap_or_else(|_| 0) as i32
    }
}
