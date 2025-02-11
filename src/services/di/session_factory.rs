use crate::repository::user_repository::UserRepository;
use crate::services::di::database_connection_factory::DatabaseConnectionFactory;
use crate::services::di::jwt_manager_factory::JWTManagerFactory;
use crate::services::session_manager::SessionManager;

pub struct SessionManagerFactory {}

impl SessionManagerFactory {
    pub async fn get_session_manager() -> SessionManager {
        let db = DatabaseConnectionFactory::get_connection().await;
        let jwt_manager = JWTManagerFactory::get_jwt_manager();

        SessionManager::new(
            UserRepository::new(db),
            jwt_manager
        )
    }
}
