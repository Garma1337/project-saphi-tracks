use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared(
        "CREATE TABLE `settings`
            (
                `id`       INT4    NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                `category` VARCHAR NOT NULL,
                `key`      VARCHAR NOT NULL,
                `value`    VARCHAR NOT NULL
            );"
        ).await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared("DROP TABLE `settings`;").await?;

        Ok(())
    }
}
