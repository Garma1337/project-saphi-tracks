use crate::auth::jwt::JWTManager;
use crate::repository::user_repository::UserRepository;
use crate::services::file_system_adapter::local_file_system_adapter::LocalFileSystemAdapter;
use crate::services::permission_resolver::PermissionResolver;
use crate::services::resource_service::ResourceService;
use crate::services::resources::md5_encoder_strategy::Md5EncoderStrategy;
use crate::services::semver_validator::SemverValidator;
use crate::services::session_factory::SessionFactory;
use dotenvy::dotenv;
use jsonwebtoken::Algorithm;
use sea_orm::{ConnectOptions, Database, DatabaseConnection};
use std::env;
use std::time::Duration;

pub trait ServiceContainer {
    async fn db() -> DatabaseConnection;
    fn jwt_manager() -> JWTManager;
    fn permission_resolver() -> PermissionResolver;
    fn resources() -> ResourceService;
    fn session_factory(db: DatabaseConnection) -> SessionFactory;
    fn semver_validator() -> SemverValidator;
}

pub struct App {}

impl ServiceContainer for App {

    async fn db() -> DatabaseConnection {
        dotenv().ok();

        let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");

        let mut opt = ConnectOptions::new(database_url);
        opt
            .max_connections(100)
            .min_connections(5)
            .connect_timeout(Duration::from_secs(8))
            .acquire_timeout(Duration::from_secs(8))
            .idle_timeout(Duration::from_secs(8))
            .max_lifetime(Duration::from_secs(8));

        Database::connect(opt).await.unwrap()
    }

    fn jwt_manager() -> JWTManager {
        dotenv().ok();

        let secret = env::var("JWT_SECRET").expect("JWT_SECRET must be set");
        let algorithm = Algorithm::HS512;
        let secret_key = secret.to_string();

        JWTManager {
            algorithm,
            secret_key
        }
    }

    fn permission_resolver() -> PermissionResolver {
        PermissionResolver {}
    }

    fn resources() -> ResourceService {
        ResourceService::new(
            Md5EncoderStrategy {},
            LocalFileSystemAdapter {}
        )
    }

    fn session_factory(db: DatabaseConnection) -> SessionFactory {
        SessionFactory::new(
            UserRepository::new(db),
            App::jwt_manager()
        )
    }

    fn semver_validator() -> SemverValidator {
        SemverValidator {}
    }

}
