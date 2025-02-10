use crate::models::tags::Column;
use sea_orm::sea_query::IntoCondition;
use sea_orm::{ColumnTrait, Condition};

pub struct PermissionFilter {
    pub id: Option<i32>,
    pub name: Option<String>,
}

impl IntoCondition for PermissionFilter {
    fn into_condition(self) -> Condition {
        let mut condition = Condition::any();

        if let Some(id) = self.id {
            condition = condition.add(Column::Id.eq(id));
        }

        if let Some(name) = self.name {
            condition = condition.add(Column::Name.eq(name));
        }

        condition
    }
}
