use std::collections::HashMap;
use std::hash::Hash;
use crate::event::event::Event;
use crate::event::event_handler::EventHandlerTrait;

pub struct EventManager<E: EventHandlerTrait> {
    handlers: HashMap<String, E>,
}

impl <E: EventHandlerTrait>EventManager<E> {

    pub fn new() -> EventManager<E> {
        EventManager {
            handlers: HashMap::new(),
        }
    }

    pub fn register<H>(&mut self, handler: H) -> Result<(), String> where H: EventHandlerTrait + Hash + Eq {
        if self.handlers.contains_key(&handler) {
            return Err(format!("The event handler {} is already registered", handler.get_name()));
        }

        self.handlers.insert(handler.get_event_name().into(), handler);
        Ok(())
    }

    pub async fn fire_event(&self, event: Event) {
        println!("Firing event: {:?}", event.get_name());

        let handlers = self.handlers.iter().filter(|handler| handler.get_event_name() == event.get_name());
        for handler in handlers {
            println!("Running event handler: {}", handler.get_name());
            handler.run(&event).await;
        }
    }

}
