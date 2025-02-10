use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared(
        "CREATE TABLE `tags_to_custom_tracks`
            (
                `id`              INT4    NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                `tag_id`          INT4    NOT NULL REFERENCES tags (id),
                `custom_track_id` INT4    NOT NULL REFERENCES custom_tracks (id)
            );"
        ).await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared("DROP TABLE `tags_to_custom_tracks`;").await?;

        Ok(())
    }
}
