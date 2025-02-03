use crate::services::file_system_adapter::file_system_adapter::FileSystemAdapter;
use crate::services::resources::encoder_strategy::EncoderStrategy;

pub struct ResourceService {
    pub encoder_strategy: Box<dyn EncoderStrategy>,
    pub file_system_adapter: Box<dyn FileSystemAdapter>,
}

impl ResourceService {
    pub fn new(encoder_strategy: Box<dyn EncoderStrategy>, file_system_adapter: Box<dyn FileSystemAdapter>) -> ResourceService {
        ResourceService { encoder_strategy, file_system_adapter }
    }

    pub fn encode_filename(&self, file_name: &str) -> String {
        self.encoder_strategy.encode_filename(file_name)
    }

}
