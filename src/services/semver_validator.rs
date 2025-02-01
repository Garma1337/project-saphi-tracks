pub struct SemverValidator {}

impl SemverValidator {
    pub fn is_valid_version(&self, version: &str) -> bool {
        let version_parts: Vec<&str> = version.split('.').collect();

        if version_parts.len() != 3 {
            return false;
        }

        for part in version_parts {
            if part.parse::<i32>().is_err() {
                return false
            }
        }

        true
    }
}
