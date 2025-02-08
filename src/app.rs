use crate::auth::jwt::JWTManager;
use crate::repository::user_repository::UserRepository;
use crate::services::file_system_adapter::local_file_system_adapter::LocalFileSystemAdapter;
use crate::services::permission_resolver::PermissionResolver;
use crate::services::resource_service::ResourceService;
use crate::services::resources::md5_encoder_strategy::Md5EncoderStrategy;
use crate::services::semver_validator::SemverValidator;
use crate::services::session_factory::SessionFactory;
use diesel::{Connection, PgConnection};
use dotenvy::dotenv;
use jsonwebtoken::Algorithm;
use std::env;

pub trait ServiceContainer {
    fn db() -> PgConnection;
    fn jwt_manager() -> JWTManager;
    fn permission_resolver() -> PermissionResolver;
    fn resources() -> ResourceService;
    fn session_factory() -> SessionFactory;
    fn semver_validator() -> SemverValidator;
}

pub struct App {}

impl ServiceContainer for App {

    fn db() -> PgConnection {
        dotenv().ok();

        let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
        PgConnection::establish(&database_url).unwrap_or_else(|_| panic!("Error connecting to {}", database_url))
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

    fn session_factory() -> SessionFactory {
        SessionFactory::new(
            UserRepository::new(App::db()),
            App::jwt_manager()
        )
    }

    fn semver_validator() -> SemverValidator {
        SemverValidator {}
    }

}
