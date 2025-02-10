use crate::models::resources::Column;
use sea_orm::sea_query::IntoCondition;
use sea_orm::{ColumnTrait, Condition};

pub struct ResourceFilter {
    pub id: Option<i32>,
    pub author_id: Option<i32>,
    pub custom_track_id: Option<i32>,
    pub search_text: Option<String>,
    pub resource_type: Option<String>,
    pub verified: Option<bool>,
}

impl IntoCondition for ResourceFilter {
    fn into_condition(self) -> Condition {
        let mut condition = Condition::any();

        if let Some(id) = self.id {
            condition = condition.add(Column::Id.eq(id));
        }

        if let Some(author_id) = self.author_id {
            condition = condition.add(Column::AuthorId.eq(author_id));
        }

        if let Some(custom_track_id) = self.custom_track_id {
            condition = condition.add(Column::CustomTrackId.eq(custom_track_id));
        }

        if let Some(search_text) = self.search_text {
            condition = condition.add(Column::FileName.like(search_text));
        }

        if let Some(resource_type) = self.resource_type {
            condition = condition.add(Column::ResourceType.eq(resource_type));
        }

        if let Some(verified) = self.verified {
            condition = condition.add(Column::Verified.eq(verified));
        }

        condition
    }
}
