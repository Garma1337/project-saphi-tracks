use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared(
        "CREATE TABLE `resources`
            (
                `id`              INT4      NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                `author_id`       INT4      NOT NULL REFERENCES users (id),
                `custom_track_id` INT4      NOT NULL REFERENCES custom_tracks (id),
                `file_name`       VARCHAR   NOT NULL,
                `file_size`       INT4      NOT NULL,
                `resource_type`   VARCHAR   NOT NULL,
                `checksum`        VARCHAR   NOT NULL,
                `version`         VARCHAR   NOT NULL,
                `date_created`    TIMESTAMP NOT NULL,
                `verified`        BOOLEAN   NOT NULL
            );"
        ).await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared("DROP TABLE `resources`;").await?;

        Ok(())
    }
}
