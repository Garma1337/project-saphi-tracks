use crate::models::resource::Resource;
use crate::repository::filter::resource_filter::ResourceFilter;
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

    pub fn find(&mut self, filter: ResourceFilter) -> QueryResult<Vec<Resource>> {
        let mut query = resources::table.into_boxed();

        if let Some(id) = filter.id {
            query = query.filter(resources::id.eq(id));
        }

        if let Some(custom_track_id) = filter.custom_track_id {
            query = query.filter(resources::custom_track_id.eq(custom_track_id));
        }

        if let Some(search_text) = filter.search_text {
            query = query.filter(resources::file_name.ilike(format!("%{}%", search_text)));
        }

        if let Some(resource_type) = filter.resource_type {
            query = query.filter(resources::resource_type.eq(resource_type));
        }

        query.load::<Resource>(&mut self.connection)
    }

    pub fn create(&mut self, new_resource: &Resource) -> QueryResult<Resource> {
        diesel::insert_into(resources::table)
            .values(new_resource)
            .get_result(&mut self.connection)
    }

    pub fn update(
        &mut self,
        resource_id: i32,
        updated_resource: &Resource,
    ) -> QueryResult<Resource> {
        diesel::update(resources::table.find(resource_id))
            .set(updated_resource)
            .get_result(&mut self.connection)
    }
}
