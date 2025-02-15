use crate::event::event::{Event, EventName};

#[derive(Clone)]
pub struct EventHandler {
    name: String,
    event_name: EventName,
}

pub trait EventHandlerTrait {
    fn new() -> Self where Self: Sized;
    async fn run(&self, event: Event);
    fn get_name(&self) -> String;
    fn get_event_name(&self) -> EventName;
}
