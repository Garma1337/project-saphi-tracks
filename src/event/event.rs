use rocket::serde::json::Value;

#[derive(Clone, Debug)]
pub enum EventName {
    UserLoggedIn,
    CustomTrackCreated,
    CustomTrackVerified,
    ResourceCreated,
}

#[derive(Clone)]
pub struct Event {
    name: EventName,
    context: Value,
}

impl Event {
    pub fn new(name: EventName, context: Value) -> Event {
        Event {
            name,
            context,
        }
    }

    pub fn get_name(&self) -> EventName {
        self.name.clone()
    }

    pub fn get_context(&self) -> Value {
        self.context.clone()
    }
}
