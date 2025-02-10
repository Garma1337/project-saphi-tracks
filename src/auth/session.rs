use crate::auth::jwt::JWT;
use crate::models::users::Model as User;

pub struct Session {
    pub user: User,
    pub jwt: JWT,
}
