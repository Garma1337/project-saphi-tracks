use crate::event::event_handler::EventHandlerTrait;
use crate::event::event_manager::EventManager;
use crate::event::handlers::custom_track_verified_event_handler::CustomTrackVerifiedEventHandler;
use crate::event::handlers::resource_created_event_handler::ResourceCreatedEventHandler;
use crate::event::handlers::user_logged_in_event_handler::UserLoggedInEventHandler;

pub struct EventManagerFactory {}

impl EventManagerFactory {
    pub fn get_event_manager<E: EventHandlerTrait>() -> EventManager<E> {
        let mut event_manager = EventManager::new();

        event_manager.register(CustomTrackVerifiedEventHandler::new()).expect("Failed to register event handler");
        event_manager.register(ResourceCreatedEventHandler::new()).expect("Failed to register event handler");
        event_manager.register(UserLoggedInEventHandler::new()).expect("Failed to register event handler");

        event_manager
    }
}
