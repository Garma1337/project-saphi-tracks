use crate::services::file_system_adapter::local_file_system_adapter::LocalFileSystemAdapter;
use crate::services::resources::encoder_strategy::EncoderStrategy;
use crate::services::resources::md5_encoder_strategy::Md5EncoderStrategy;

pub struct ResourceService {
    pub encoder_strategy: Md5EncoderStrategy,
    pub file_system_adapter: LocalFileSystemAdapter,
}

impl ResourceService {
    pub fn new(encoder_strategy: Md5EncoderStrategy, file_system_adapter: LocalFileSystemAdapter) -> Self {
        ResourceService {
            encoder_strategy,
            file_system_adapter,
        }
    }

    pub fn encode_filename(&self, file_name: &str) -> String {
        self.encoder_strategy.encode_filename(file_name)
    }
}
