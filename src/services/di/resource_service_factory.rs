use crate::services::file_system_adapter::local_file_system_adapter::LocalFileSystemAdapter;
use crate::services::resource_service::ResourceService;
use crate::services::resources::md5_encoder_strategy::Md5EncoderStrategy;

pub struct ResourceServiceFactory {}

impl ResourceServiceFactory {
    pub fn get_resource_service() -> ResourceService {
        ResourceService::new(Md5EncoderStrategy {}, LocalFileSystemAdapter {})
    }
}
