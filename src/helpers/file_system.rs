pub struct FileSystem {}

impl FileSystem {
    pub fn store_file(&self, file: &str) -> bool {
        println!("Storing file: {}", file);
        true
    }
}
