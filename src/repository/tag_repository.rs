use crate::models::tags::{Column, Entity as Tag, Model};
use crate::repository::filter::tag_filter::TagFilter;
use sea_orm::{DatabaseConnection, EntityTrait, QueryFilter};

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
        let mut cursor = Tag::find().filter(filter).cursor_by(Column::Id);

        cursor.after(offset);
        cursor.before(offset + limit);

        cursor.all(&self.db).await.unwrap_or_else(|_| vec![])
    }

    pub async fn count(&mut self, filter: &TagFilter) -> i32 {
        Tag::find().filter(filter).count().await.unwrap_or_else(|_| 0)
    }
}
