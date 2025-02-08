use crate::auth::jwt::JWT;
use crate::models::user::User;

pub struct Session {
    pub user: User,
    pub jwt: JWT,
}
