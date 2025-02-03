use crate::models::permission::Permission;
use crate::schema::permissions;
use diesel::prelude::*;

pub struct PermissionRepository {
    pub connection: PgConnection
}

impl PermissionRepository {
    pub fn new(connection: PgConnection) -> Self {
        PermissionRepository { connection }
    }

    pub fn find(&mut self) -> QueryResult<Vec<Permission>> {
        permissions::table.load::<Permission>(&mut self.connection)
    }

    pub fn find_one(&mut self, permission_id: i32) -> QueryResult<Permission> {
        permissions::table.find(permission_id).first(&mut self.connection)
    }

    pub fn create(&mut self, new_permission: &Permission) -> QueryResult<Permission> {
        diesel::insert_into(permissions::table)
            .values(new_permission)
            .get_result(&mut self.connection)
    }

    pub fn update(&mut self, permission_id: i32, updated_permission: &Permission) -> QueryResult<Permission> {
        diesel::update(permissions::table.find(permission_id))
            .set(updated_permission)
            .get_result(&mut self.connection)
    }
}