#[cfg(test)]
mod tests {
    use crate::services::resources::encoder_strategy::EncoderStrategy;
    use crate::services::resources::md5_encoder_strategy::Md5EncoderStrategy;

    #[test]
    fn test_should_return_md5_encoded_filename() {
        let encoder_strategy = Md5EncoderStrategy {};
        assert_eq!(encoder_strategy.encode_filename("preview.jpg"), "daf3eeae9d3aeb5bdf9a2b9f86ba8bab");
    }
}
