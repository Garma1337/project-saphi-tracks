use crate::services::resources::encoder_strategy::EncoderStrategy;
use md5::{Digest, Md5};

pub struct Md5EncoderStrategy {}

impl EncoderStrategy for Md5EncoderStrategy {
    fn encode_filename(&self, file_name: &str) -> String {
        let mut hasher = Md5::new();
        hasher.update(file_name);
        let result = hasher.finalize();
        format!("{:x}", result)
    }
}
