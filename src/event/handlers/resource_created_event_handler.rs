use crate::event::event::{Event, EventName};
use crate::event::event_handler::EventHandlerTrait;

pub struct ResourceCreatedEventHandler {
    name: String,
    event_name: EventName,
}

impl EventHandlerTrait for ResourceCreatedEventHandler {
    fn new() -> ResourceCreatedEventHandler {
        ResourceCreatedEventHandler {
            name: "ResourceCreatedEventHandler".to_string(),
            event_name: EventName::ResourceCreated,
        }
    }

    async fn run(&self, event: Event) {
        println!("{:?}", event.get_name());
    }

    fn get_name(&self) -> String {
        self.name.clone()
    }

    fn get_event_name(&self) -> EventName {
        self.event_name.clone()
    }
}
