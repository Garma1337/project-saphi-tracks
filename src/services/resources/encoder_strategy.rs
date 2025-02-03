pub trait EncoderStrategy {
    fn encode_filename(&self, file_name: &str) -> String;
}
