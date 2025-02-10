use crate::models::settings::{Entity as Setting, Model};
use crate::repository::filter::setting_filter::SettingFilter;
use sea_orm::{DatabaseConnection, EntityTrait};

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
        let mut cursor = Setting::find().filter(filter).cursor_by("id");

        cursor.after(offset);
        cursor.before(offset + limit);

        cursor.all(&self.db).await.unwrap_or_else(|_| vec![])
    }

    pub async fn count(&mut self, filter: &SettingFilter) -> i32 {
        Setting::find().filter(filter).count().await.unwrap_or_else(|_| 0)
    }
}
