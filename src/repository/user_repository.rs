use crate::models::user::User;
use crate::repository::filter::user_filter::UserFilter;
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

    pub fn find(&mut self, filter: UserFilter) -> QueryResult<Vec<User>> {
        let mut query = users::table.into_boxed();

        if let Some(id) = filter.id {
            query = query.filter(users::id.eq(id));
        }

        if let Some(username) = filter.username {
            query = query.filter(users::username.eq(username));
        }

        if let Some(email) = filter.email {
            query = query.filter(users::email.eq(email));
        }

        if let Some(active) = filter.active {
            query = query.filter(users::active.eq(active));
        }

        query.load::<User>(&mut self.connection)
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
