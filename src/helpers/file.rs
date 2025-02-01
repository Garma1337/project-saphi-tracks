use std::fs::metadata;
use std::path::Path;

pub struct File {}

impl File {
    pub fn new() -> Self {
        File {}
    }

    pub fn get_size(&self, path: &str) -> u64 {
        metadata(path).unwrap().len()
    }

    pub fn get_extension(&self, path: &str) -> String {
        let path = Path::new(path);

        match path.extension() {
            Some(ext) => ext.to_str().unwrap().to_string(),
            None => "".to_string(),
        }
    }

    pub fn get_name(&self, path: &str) -> String {
        let path = Path::new(path);

        match path.file_name() {
            Some(name) => name.to_str().unwrap().to_string(),
            None => "".to_string(),
        }
    }
}
