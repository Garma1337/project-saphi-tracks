use crate::models::tags::{Column, Entity as Tag, Model};
use crate::repository::filter::tag_filter::TagFilter;
use sea_orm::prelude::Expr;
use sea_orm::{DatabaseConnection, EntityTrait, PaginatorTrait, QueryFilter, QueryOrder};

pub struct TagRepository {
    pub db: DatabaseConnection,
}

impl TagRepository {
    pub fn new(db: DatabaseConnection) -> TagRepository {
        TagRepository { db }
    }

    pub async fn find(
        &mut self,
        filter: &TagFilter,
        order_by: &str,
        limit: i32,
        offset: i32,
    ) -> Vec<Model> {
        let mut cursor = Tag::find()
            .filter(filter)
            .order_by_asc(Expr::cust(order_by))
            .cursor_by(Column::Id)
        ;

        cursor.after(offset);
        cursor.before(offset + limit);

        cursor.all(&self.db).await.unwrap_or_else(|_| vec![])
    }

    pub async fn count(&mut self, filter: &TagFilter) -> i32 {
        Tag::find().filter(filter).count(&self.db).await.unwrap_or_else(|_| 0) as i32
    }
}
