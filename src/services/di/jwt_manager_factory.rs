use crate::auth::jwt::JWTManager;
use dotenvy::dotenv;
use jsonwebtoken::Algorithm;
use std::env;

pub struct JWTManagerFactory {}

impl JWTManagerFactory {
    pub fn get_jwt_manager() -> JWTManager {
        dotenv().ok();

        let secret = env::var("JWT_SECRET").expect("JWT_SECRET must be set");
        let algorithm = Algorithm::HS512;
        let secret_key = secret.to_string();

        JWTManager {
            algorithm,
            secret_key,
        }
    }
}
