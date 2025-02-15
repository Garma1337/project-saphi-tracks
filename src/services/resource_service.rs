use crate::event::event::{Event, EventName};
use crate::event::event_handler::EventHandlerTrait;
use crate::event::event_manager::EventManager;
use crate::services::file_system_adapter::file_system_adapter::FileSystemAdapter;
use crate::services::file_system_adapter::local_file_system_adapter::LocalFileSystemAdapter;
use crate::services::resources::encoder_strategy::EncoderStrategy;
use crate::services::resources::md5_encoder_strategy::Md5EncoderStrategy;
use rocket::serde::json::serde_json::json;

pub struct ResourceService<E: EventHandlerTrait> {
    pub event_manager: EventManager<E>,
    pub encoder_strategy: Md5EncoderStrategy,
    pub file_system_adapter: LocalFileSystemAdapter,
}

impl<E: EventHandlerTrait> ResourceService<E> {
    pub fn new(
        event_manager: EventManager<E>,
        encoder_strategy: Md5EncoderStrategy,
        file_system_adapter: LocalFileSystemAdapter,
    ) -> Self {
        ResourceService {
            event_manager,
            encoder_strategy,
            file_system_adapter,
        }
    }

    pub fn encode_filename(&self, file_name: &str) -> String {
        self.encoder_strategy.encode_filename(file_name)
    }

    pub fn write_file(&self, file_name: &str, file_content: &str) -> Result<(), String> {
        self.file_system_adapter.write_file(file_name, file_content)
    }

    pub async fn create_resource(&self) {
        self.event_manager
            .fire_event(Event::new(
                EventName::ResourceCreated,
                json!({
                    "resource": "resource"
                }),
            ))
            .await;
    }
}
