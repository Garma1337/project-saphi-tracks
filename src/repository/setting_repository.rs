use crate::models::settings::{Entity as Setting, Model};
use crate::repository::filter::setting_filter::SettingFilter;
use sea_orm::prelude::Expr;
use sea_orm::{DatabaseConnection, EntityTrait, PaginatorTrait, QueryFilter, QueryOrder};

pub struct SettingRepository {
    pub db: DatabaseConnection,
}

impl SettingRepository {
    pub fn new(db: DatabaseConnection) -> SettingRepository {
        SettingRepository { db }
    }

    pub async fn find(
        &mut self,
        filter: &SettingFilter,
        order_by: &str,
        limit: i32,
        offset: i32,
    ) -> Vec<Model> {
        let mut cursor = Setting::find()
            .filter(filter)
            .order_by_asc(Expr::cust(order_by))
            .cursor_by("id")
        ;

        cursor.after(offset);
        cursor.before(offset + limit);

        cursor.all(&self.db).await.unwrap_or_else(|_| vec![])
    }

    pub async fn count(&mut self, filter: &SettingFilter) -> i32 {
        Setting::find().filter(filter).count(&self.db).await.unwrap_or_else(|_| 0) as i32
    }
}
