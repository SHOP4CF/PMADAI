class EncoderConfig:
    def __init__(self, encoder_dir: str, encoder_file_name: str):
        """
        Parameters
        ----------
        encoder_dir:
            Path to the directory containing the encoder file
        encoder_file_name
            Name of file containing the encoder file
        """
        self.encoder_dir = encoder_dir
        self.encoder_file_name = encoder_file_name
