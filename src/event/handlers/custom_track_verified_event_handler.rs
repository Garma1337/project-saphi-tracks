use crate::event::event::{Event, EventName};
use crate::event::event_handler::EventHandlerTrait;

pub struct CustomTrackVerifiedEventHandler {
    name: String,
    event_name: EventName,
}

impl EventHandlerTrait for CustomTrackVerifiedEventHandler {
    fn new() -> CustomTrackVerifiedEventHandler {
        CustomTrackVerifiedEventHandler {
            name: "CustomTrackVerifiedEventHandler".to_string(),
            event_name: EventName::CustomTrackVerified,
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
