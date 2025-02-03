pub trait FileSystemAdapter {
    fn read_file(&self, path: &str) -> Result<String, String>;
    fn write_file(&self, path: &str, content: &str) -> Result<(), String>;
}
