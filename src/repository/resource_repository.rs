use crate::models::resource::Resource;
use crate::schema::resources;
use diesel::prelude::*;

pub struct ResourceRepository {
    pub connection: PgConnection,
}

impl ResourceRepository {
    pub fn new(connection: PgConnection) -> Self {
        ResourceRepository { connection }
    }

    pub fn find_one(&mut self, id: i32) -> QueryResult<Resource> {
        resources::table.find(id).first(&mut self.connection)
    }

    pub fn find(&mut self) -> QueryResult<Vec<Resource>> {
        resources::table.load::<Resource>(&mut self.connection)
    }

    pub fn create(&mut self, new_resource: &Resource) -> QueryResult<Resource> {
        diesel::insert_into(resources::table)
            .values(new_resource)
            .get_result(&mut self.connection)
    }

    pub fn update(&mut self, resource_id: i32, updated_resource: &Resource) -> QueryResult<Resource> {
        diesel::update(resources::table.find(resource_id))
            .set(updated_resource)
            .get_result(&mut self.connection)
    }
}
