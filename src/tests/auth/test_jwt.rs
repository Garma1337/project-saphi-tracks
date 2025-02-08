#[cfg(test)]
mod tests {
    use std::time::SystemTime;
    use crate::auth::jwt::JWTManager;
    use jsonwebtoken::Algorithm;

    #[test]
    pub fn test_should_create_token() {
        let jwt_manager = JWTManager::new(
            Algorithm::HS512,
            "secret".to_string(),
        );

        let token = jwt_manager.create_token(1, 3600);
        assert_eq!(token.unwrap().to_string(), "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWJqZWN0IjoxLCJleHAiOjM2MDB9.D0fxvVxOe2AHV6cdwtroSFGIoYikgNgylyMhbHe3-829bVyDjAd07s74InaFuBz2iXNWaWL74jVP5sE46lZF7A".to_string());
    }

    #[test]
    pub fn test_should_decode_token() {
        let jwt_manager = JWTManager::new(
            Algorithm::HS512,
            "secret".to_string(),
        );

        let timestamp = SystemTime::now().duration_since(SystemTime::UNIX_EPOCH).unwrap().as_secs() + 3600;

        let token = jwt_manager.create_token(1, timestamp as usize).unwrap();
        let decoded = jwt_manager.decode_token(&token);

        let claims = decoded.unwrap().claims;

        assert_eq!(claims.subject.to_string(), "1");
        assert_eq!(claims.exp.to_string(), timestamp.to_string());
    }
}
