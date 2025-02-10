use crate::models::custom_tracks::{Entity as CustomTrack, Model};
use crate::repository::filter::custom_track_filter::CustomTrackFilter;
use sea_orm::{DatabaseConnection, EntityTrait, QueryFilter};

pub struct CustomTrackRepository {
    pub db: DatabaseConnection,
}

impl CustomTrackRepository {
    pub fn new(db: DatabaseConnection) -> CustomTrackRepository {
        CustomTrackRepository { db }
    }

    pub async fn find(
        &mut self,
        filter: &CustomTrackFilter,
        order_by: &str,
        limit: i32,
        offset: i32,
    ) -> Vec<Model> {
        let mut cursor = CustomTrack::find().filter(filter).cursor_by("id");

        cursor.after(offset);
        cursor.before(offset + limit);

        cursor.all(&self.db).await.unwrap_or_else(|_| vec![])
    }

    pub async fn count(&mut self, filter: &CustomTrackFilter) -> i32 {
        CustomTrack::find().filter(filter).count().await.unwrap_or_else(|_| 0)
    }
}
