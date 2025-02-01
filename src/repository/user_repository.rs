use crate::models::user::User;
use crate::schema::users;
use diesel::prelude::*;

pub struct UserRepository {
    pub connection: PgConnection,
}

impl UserRepository {
    pub fn new(connection: PgConnection) -> Self {
        UserRepository { connection }
    }

    pub fn find_one(&mut self, id: i32) -> QueryResult<User> {
        users::table.find(id).first(&mut self.connection)
    }

    pub fn find(&mut self) -> QueryResult<Vec<User>> {
        users::table.load::<User>(&mut self.connection)
    }

    pub fn create(&mut self, new_user: &User) -> QueryResult<User> {
        diesel::insert_into(users::table)
            .values(new_user)
            .get_result(&mut self.connection)
    }

    pub fn update(&mut self, user_id: i32, updated_user: &User) -> QueryResult<User> {
        diesel::update(users::table.find(user_id))
            .set(updated_user)
            .get_result(&mut self.connection)
    }
}
