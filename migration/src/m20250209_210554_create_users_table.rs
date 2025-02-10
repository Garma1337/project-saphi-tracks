use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared(
        "CREATE TABLE `users`
            (
                `id`            INT4      NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                `username`      VARCHAR   NOT NULL,
                `email`         VARCHAR   NOT NULL,
                `password_hash` VARCHAR   NOT NULL,
                `created_at`    TIMESTAMP NOT NULL,
                `verified`      BOOL      NOT NULL
            );"
        ).await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared("DROP TABLE `users`;").await?;

        Ok(())
    }
}
