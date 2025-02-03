use crate::services::file_system::file_system::FileSystem;

pub struct LocalFileSystem {}

impl FileSystem for LocalFileSystem {
    fn read_file(&self, path: &str) -> Result<String, String> {
        Ok(String::from("file content"))
    }

    fn write_file(&self, path: &str, content: &str) -> Result<(), String> {
        Ok(())
    }
}
