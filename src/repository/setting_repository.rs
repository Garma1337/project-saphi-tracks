use crate::models::setting::Setting;
use crate::repository::filter::setting_filter::SettingFilter;
use crate::schema::settings;
use diesel::prelude::*;

pub struct SettingRepository {
    pub connection: PgConnection,
}

impl SettingRepository {
    pub fn new(connection: PgConnection) -> Self {
        SettingRepository { connection }
    }

    pub fn find_one(&mut self, id: i32) -> QueryResult<Setting> {
        settings::table.find(id).first(&mut self.connection)
    }

    pub fn find(&mut self, filter: SettingFilter) -> QueryResult<Vec<Setting>> {
        let mut query = settings::table.into_boxed();

        if let Some(id) = filter.id {
            query = query.filter(settings::id.eq(id));
        }

        if let Some(key) = &filter.key {
            query = query.filter(settings::key.ilike(format!("%{}%", key)));
        }

        query.load::<Setting>(&mut self.connection)
    }

    pub fn create(&mut self, new_setting: &Setting) -> QueryResult<Setting> {
        diesel::insert_into(settings::table)
            .values(new_setting)
            .get_result(&mut self.connection)
    }

    pub fn update(&mut self, setting_id: i32, updated_setting: &Setting) -> QueryResult<Setting> {
        diesel::update(settings::table.find(setting_id))
            .set(updated_setting)
            .get_result(&mut self.connection)
    }
}
