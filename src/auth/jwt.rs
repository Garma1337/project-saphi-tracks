use jsonwebtoken::errors::Error;
use jsonwebtoken::{decode, encode, Algorithm, DecodingKey, EncodingKey, Header, Validation};
use rocket::serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Claims {
    pub subject: i32,
    pub exp: usize,
}

#[derive(Debug)]
pub struct JWT {
    pub claims: Claims,
}

pub struct JWTManager {
    pub algorithm: Algorithm,
    pub secret_key: String,
}

impl JWTManager {
    pub fn new(algorithm: Algorithm, secret: String) -> JWTManager {
        JWTManager {
            algorithm,
            secret_key: secret,
        }
    }

    pub fn create_token(&self, user_id: i32, expires: usize) -> Result<String, Error> {
        let header = Header::new(self.algorithm);
        let claims = Claims {
            subject: user_id,
            exp: expires,
        };
        let encoding_key = EncodingKey::from_secret(self.secret_key.as_bytes());

        encode(&header, &claims, &encoding_key)
    }

    pub fn decode_token(&self, token: &str) -> Result<JWT, String> {
        let decoding_key = DecodingKey::from_secret(self.secret_key.as_bytes());
        let validation = Validation::new(self.algorithm);

        let token_data = decode::<Claims>(&token, &decoding_key, &validation);

        match token_data {
            Ok(token_data) => Ok(JWT { claims: token_data.claims }),
            Err(err) => Err(err.to_string()),
        }
    }
}
