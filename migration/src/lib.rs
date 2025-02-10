pub use sea_orm_migration::prelude::*;

mod m20250209_210554_create_users_table;
mod m20250209_210639_create_custom_tracks_table;
mod m20250209_210650_create_resources_table;
mod m20250209_210657_create_permissions_table;
mod m20250209_210701_create_settings_table;
mod m20250209_210707_create_tags_table;
mod m20250209_210718_create_tags_to_custom_track_table;
mod m20250209_212844_add_settings;
mod m20250209_212849_add_tags;

pub struct Migrator;

#[async_trait::async_trait]
impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![
            Box::new(m20250209_210554_create_users_table::Migration),
            Box::new(m20250209_210639_create_custom_tracks_table::Migration),
            Box::new(m20250209_210650_create_resources_table::Migration),
            Box::new(m20250209_210657_create_permissions_table::Migration),
            Box::new(m20250209_210701_create_settings_table::Migration),
            Box::new(m20250209_210707_create_tags_table::Migration),
            Box::new(m20250209_210718_create_tags_to_custom_track_table::Migration),
            Box::new(m20250209_212844_add_settings::Migration),
            Box::new(m20250209_212849_add_tags::Migration),
        ]
    }
}
