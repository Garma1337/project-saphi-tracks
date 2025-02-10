use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared(
        "CREATE TABLE `permissions`
            (
                `id`                       INT4 NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                `user_id`                  INT4 NOT NULL REFERENCES users(id),
                `can_edit_custom_tracks`   BOOL NOT NULL,
                `can_delete_custom_tracks` BOOL NOT NULL,
                `can_edit_resources`       BOOL NOT NULL,
                `can_delete_resources`     BOOL NOT NULL,
                `can_edit_users`           BOOL NOT NULL
            );"
        ).await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared("DROP TABLE `permissions`;").await?;

        Ok(())
    }
}
