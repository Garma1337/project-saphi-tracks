use crate::models::users::Column;
use sea_orm::sea_query::IntoCondition;
use sea_orm::{ColumnTrait, Condition};

pub struct UserFilter {
    pub id: Option<i32>,
    pub username: Option<String>,
    pub email: Option<String>,
    pub verified: Option<bool>,
}

impl IntoCondition for UserFilter {
    fn into_condition(self) -> Condition {
        let mut condition = Condition::any();

        if let Some(id) = self.id {
            condition = condition.add(Column::Id.eq(id));
        }

        if let Some(username) = self.username {
            condition = condition.add(Column::Username.eq(username));
        }

        if let Some(email) = self.email {
            condition = condition.add(Column::Email.eq(email));
        }

        if let Some(verified) = self.verified {
            condition = condition.add(Column::Verified.eq(verified));
        }

        condition
    }
}
