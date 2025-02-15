use crate::services::di::event_manager_factory::EventManagerFactory;
use crate::services::file_system_adapter::local_file_system_adapter::LocalFileSystemAdapter;
use crate::services::resource_service::ResourceService;
use crate::services::resources::md5_encoder_strategy::Md5EncoderStrategy;

pub struct ResourceServiceFactory {}

impl ResourceServiceFactory {
    pub fn get_resource_service<E>() -> ResourceService<E> {
        let event_manager = EventManagerFactory::get_event_manager();
        let encoder_strategy = Md5EncoderStrategy {};
        let file_system_adapter = LocalFileSystemAdapter {};

        ResourceService::new(event_manager, encoder_strategy, file_system_adapter)
    }
}
