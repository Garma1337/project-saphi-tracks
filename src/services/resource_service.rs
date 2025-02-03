use crate::services::file_system::file_system::FileSystem;
use crate::services::resources::encoder_strategy::EncoderStrategy;

pub struct ResourceService {
    pub encoder_strategy: Box<dyn EncoderStrategy>,
    pub file_system: Box<dyn FileSystem>,
}

impl ResourceService {
    pub fn new(encoder_strategy: Box<dyn EncoderStrategy>, file_system: Box<dyn FileSystem>) -> ResourceService {
        ResourceService { encoder_strategy, file_system }
    }

    pub fn encode_filename(&self, file_name: &str) -> String {
        self.encoder_strategy.encode_filename(file_name)
    }

}
