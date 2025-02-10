use sea_orm_migration::{prelude::*, schema::*};

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared(
        "INSERT INTO `tags`
                (`id`, `name`)
            VALUES
                (1, 'USF'),
                (2, 'SF'),
                (3, 'No Turbo Pads'),
                (4, 'No Shortcuts'),
                (5, 'Shortcuts'),
                (6, 'Remake'),
                (7, 'Ice'),
                (8, 'Circular'),
                (9, 'Point to Point'),
                (10, 'Technical'),
                (11, 'Simple'),
                (12, 'Original'),
                (13, 'Multiple Paths'),
                (14, 'Short'),
                (15, 'Long'),
                (16, 'Tight Turns'),
                (17, 'Loose Turns')"
        ).await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        db.execute_unprepared("DELETE FROM `tags`;").await?;

        Ok(())
    }
}
