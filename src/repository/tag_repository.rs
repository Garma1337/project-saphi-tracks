use crate::models::tag::Tag;
use crate::repository::filter::tag_filter::TagFilter;
use crate::schema::tags;
use diesel::prelude::*;

pub struct TagRepository {
    pub connection: PgConnection,
}

impl TagRepository {
    pub fn new(connection: PgConnection) -> TagRepository {
        TagRepository { connection }
    }

    pub fn find_one(&mut self, id: i32) -> QueryResult<Tag> {
        tags::table.find(id).first(&mut self.connection)
    }

    pub fn find(&mut self, tag_filter: TagFilter) -> QueryResult<Vec<Tag>> {
        let mut query = tags::table.into_boxed();

        if let Some(id) = tag_filter.id {
            query = query.filter(tags::id.eq(id));
        }

        if let Some(name) = tag_filter.name {
            query = query.filter(tags::name.eq(name));
        }

        query.load::<Tag>(&mut self.connection)
    }

    pub fn create(&mut self, new_tag: &Tag) -> QueryResult<Tag> {
        diesel::insert_into(tags::table)
            .values(new_tag)
            .get_result(&mut self.connection)
    }

    pub fn update(&mut self, tag_id: i32, updated_tag: &Tag) -> QueryResult<Tag> {
        diesel::update(tags::table.find(tag_id))
            .set(updated_tag)
            .get_result(&mut self.connection)
    }
}
