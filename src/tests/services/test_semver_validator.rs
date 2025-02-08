#[cfg(test)]
mod tests {
    use crate::services::semver_validator::SemverValidator;

    #[test]
    fn test_should_return_true_if_version_is_valid_semver() {
        assert_eq!(SemverValidator::is_valid_version("1.0.0"), true);
        assert_eq!(SemverValidator::is_valid_version("2.21.345"), true);
    }

    #[test]
    fn test_should_return_false_if_version_is_invalid_semver() {
        assert_eq!(SemverValidator::is_valid_version("1.0"), false);
        assert_eq!(SemverValidator::is_valid_version(""), false);
        assert_eq!(SemverValidator::is_valid_version("test"), false);
        assert_eq!(SemverValidator::is_valid_version("1.a.b"), false);
    }
}
