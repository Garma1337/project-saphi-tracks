use crate::services::file_system_adapter::file_system_adapter::FileSystemAdapter;

pub struct LocalFileSystemAdapter {}

impl FileSystemAdapter for LocalFileSystemAdapter {
    fn read_file(&self, path: &str) -> Result<String, String> {
        Ok(String::from("file content"))
    }

    fn write_file(&self, path: &str, content: &str) -> Result<(), String> {
        Ok(())
    }
}
