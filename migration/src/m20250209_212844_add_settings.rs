use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared(
        "INSERT INTO `settings`
                (`id`, `category`, `key`, `value`)
            VALUES
                (1, 'general', 'max_file_size', '5242880'),
                (2, 'general', 'accepted_preview_file_types', 'jpg,png')"
        ).await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared("DELETE FROM `settings`;").await?;

        Ok(())
    }
}
