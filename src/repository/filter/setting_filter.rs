use crate::models::settings::Column;
use sea_orm::sea_query::IntoCondition;
use sea_orm::{ColumnTrait, Condition};

pub struct SettingFilter {
    pub id: Option<i32>,
    pub category: Option<String>,
    pub key: Option<String>,
}

impl IntoCondition for &SettingFilter {
    fn into_condition(self) -> Condition {
        let mut condition = Condition::any();

        if let Some(id) = self.id {
            condition = condition.add(Column::Id.eq(id));
        }

        if let Some(category) = &self.category {
            condition = condition.add(Column::Category.eq(category));
        }

        if let Some(key) = &self.key {
            condition = condition.add(Column::Key.eq(key));
        }

        condition
    }
}
