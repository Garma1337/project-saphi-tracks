use crate::services::semver_validator::SemverValidator;

pub struct SemverValidatorFactory {}

impl SemverValidatorFactory {
    pub fn get_semver_validator() -> SemverValidator {
        SemverValidator {}
    }
}
