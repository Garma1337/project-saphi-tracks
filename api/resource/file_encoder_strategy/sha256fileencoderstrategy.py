# coding: utf-8

import hashlib

from werkzeug.utils import secure_filename

from api.resource.file_encoder_strategy.fileencoderstrategy import FileEncoderStrategy, EncodedResourceTarget


class Sha256FileEncoderStrategy(FileEncoderStrategy):

    def encode_file_name(self, file_name: str) -> EncodedResourceTarget:
        encoded_file_name = secure_filename(file_name)

        hash_value = str(hashlib.sha256(encoded_file_name.encode()).hexdigest())
        base_directory = f'{hash_value[0]}{hash_value[1]}/{hash_value[2]}{hash_value[3]}/{hash_value[4]}{hash_value[5]}'

        return EncodedResourceTarget(encoded_file_name, base_directory)
