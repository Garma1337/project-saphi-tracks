use crate::models::custom_tracks::Column;
use sea_orm::sea_query::IntoCondition;
use sea_orm::{ColumnTrait, Condition};

pub struct CustomTrackFilter {
    pub id: Option<i32>,
    pub author_id: Option<i32>,
    pub search_text: Option<String>,
    pub staff_pick: Option<bool>,
    pub verified: Option<bool>,
}

impl IntoCondition for &CustomTrackFilter {
    fn into_condition(self) -> Condition {
        let mut condition = Condition::any();

        if let Some(id) = self.id {
            condition = condition.add(Column::Id.eq(id));
        }

        if let Some(author_id) = self.author_id {
            condition = condition.add(Column::AuthorId.eq(author_id));
        }

        if let Some(search_text) = &self.search_text {
            condition = condition.add(Column::Name.like(search_text));
        }

        if let Some(staff_pick) = self.staff_pick {
            condition = condition.add(Column::StaffPick.eq(staff_pick));
        }

        if let Some(verified) = self.verified {
            condition = condition.add(Column::Verified.eq(verified));
        }

        condition
    }
}
