use crate::auth::jwt::JWTManager;
use crate::auth::session::Session;
use crate::models::users::Model as User;
use crate::repository::user_repository::UserRepository;
use chrono::NaiveDateTime;

pub struct SessionManager {
    pub user_repository: UserRepository,
    pub jwt_manager: JWTManager,
}

impl SessionManager {
    pub fn new(user_repository: UserRepository, jwt_manager: JWTManager) -> SessionManager {
        SessionManager {
            user_repository,
            jwt_manager,
        }
    }

    pub async fn create_from_token(&mut self, auth_token: &str) -> Session {
        let jwt = self.jwt_manager.decode_token(auth_token).unwrap();

        let guest = User {
            id: 0,
            username: "?".to_string(),
            email: "?".to_string(),
            password_hash: "".to_string(),
            created_at: NaiveDateTime::from_timestamp(0, 0),
            verified: false,
        };

        match self.user_repository.find_one(jwt.claims.subject).await {
            Some(user) => Session { user, jwt },
            None => Session { user: guest, jwt },
        }
    }
}
