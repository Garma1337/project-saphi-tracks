use crate::auth::jwt::JWTManager;
use crate::auth::session::Session;
use crate::models::user::User;
use crate::repository::user_repository::UserRepository;
use std::time::SystemTime;

pub struct SessionFactory {
    pub user_repository: UserRepository,
    pub jwt_manager: JWTManager,
}

impl SessionFactory {
    pub fn new(user_repository: UserRepository, jwt_manager: JWTManager) -> SessionFactory {
        SessionFactory {
            user_repository,
            jwt_manager,
        }
    }

    pub fn factory(&mut self, auth_token: &str) -> Session {
        let jwt = self.jwt_manager.decode_token(auth_token).unwrap();

        let mut user = User {
            id: 0,
            username: "?".to_string(),
            email: "?".to_string(),
            password_hash: "".to_string(),
            created_at: SystemTime::now(),
            active: false,
        };

        if jwt.claims.subject > 0 {
            user = self.user_repository.find_one(jwt.claims.subject).unwrap()
        }

        Session { user, jwt }
    }
}
