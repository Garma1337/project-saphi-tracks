use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared(
        "CREATE TABLE `custom_tracks`
            (
                `id`           INT4      NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                `author_id`    INT4      NOT NULL REFERENCES users (id),
                `name`         VARCHAR   NOT NULL,
                `description`  VARCHAR   NOT NULL,
                `date_created` TIMESTAMP NOT NULL,
                `staff_pick`   BOOL      NOT NULL,
                `verified`     BOOL      NOT NULL
            );"
        ).await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared("DROP TABLE `custom_tracks`;").await?;

        Ok(())
    }
}
